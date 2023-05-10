import threading
import datetime
import os
import time
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler

import click
from watchfiles import watch, Change

from .exceptions import BuildError
from .files.ignored import IgnoredFile
from .logger import logger

from typing import TYPE_CHECKING, Optional, Callable, List, Any, Tuple, Type

if TYPE_CHECKING:
    from .core import Combine
    from repaint import Repaint


class Watcher:
    def __init__(
        self,
        path: str,
        combine: "Combine",
        repaint: Optional["Repaint"] = None,
        debug: bool = False,
    ) -> None:
        self.path = path
        self.debug = debug
        self.event_handler = EventHandler(combine, repaint)

    def watch(self) -> None:
        for changes in watch(self.path, recursive=True, debug=self.debug):
            for change, path in changes:
                self.event_handler.on_any_event(change, path)


class EventHandler:
    def __init__(
        self,
        combine: "Combine",
        repaint: Optional["Repaint"],
    ) -> None:
        self.combine = combine
        self.repaint = repaint

    def should_ignore_path(self, path: str) -> bool:
        # Most of these are filtered already by watch
        ignore_dirs = (
            "node_modules",
            ".cache",
            ".venv",
            "env",
            ".git",
        )

        for p in os.path.abspath(path).split(os.sep):
            if p in ignore_dirs:
                return True

        ignore_extensions = (".crdownload",)

        if os.path.splitext(path)[1] in ignore_extensions:
            return True

        return False

    def on_any_event(self, change: Change, path: str) -> None:
        logger.debug("Event: %s %s", change.name, path)

        if self.should_ignore_path(path):
            logger.debug("Ignoring path: %s", path)
            return

        if self.combine.is_in_output_path(path):
            _, ext = os.path.splitext(path)
            if ext in (".css", ".img", ".js") and self.repaint:
                output_relative_path = os.path.relpath(path, self.combine.output_path)
                logger.debug("Repainting output path: %s", output_relative_path)
                self.repaint.reload_assets([output_relative_path])
            else:
                logger.debug("Ignoring output path: %s", path)
            return

        for step in self.combine.config.steps:
            matched_pattern = step.watch_pattern_match(path)
            if matched_pattern:
                click.secho(
                    f"Running step for matching {matched_pattern}",
                    bold=True,
                    color=True,
                )
                result = step.run_process(check=False)
                if result.returncode != 0:
                    click.secho(
                        "There was an error running a user command.",
                        fg="red",
                        color=True,
                    )

        if os.path.abspath(path) == os.path.abspath(self.combine.config_path):
            click.secho(
                f"{self.combine.config_path} {change.name}: reloading combine and rebuilding site",
                bold=True,
                color=True,
            )
            self.reload_combine()
            self.rebuild_site()
            return

        content_relative_path = self.combine.content_relative_path(
            os.path.abspath(path)
        )

        if content_relative_path:

            if change in (Change.added, Change.modified):
                # Reload first, so we know about any new files
                self.reload_combine()

            if change == Change.deleted:
                click.secho(
                    f"{content_relative_path} {change.name}: ",
                    nl=False,
                    bold=True,
                    color=True,
                )
                click.echo("Rebuilding entire site")
                self.reload_combine()
                self.rebuild_site()
                return

            files = self.combine.get_related_files(content_relative_path)

            if files and all([type(f) == IgnoredFile for f in files]):
                return

            click.secho(
                f"{content_relative_path} {change.name}: ",
                nl=False,
                bold=True,
                color=True,
            )

            if len(files) == 1:
                click.echo(f"Rebuilding {files[0].content_relative_path}")
            elif not files:
                click.echo("Rebuliding entire site")
            else:
                click.echo(f"Rebuilding {len(files)} files")
            self.rebuild_site(only_paths=[x.path for x in files])

    def reload_combine(self) -> None:
        try:
            self.combine.reload()
            if self.repaint:
                self.repaint.reload()
        except Exception as e:
            logger.error("Error reloading", exc_info=e)
            click.secho("There was an error! See output above.", fg="red", color=True)

    def rebuild_site(self, only_paths: List[str] = []) -> None:
        try:
            self.combine.build(only_paths)
            if self.repaint:
                self.repaint.reload()
        except BuildError:
            click.secho("Build error (see above)", fg="red", color=True)
        except Exception as e:
            logger.error("Error building", exc_info=e)
            click.secho("There was an error! See output above.", fg="red", color=True)


class Server:
    def __init__(
        self, path: str, repaint: Optional["Repaint"] = None, port: int = 8000
    ) -> None:
        self.path = path
        self.port = port
        self.repaint = repaint
        self.httpd = HTTPServer(self.path, ("", self.port), repaint)

    def serve(self) -> None:
        self.httpd.serve_forever()


class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""

    @property
    def repaint(self) -> Optional["Repaint"]:
        return self.server.repaint  # type: ignore

    @property
    def base_path(self) -> str:
        return self.server.base_path  # type: ignore

    def inject_repaint(self) -> None:
        if not self.repaint:
            return

        path = self.translate_path(self.path)
        path_extension = os.path.splitext(path)[1]

        if path_extension not in ("", ".html"):
            return

        if path_extension == "":
            # Guess that there is an index.html
            path = os.path.join(path, "index.html")

        if os.path.exists(path):
            with open(path, "r") as f:
                contents = f.read()

            repaint_script = self.repaint.script_tag
            if repaint_script not in contents:
                contents = contents.replace("</body>", repaint_script + "</body>")

            with open(path, "w") as f:
                f.write(contents)

    def do_GET(self) -> None:
        self.inject_repaint()
        return super().do_GET()

    def translate_path(self, path: str) -> str:
        path = super().translate_path(path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.base_path, relpath)
        return fullpath

    def log_message(self, format: str, *args: Any) -> None:
        """Disable logging"""
        return


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""

    def __init__(
        self,
        base_path: str,
        server_address: Tuple[str, int],
        repaint: Optional["Repaint"],
        RequestHandlerClass: Type[HTTPHandler] = HTTPHandler,
    ) -> None:
        self.base_path = base_path
        self.repaint = repaint
        super().__init__(server_address, RequestHandlerClass)
