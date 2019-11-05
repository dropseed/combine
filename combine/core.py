import os
import shutil
import subprocess
import shlex
import gettext

import jinja2
from babel.support import Translations

from .config import Config
from .files import file_class_for_path
from .jinja_extensions import default_extensions


DEFAULT_BUILT_IN_EXTENSIONS = ["jinja2.ext.i18n"]


class Combine:
    def __init__(self, config_path, env=None):
        self.config_path = config_path
        self.env = env
        self.load()

    def load(self):
        self.config = Config(self.config_path)
        self.output_path = self.config.output_path
        self.content_paths = self.config.content_paths

        self._translations = {}
        self.locale_path = os.path.join(os.path.dirname(self.config_path), "locale")
        self.locale_domain = "messages"

        self.content_directories = [ContentDirectory(x) for x in self.content_paths]

        choice_loaders = [
            jinja2.FileSystemLoader(x.path) for x in self.content_directories
        ]

        extensions = default_extensions + DEFAULT_BUILT_IN_EXTENSIONS

        self.jinja_environment = jinja2.Environment(
            loader=jinja2.ChoiceLoader(choice_loaders),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            undefined=jinja2.StrictUndefined,  # make sure variables exist
            extensions=extensions,
        )
        self.jinja_environment.globals.update(self.get_jinja_variables())
        self.jinja_environment.install_gettext_callables(
            gettext.gettext, gettext.ngettext, newstyle=True
        )

    def install_translations(self, locale):
        # only load each translation once
        if locale in self._translations:
            translations = self._translations[locale]
        else:
            translations = Translations.load(
                dirname=self.locale_path, locales=[locale], domain=self.locale_domain
            )
            self._translations[locale] = translations

        self.jinja_environment.install_gettext_translations(translations, newstyle=True)

    def get_jinja_variables(self):
        variables = self.config.variables
        variables["env"] = self.env
        return variables

    def reload(self):
        """Reload the config and entire jinja environment"""
        self.load()

    def clean(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def iter_files(self):
        for content_directory in self.content_directories:
            for file in content_directory.files:
                yield file

    def build(self, only_paths=None):
        if not only_paths:
            # completely wipe it
            self.clean()

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        paths_rendered = []

        for file in self.iter_files():
            if (
                file.output_relative_path
                and file.output_relative_path not in paths_rendered
            ):
                if only_paths and file.path not in only_paths:
                    continue

                file.render_to_output(self.output_path, combine=self)
                paths_rendered.append(file.output_relative_path)

        # If building the entire site, run the custom steps now
        if not only_paths:
            for step in self.config.steps:
                subprocess.run(shlex.split(step["run"]), check=True)

    def get_file_obj_for_path(self, path):
        for file in self.iter_files():
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

        for root, _, files in os.walk(self.path, followlinks=True):
            for file in files:
                file_path = os.path.join(root, file)
                self.files.append(file_class_for_path(file_path)(file_path, self))

    def file_classes(self):
        return set([x.__class__ for x in self.files])
