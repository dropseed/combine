import datetime
import os
import time
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler

import click
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    DirModifiedEvent,
    FileDeletedEvent,
    FileMovedEvent,
    DirDeletedEvent,
    DirMovedEvent,
)

from .exceptions import BuildError
from .files.ignored import IgnoredFile
from .logger import logger

from typing import TYPE_CHECKING, Optional, Callable, List, Any, Tuple, Type

if TYPE_CHECKING:
    from .core import Combine
    from repaint import Repaint


class Watcher:
    def __init__(
        self, path: str, combine: "Combine", repaint: Optional["Repaint"] = None
    ) -> None:
        self.path = path
        self.observer = Observer()
        self.event_handler = EventHandler(combine, repaint)

    def watch(self, while_running_func: Callable = None) -> None:
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            if while_running_func is not None:
                while_running_func()
            else:
                while True:
                    time.sleep(1)
        except (Exception, KeyboardInterrupt) as e:
            print(e)
            self.observer.stop()
        self.observer.join()


class EventHandler(FileSystemEventHandler):
    def __init__(
        self,
        combine: "Combine",
        repaint: Optional["Repaint"],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.combine = combine
        self.repaint = repaint

        # To dedupe modified events
        self.last_valid_event: Optional[FileSystemEventHandler] = None
        self.last_event_time: Optional[datetime.datetime] = None

        super().__init__(*args, **kwargs)

    def should_ignore_path(self, event_path: str) -> bool:
        ignore_dirs = (
            "node_modules",
            ".cache",
            ".venv",
            "env",
            ".git",
        )

        for p in os.path.abspath(event_path).split(os.sep):
            if p in ignore_dirs:
                return True

        ignore_extensions = (".crdownload",)

        if os.path.splitext(event_path)[1] in ignore_extensions:
            return True

        return False

    def is_duplicate_event(self, event: FileSystemEventHandler) -> bool:
        return (
            self.last_valid_event is not None
            and self.last_event_time is not None
            and event == self.last_valid_event
            and (datetime.datetime.now() - self.last_event_time)
            < datetime.timedelta(seconds=0.1)
        )

    def valid_event(self, event: FileSystemEventHandler) -> None:
        """When an event is processed, call this to make sure we can
        deduplicate file events that sometimes trigger twice"""
        self.last_valid_event = event
        self.last_event_time = datetime.datetime.now()

    def on_any_event(self, event: FileSystemEventHandler) -> None:
        logger.debug("Event: %s", event)

        # if a file was moved or something, we only care about the destination
        event_path = event.dest_path if hasattr(event, "dest_path") else event.src_path

        if self.should_ignore_path(event_path):
            logger.debug("Ignoring path: %s", event_path)
            return

        if self.is_duplicate_event(event):
            logger.debug("Duplicate event: %s", event)
            return

        if self.combine.is_in_output_path(event_path):
            _, ext = os.path.splitext(event_path)
            if ext in (".css", ".img", ".js") and self.repaint:
                output_relative_path = os.path.relpath(
                    event_path, self.combine.output_path
                )
                logger.debug("Repainting output path: %s", output_relative_path)
                self.repaint.reload_assets([output_relative_path])
            else:
                logger.debug("Ignoring output path: %s", event_path)
            return

        for step in self.combine.config.steps:
            matched_pattern = step.watch_pattern_match(event_path)
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

        if os.path.abspath(event_path) == os.path.abspath(self.combine.config_path):
            click.secho(
                f"{self.combine.config_path} {event.event_type}: reloading combine and rebuilding site",
                bold=True,
                color=True,
            )
            self.reload_combine()
            self.rebuild_site()
            self.valid_event(event)
            return

        content_relative_path = self.combine.content_relative_path(
            os.path.abspath(event_path)
        )

        if content_relative_path:

            if isinstance(event, (FileCreatedEvent, DirModifiedEvent)):
                # Reload first, so we know about any new files
                self.reload_combine()

            if isinstance(
                event,
                (FileDeletedEvent, DirDeletedEvent, DirMovedEvent, FileMovedEvent),
            ):
                click.secho(
                    f"{content_relative_path} {event.event_type}: ",
                    nl=False,
                    bold=True,
                    color=True,
                )
                click.echo("Rebuilding entire site")
                self.reload_combine()
                self.rebuild_site()
                self.valid_event(event)
                return

            files = self.combine.get_related_files(content_relative_path)

            if files and all([type(f) == IgnoredFile for f in files]):
                return

            click.secho(
                f"{content_relative_path} {event.event_type}: ",
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
            self.valid_event(event)

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
