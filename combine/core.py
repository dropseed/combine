import os
import shutil
import subprocess
import shlex

import jinja2

from .config import Config
from .files import file_class_for_path
from .jinja import default_extensions, default_filters
from .jinja.exceptions import ReservedVariableError


class Combine:
    def __init__(self, config_path, env=None, variables={}):
        self.config_path = config_path
        self.env = env
        self.variables = variables
        self.load()

    def load(self):
        self.config = Config(self.config_path)
        self.output_path = self.config.output_path
        self.content_paths = self.config.content_paths

        self.content_directories = [ContentDirectory(x) for x in self.content_paths]

        choice_loaders = [
            jinja2.FileSystemLoader(x.path) for x in self.content_directories
        ]

        self.jinja_environment = jinja2.Environment(
            loader=jinja2.ChoiceLoader(choice_loaders),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            undefined=jinja2.StrictUndefined,  # make sure variables exist
            extensions=default_extensions,
        )
        self.jinja_environment.globals.update(self.get_jinja_variables())
        self.jinja_environment.filters.update(default_filters)

    def get_jinja_variables(self):
        """
        1. combine.yml variables
        2. Combine object variables (CLI, Python, etc.) that should override
        3. Built-in variables
        """
        variables = self.config.variables
        variables.update(self.variables)

        if "env" in variables:
            raise ReservedVariableError("env")

        variables["env"] = self.env

        if not variables.get("base_url", "") and self.env == "development":
            variables["base_url"] = "test"

        return variables

    def reload(self):
        """Reload the config and entire jinja environment"""
        self.load()

    def clean(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def build(self, only_paths=None):
        if not only_paths:
            # completely wipe it
            self.clean()

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        paths_rendered = []

        for content_directory in self.content_directories:
            for file in content_directory.files:
                if (
                    file.output_relative_path
                    and file.output_relative_path not in paths_rendered
                ):
                    if only_paths and file.path not in only_paths:
                        continue

                    file.render_to_output(
                        self.output_path, jinja_environment=self.jinja_environment
                    )
                    paths_rendered.append(file.output_relative_path)

        # If building the entire site, run the custom steps now
        if not only_paths:
            for step in self.config.steps:
                subprocess.run(shlex.split(step["run"]), check=True)

    def get_file_obj_for_path(self, path):
        for content_directory in self.content_directories:
            for file in content_directory.files:
                if os.path.abspath(file.path) == os.path.abspath(path):
                    return file

        return None

    def is_in_content_paths(self, path):
        for content_path in self.content_paths:
            if (
                os.path.commonpath([content_path, path]) != os.getcwd()
                and os.getcwd() in content_path
            ):
                return True
        return False

    def is_in_output_path(self, path):
        return (
            os.path.commonpath([self.output_path, os.path.abspath(path)]) != os.getcwd()
        )


class ContentDirectory:
    def __init__(self, path):
        assert os.path.exists(path), f"Path does not exist: {path}"
        self.path = path
        self.load_files()

    def load_files(self):
        self.files = []

        for root, dirs, files in os.walk(self.path, followlinks=True):
            for file in files:
                file_path = os.path.join(root, file)
                self.files.append(file_class_for_path(file_path)(file_path, self))

    def file_classes(self):
        return set([x.__class__ for x in self.files])
