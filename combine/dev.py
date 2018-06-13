import os
import time
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
        if self.combine.is_in_output_path(os.path.abspath(event.src_path)):
            return

        if os.path.abspath(event.src_path) == os.path.abspath(self.combine.config_path):
            print(event)
            self.reload_combine()

        if self.combine.is_in_content_paths(os.path.abspath(event.src_path)):
            print(event)
            self.rebuild_site()

    def reload_combine(self):
        click.secho('Rebuilding combine because of config change', fg='cyan')
        self.combine.reload()
        self.rebuild_site()

    def rebuild_site(self):
        click.secho('Rebuilding site', fg='cyan')
        self.combine.clean_and_build()


class Server:
    def __init__(self, path):
        self.path = path
        self.port = 8000
        self.httpd = HTTPServer(self.path, ("", self.port))

    def serve(self):
        click.secho(f"Serving at http://127.0.0.1:{self.port}", fg='green')
        self.httpd.serve_forever()


class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)
