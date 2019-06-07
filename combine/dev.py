import logging
import os
import time
from fnmatch import fnmatch
import subprocess
import shlex

import livereload
import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, DirModifiedEvent

from .files.template import TemplateFile


logger = logging.getLogger(__file__)


class Watcher:
    def __init__(self, path, combine):
        self.path = path
        self.combine = combine
        self.observer = Observer()
        self.event_handler = EventHandler(combine)

    def watch(self, while_running_func):
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while_running_func()
        except (ServerQuit, Exception) as e:
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
            for pattern in step["watch"]:
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

        if os.path.abspath(event_path) == os.path.abspath(self.combine.config_path):
            print(event)
            self.reload_combine()
            self.rebuild_site()

        if self.combine.is_in_content_paths(os.path.abspath(event_path)):
            print(event)
            if isinstance(event, (FileCreatedEvent, DirModifiedEvent)):
                self.reload_combine()

            file_obj = self.combine.get_file_obj_for_path(event_path)
            if isinstance(file_obj, TemplateFile):
                # if it was a template, we want to rebuild everything that uses it,
                # but right now we just rebuild the entire site
                self.rebuild_site()
            else:
                self.rebuild_site(only_paths=[os.path.abspath(event_path)])

    def reload_combine(self):
        click.secho("Reloading combine", fg="cyan")
        try:
            self.combine.reload()
        except Exception as e:
            logger.error("Error reloading", exc_info=e)
            click.secho("There was an error! See output above.", fg="red")

    def rebuild_site(self, only_paths=None):
        try:
            self.combine.build(only_paths)
            if only_paths:
                cwd = os.getcwd()
                nice_paths = [os.path.relpath(x, cwd) for x in only_paths]
                click.secho(f'Rebuilt {",".join(nice_paths)}', fg="green")
            else:
                click.secho(f"Rebuilt site", fg="green")
        except Exception as e:
            logger.error("Error building", exc_info=e)
            click.secho("There was an error! See output above.", fg="red")


class Server:
    def __init__(self, path, port=8000):
        self.path = path
        self.port = port
        self.server = livereload.Server()

    def serve(self):
        # livereload_logger = logging.getLogger('livereload')
        # livereload_logger.setLevel(logging.ERROR)
        self.server.serve(root=self.path, port=self.port, debug=False)
        raise ServerQuit()


class ServerQuit(Exception):
    pass
