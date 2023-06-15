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


class ChangeResult:
    def __init__(
        self, *, reload: bool = False, rebuild: bool = False, rebuild_paths: list = []
    ) -> None:
        self.reload = reload
        self.rebuild = rebuild
        self.rebuild_paths = rebuild_paths


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
        self.combine = combine
        self.repaint = repaint

    def watch(self) -> None:
        for changes in watch(self.path, recursive=True, debug=self.debug):
            change_results = [
                self.process_change(change, path) for change, path in changes
            ]

            reload = False
            rebuild = False
            rebuild_paths = []
            rebuild_all_paths = False

            for change_result in change_results:
                if not change_result:
                    continue

                if change_result.reload:
                    reload = True

                if change_result.rebuild:
                    rebuild = True

                if change_result.rebuild_paths:
                    rebuild_paths.extend(change_result.rebuild_paths)
                else:
                    rebuild_all_paths = True

            if reload:
                self.reload_combine()

            if rebuild:
                self.rebuild_site([] if rebuild_all_paths else list(set(rebuild_paths)))

    def reload_combine(self) -> None:
        click.secho("Reloading combine", bold=True, color=True)
        try:
            self.combine.reload()
        except Exception as e:
            logger.error("Error reloading", exc_info=e)
            click.secho("There was an error! See output above.", fg="red", color=True)

    def rebuild_site(self, only_paths: List[str] = []) -> None:
        if len(only_paths) == 1:
            click.secho(f"--> Rebuilding {only_paths[0]}", bold=True, color=True)
        elif len(only_paths) > 1:
            click.secho(
                f"--> Rebuilding {len(only_paths)} paths", bold=True, color=True
            )
        else:
            click.secho("--> Rebuilding entire site", bold=True, color=True)

        try:
            self.combine.build(only_paths)
            if self.repaint:
                self.repaint.reload()
        except BuildError:
            click.secho("Build error (see above)", fg="red", color=True)
        except Exception as e:
            logger.error("Error building", exc_info=e)
            click.secho("There was an error! See output above.", fg="red", color=True)

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

    def process_change(self, change: Change, path: str) -> Optional[ChangeResult]:
        logger.debug("Event: %s %s", change.name, path)

        if self.should_ignore_path(path):
            logger.debug("Ignoring path: %s", path)
            return None

        if self.combine.is_in_output_path(path):
            _, ext = os.path.splitext(path)
            if ext in (".css", ".js") and self.repaint:
                output_relative_path = os.path.relpath(path, self.combine.output_path)
                logger.debug("Repainting output path: %s", output_relative_path)
                self.repaint.reload_assets([output_relative_path])
            else:
                logger.debug("Ignoring output path: %s", path)
            return None

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
            return ChangeResult(reload=True, rebuild=True)

        content_relative_path = self.combine.content_relative_path(
            os.path.abspath(path)
        )

        if content_relative_path:
            if change == Change.deleted:
                click.secho(
                    f"{content_relative_path} {change.name}: ",
                    bold=True,
                    color=True,
                )
                return ChangeResult(reload=True, rebuild=True)

            if change in (Change.added, Change.modified):
                # Reload first, so we know about any new files
                self.reload_combine()

            files = self.combine.get_related_files(content_relative_path)

            if files and all([type(f) == IgnoredFile for f in files]):
                return None

            click.secho(
                f"{content_relative_path} {change.name}: ",
                bold=True,
                color=True,
            )

            return ChangeResult(rebuild=True, rebuild_paths=[x.path for x in files])

        return None


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
