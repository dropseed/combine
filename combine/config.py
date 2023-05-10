from typing import List, Iterator, Union
import os
import datetime
import subprocess
import shlex
from fnmatch import fnmatch
import json
from .logger import logger
import yaml


class Config:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = {}

        if os.path.exists(self.path):
            self.data = yaml.safe_load(open(self.path, "r"))

    @property
    def output_path(self) -> str:
        return os.path.abspath(self.data.get("output_path", "output"))

    @property
    def content_paths(self) -> List[str]:
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
    def variables(self) -> dict:
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
    def default_variables(self) -> dict:
        return {"now": datetime.datetime.now}  # as a function

    @property
    def steps(self) -> Iterator["BuildStep"]:
        for step in self.data.get("steps", []):
            yield BuildStep(
                run=step.get("run", None),
                watch=step.get("watch", None),
            )

    def run_build_steps(self) -> None:
        for step in self.steps:
            if step.has_run_process:
                step.run_process()


class BuildStep:
    def __init__(self, run: str = None, watch: Union[List[str], str] = None) -> None:
        if watch and not isinstance(watch, (list, str)):
            raise ValueError(
                "watch must be a string (command) or list of strings (paths to watch)"
            )

        self.run = run
        self.watch = watch

    def get_name(self) -> str:
        """
        Get a step name automatically by parsing the first
        executable name in the watch or run command
        """
        if self.has_watch_process:
            return self.watch.split()[0].split("/")[-1]  # type: ignore

        if self.has_run_process:
            return self.run.split()[0].split("/")[-1]  # type: ignore

        return ""

    @property
    def has_watch_process(self) -> bool:
        return isinstance(self.watch, str)

    @property
    def has_watch_patterns(self) -> bool:
        return isinstance(self.watch, list)

    @property
    def has_run_process(self) -> bool:
        return bool(self.run)

    def run_process(self, check: bool = True) -> subprocess.CompletedProcess:
        if not self.run:
            raise ValueError("No run command specified")

        return subprocess.run(shlex.split(self.run), check=check)

    def watch_pattern_match(self, path: str) -> str:
        if not self.has_watch_patterns:
            return ""

        for pattern in self.watch:  # type: ignore
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

            logger.debug(f"Checking {path} against {pattern} -- {match}")

            if match:
                return pattern

        return ""
