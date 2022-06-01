import os
import datetime
import subprocess
import shlex
from fnmatch import fnmatch
import json

import yaml


class Config:
    def __init__(self, path):
        self.path = path
        self.data = {}

        if os.path.exists(self.path):
            self.data = yaml.safe_load(open(self.path, "r"))
            if self.data is None:
                # allow an empty file to start with
                self.data = {}

    @property
    def output_path(self):
        return os.path.abspath(self.data.get("output_path", "output"))

    @property
    def content_paths(self):
        if "content_paths" in self.data:
            paths = self.data["content_paths"]
        else:
            paths = ["content"]
            if os.path.exists(os.path.join("theme", "content")):
                paths.append(os.path.join("theme", "content"))

        # add the built-in content from combine itself
        paths.append(os.path.join(os.path.dirname(__file__), "base_content"))

        return [os.path.abspath(x) for x in paths]

    @property
    def variables(self):
        variables = self.default_variables

        for name, data in self.data.get("variables", {}).items():
            # To use a dict as a variable, you'd have to nest it under "default"...
            if isinstance(data, dict):
                if "default" in data:
                    variables[name] = data["default"]

                if "from_env" in data and data["from_env"] in os.environ:
                    variables[name] = os.environ[data["from_env"]]

                if "from_file" in data:
                    filename = data["from_file"]
                    _, ext = os.path.splitext(filename)

                    if not os.path.exists(filename):
                        # Treat it like from_env for now -- if it doesn't exist, that's ok
                        # becuase it will error in use if there isn't a default
                        continue
                    elif ext in (".yml", ".yaml"):
                        variables[name] = yaml.safe_load(open(filename, "r"))
                    elif ext == ".json":
                        variables[name] = json.load(open(filename, "r"))
                    else:
                        # Treat as raw text
                        variables[name] = open(filename, "r").read()
            else:
                variables[name] = data

        return variables

    @property
    def default_variables(self):
        return {"now": datetime.datetime.now}  # as a function

    @property
    def steps(self):
        for step in self.data.get("steps", []):
            yield BuildStep(
                run=step.get("run", None),
                watch=step.get("watch", None),
            )

    def run_build_steps(self):
        for step in self.steps:
            if step.has_run_process:
                step.run_process()


class BuildStep:
    def __init__(self, run=None, watch=None):
        if watch and not isinstance(watch, (list, str)):
            raise ValueError(
                "watch must be a string (command) or list of strings (paths to watch)"
            )

        self.run = run
        self.watch = watch

    def get_name(self):
        """
        Get a step name automatically by parsing the first
        executable name in the watch or run command
        """
        if self.has_watch_process:
            return self.watch.split()[0].split("/")[-1]

        if self.has_run_process:
            return self.run.split()[0].split("/")[-1]

        return ""

    @property
    def has_watch_process(self):
        return isinstance(self.watch, str)

    @property
    def has_watch_patterns(self):
        return isinstance(self.watch, list)

    @property
    def has_run_process(self):
        return bool(self.run)

    def run_process(self, check=True):
        return subprocess.run(shlex.split(self.run), check=check)

    def path_matches_watch(self, path):
        if not self.has_watch_patterns:
            return False

        for pattern in self.watch:
            match = False

            if pattern.startswith("/"):
                # Absolute path pattern
                match = fnmatch(os.path.abspath(path), pattern)
            elif pattern.startswith("./"):
                # Specified relative path pattern
                match = fnmatch(os.path.relpath(path), pattern[2:])
            else:
                # Implied relative path pattern
                match = fnmatch(os.path.relpath(path), pattern)

            if match:
                return pattern

        return False
