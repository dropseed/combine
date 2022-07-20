import os
import shutil
import logging
from typing import List, Optional, Iterator, Set, Type

import jinja2

from .config import Config
from .files import file_class_for_path, ErrorFile
from .jinja import default_extensions, default_filters
from .jinja.exceptions import ReservedVariableError
from .exceptions import BuildError
from .checks.favicon import FaviconCheck
from .checks.issues import Issues
from .files import File


logger = logging.getLogger(__file__)


class Combine:
    def __init__(self, config_path: str, env: str = None, variables: dict = {}) -> None:
        self.config_path = config_path
        self.env = env
        self.variables = variables
        self.load()

    def load(self) -> None:
        self.config = Config(self.config_path)

        self.jinja_environment = self.get_jinja_environment(
            content_paths=self.config.content_paths,
            variables=self.get_jinja_variables(self.config.variables),
        )

        self.content_directories = []
        for path in self.config.content_paths:
            cd = ContentDirectory(path)
            cd.load(self.jinja_environment)
            self.content_directories.append(cd)

    @property
    def output_path(self) -> str:
        return self.config.output_path

    def get_jinja_environment(
        self, content_paths: List[str], variables: dict
    ) -> jinja2.Environment:
        choice_loaders = [jinja2.FileSystemLoader(x) for x in content_paths]

        jinja_environment = jinja2.Environment(
            loader=jinja2.ChoiceLoader(choice_loaders),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            undefined=jinja2.StrictUndefined,  # make sure variables exist
            extensions=default_extensions,
        )
        jinja_environment.globals.update(variables)
        jinja_environment.filters.update(default_filters)

        return jinja_environment

    def get_jinja_variables(self, config_variables: dict) -> dict:
        """
        1. combine.yml variables
        2. Combine object variables (CLI, Python, etc.) that should override
        3. Built-in variables
        """
        variables = {
            **config_variables,
            **self.variables,
        }

        if "env" in variables:
            raise ReservedVariableError("env")

        variables["env"] = self.env

        return variables

    def reload(self) -> None:
        """Reload the config and entire jinja environment"""
        self.load()

    def clean(self) -> None:
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def build(self, only_paths: List[str] = [], check: bool = True) -> None:
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
                    file.load(self.jinja_environment)
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
            self.config.run_build_steps()

        if build_errors:
            for file_path, error in build_errors.items():
                logger.error(f"Error building {file_path}", exc_info=error)
            raise BuildError()

        if check:
            self.check_build(files=files_rendered, site_checks=(not only_paths))

    def check_build(self, files: List[File] = [], site_checks: bool = False) -> None:
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

    def get_related_files(self, content_relative_path: str) -> List[File]:
        files = []
        for file in self.iter_files():
            if (
                content_relative_path in file.references
                or file.content_relative_path == content_relative_path
            ):
                # TODO could this include duplicates? in the content-relative sense?
                files.append(file)
        return files

    def content_relative_path(self, path: str) -> Optional[str]:
        for content_path in self.config.content_paths:
            if (
                os.path.commonpath([content_path, path]) != os.getcwd()
                and os.getcwd() in content_path
            ):
                return os.path.relpath(path, content_path)

        return None

    def is_in_output_path(self, path: str) -> bool:
        return (
            os.path.commonpath([self.output_path, os.path.abspath(path)]) != os.getcwd()
        )

    def iter_files(self) -> Iterator[File]:
        for content_directory in self.content_directories:
            for file in content_directory.files:
                yield file


class ContentDirectory:
    def __init__(self, path: str) -> None:
        assert os.path.exists(path), f"Path does not exist: {path}"
        self.path = path

    def load(self, jinja_environment: jinja2.Environment) -> None:
        self.files = []

        for root, dirs, files in os.walk(self.path, followlinks=True):
            for file in files:
                file_path = os.path.join(root, file)
                file_obj = file_class_for_path(file_path)(file_path, self)
                file_obj.load(jinja_environment)
                self.files.append(file_obj)

    def file_classes(self) -> Set[Type[File]]:
        return set([x.__class__ for x in self.files])
