import datetime
import os
import time
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
from fnmatch import fnmatch
import subprocess
import shlex

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


class Watcher:
    def __init__(self, path, combine):
        self.path = path
        self.combine = combine
        self.observer = Observer()
        self.event_handler = EventHandler(combine)

    def watch(self, while_running_func=None):
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
    def __init__(self, combine, *args, **kwargs):
        self.combine = combine

        # To dedupe modified events
        self.last_valid_event = None
        self.last_event_time = None

        super().__init__(*args, **kwargs)

    def should_ignore_path(self, event_path):
        if self.combine.is_in_output_path(event_path):
            return True

        ignore_dirs = (
            "node_modules",
            ".cache",
            ".venv",
            "env",
        )

        for p in os.path.abspath(event_path).split(os.sep):
            if p in ignore_dirs:
                return True

        ignore_extensions = (".crdownload",)

        if os.path.splitext(event_path)[1] in ignore_extensions:
            return True

        return False

    def is_duplicate_event(self, event):
        return (
            self.last_valid_event
            and event == self.last_valid_event
            and datetime.datetime.now() - self.last_event_time
            < datetime.timedelta(seconds=0.1)
        )

    def valid_event(self, event):
        """When an event is processed, call this to make sure we can
        deduplicate file events that sometimes trigger twice"""
        self.last_valid_event = event
        self.last_event_time = datetime.datetime.now()

    def on_any_event(self, event):
        logger.debug("Event: %s", event)

        # if a file was moved or something, we only care about the destination
        event_path = event.dest_path if hasattr(event, "dest_path") else event.src_path

        if self.should_ignore_path(event_path):
            logger.debug("Ignoring path: %s", event_path)
            return

        if self.is_duplicate_event(event):
            logger.debug("Duplicate event: %s", event)
            return

        for step in self.combine.config.steps:
            command = step["run"]
            for pattern in step.get("watch", []):
                match = False

                if pattern.startswith("/"):
                    # Absolute path pattern
                    match = fnmatch(os.path.abspath(event_path), pattern)
                elif pattern.startswith("./"):
                    # Specified relative path pattern
                    match = fnmatch(os.path.relpath(event_path), pattern[2:])
                else:
                    # Implied relative path pattern
                    match = fnmatch(os.path.relpath(event_path), pattern)

                if match:
                    click.secho(f"❯ Running step for matching {pattern}", bold=True)
                    result = subprocess.run(shlex.split(command))
                    if result.returncode != 0:
                        click.secho(
                            "There was an error running a user command.", fg="red"
                        )
                    break

        timestamp = datetime.datetime.now().strftime("%-I:%M%p").lower()

        if os.path.abspath(event_path) == os.path.abspath(self.combine.config_path):
            click.secho(
                f"❯ {self.combine.config_path} {event.event_type} ({timestamp}): reloading combine and rebuilding site",
                bold=True,
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
                    f"❯ {content_relative_path} {event.event_type} ({timestamp}): ",
                    nl=False,
                    bold=True,
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
                f"❯ {content_relative_path} {event.event_type} ({timestamp}): ",
                nl=False,
                bold=True,
            )

            if len(files) == 1:
                click.echo(f"Rebuilding {files[0].content_relative_path}")
            elif not files:
                click.echo("Rebuliding entire site")
            else:
                click.echo(f"Rebuilding {len(files)} files")
            self.rebuild_site(only_paths=[x.path for x in files])
            self.valid_event(event)

    def reload_combine(self):
        try:
            self.combine.reload()
        except Exception as e:
            logger.error("Error reloading", exc_info=e)
            click.secho("There was an error! See output above.", fg="red")

    def rebuild_site(self, only_paths=None):
        try:
            self.combine.build(only_paths)
        except BuildError:
            click.secho("Build error (see above)", fg="red")
        except Exception as e:
            logger.error("Error building", exc_info=e)
            click.secho("There was an error! See output above.", fg="red")


class Server:
    def __init__(self, path, port=8000):
        self.path = path
        self.port = port
        self.httpd = HTTPServer(self.path, ("", self.port))

    def serve(self):
        self.httpd.serve_forever()


class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""

    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath

    def log_message(self, format, *args):
        """Disable logging"""
        return


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""

    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)
