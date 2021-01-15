import datetime
import logging
import os
import time
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
from fnmatch import fnmatch
import subprocess
import shlex

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, DirModifiedEvent

from .exceptions import BuildError
from .files.template import TemplateFile


logger = logging.getLogger(__file__)


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
        super().__init__(*args, **kwargs)

    def on_any_event(self, event):
        # if a file was moved or something, we only care about the destination
        event_path = event.dest_path if hasattr(event, "dest_path") else event.src_path

        if self.combine.is_in_output_path(event_path):
            # never need to process if in output path
            return

        # if matches a specific pattern, only use that
        for step in self.combine.config.steps:
            command = step["run"]
            for pattern in step.get("watch", []):
                # TODO remove ./ automatically?
                if fnmatch(event_path, pattern):
                    click.secho(
                        "Running command for matching config pattern", fg="cyan"
                    )
                    result = subprocess.run(shlex.split(command))
                    if result.returncode != 0:
                        click.secho(
                            "There was an error running a user command.", fg="red"
                        )
                    return

        timestamp = datetime.datetime.now().strftime("%-I:%M%p").lower()

        if os.path.abspath(event_path) == os.path.abspath(self.combine.config_path):
            print(
                f"File {event.event_type} [{timestamp}]: reloading combine and rebuilding site"
            )
            self.reload_combine()
            self.rebuild_site()

        content_relative_path = self.combine.content_relative_path(
            os.path.abspath(event_path)
        )

        if content_relative_path:
            print(f"File {event.event_type} [{timestamp}]", end=": ")
            if isinstance(event, (FileCreatedEvent, DirModifiedEvent)):
                self.reload_combine()  # why these events

            # TODO given path, get all related files and biuld those
            # template -> build children
            # page -> build includes (children)
            # so, each file needs children - but you have to load that at the end, don't know when evaluating template, for example

            # file_obj = self.combine.get_file_obj_for_path(event_path)
            # if isinstance(file_obj, TemplateFile):
            #     # if it was a template, we want to rebuild everything that uses it,
            #     # but right now we just rebuild the entire site
            #     print("Rebuilding site")
            #     self.rebuild_site()
            # else:

            files = self.combine.get_files_with_reference(content_relative_path)

            print(f"Rebuilding {[x.path for x in files]}")
            self.rebuild_site(only_paths=[x.path for x in files])

            # click.secho("✓", fg="green")

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
        click.secho(f"Serving at http://127.0.0.1:{self.port}", fg="green")
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
