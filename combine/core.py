import os
import shutil
import subprocess
import shlex
import logging

import jinja2

from .config import Config
from .files import file_class_for_path, ErrorFile
from .jinja import default_extensions, default_filters
from .jinja.exceptions import ReservedVariableError
from .exceptions import BuildError
from .checks.favicon import FaviconCheck
from .checks.issues import Issues


logger = logging.getLogger(__file__)


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

        return variables

    def reload(self):
        """Reload the config and entire jinja environment"""
        self.load()

    def clean(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def build(self, only_paths=None, check=True):
        build_errors = {}

        if not only_paths:
            # completely wipe it
            self.clean()

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        paths_rendered = []
        files_rendered = []

        for file in self.iter_files():
            if (
                file.output_relative_path
                and file.output_relative_path not in paths_rendered
            ):
                if only_paths and file.path not in only_paths:
                    continue

                try:
                    file.render(
                        output_path=self.output_path,
                        jinja_environment=self.jinja_environment,
                    )
                    files_rendered.append(file)
                except Exception as e:
                    build_errors[file.path] = e
                    ErrorFile(file.path, file.content_directory, error=e).render(
                        output_path=self.output_path,
                        jinja_environment=self.jinja_environment,
                    )

                paths_rendered.append(file.output_relative_path)

        if not only_paths:
            self.run_build_steps()

        if build_errors:
            for file_path, error in build_errors.items():
                logger.error(f"Error building {file_path}", exc_info=error)
            raise BuildError()

        if check:
            self.check_build(files=files_rendered, site_checks=(not only_paths))

    def check_build(self, files=[], site_checks=False):
        self.issues = Issues()

        if site_checks:
            for issue in FaviconCheck(site_dir=self.output_path).run():
                self.issues.append(issue)

            if self.issues:
                self.issues.print(f"Issues across your site")

        for file in files:
            # TODO could pass check settings here, just don't know what they should look like
            for issue in file.check_output():
                self.issues.append(issue)

    def run_build_steps(self):
        for step in self.config.steps:
            subprocess.run(shlex.split(step["run"]), check=True)

    def get_related_files(self, content_relative_path):
        files = []
        for file in self.iter_files():
            if (
                content_relative_path in file.references
                or file.content_relative_path == content_relative_path
            ):
                # TODO could this include duplicates? in the content-relative sense?
                files.append(file)
        return files

    def content_relative_path(self, path):
        for content_path in self.content_paths:
            if (
                os.path.commonpath([content_path, path]) != os.getcwd()
                and os.getcwd() in content_path
            ):
                return os.path.relpath(path, content_path)

    def is_in_output_path(self, path):
        return (
            os.path.commonpath([self.output_path, os.path.abspath(path)]) != os.getcwd()
        )

    def iter_files(self):
        for content_directory in self.content_directories:
            for file in content_directory.files:
                yield file


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
