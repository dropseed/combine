import os
import shutil

import jinja2

from .config import Config
from .files import file_class_for_path


class Combine:
    def __init__(self, config_path, content_paths, output_path):
        self.config_path = config_path
        self.content_paths = content_paths
        self.content_directories = [ContentDirectory(x) for x in self.content_paths if os.path.exists(x)]
        self.output_path = output_path
        self.reload()

    def reload(self):
        """Reload the config and entire jinja environment"""
        self.config = Config(self.config_path)

        choice_loaders = [jinja2.FileSystemLoader(x.path) for x in self.content_directories]

        self.jinja_environment = jinja2.Environment(
            loader=jinja2.ChoiceLoader(choice_loaders),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            undefined=jinja2.StrictUndefined,  # make sure variables exist
        )
        self.jinja_environment.globals = self.config.get_variables()

    def clean_and_build(self):
        self.clean()
        self.build()

    def clean(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def build(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        paths_rendered = []

        for content_directory in self.content_directories:
            for file in content_directory.files:
                if file.output_relative_path and file.output_relative_path not in paths_rendered:
                    file.render_to_output(
                        self.output_path,
                        jinja_environment=self.jinja_environment,
                    )
                    paths_rendered.append(file.output_relative_path)

    def is_in_content_paths(self, path):
        for cp in self.content_paths:
            if os.path.commonpath([cp, path]) != os.getcwd():
                return True
        return False

    def is_in_output_path(self, path):
        return os.path.commonpath([self.output_path, path]) != os.getcwd()


class ContentDirectory:
    def __init__(self, path):
        self.path = path
        self.load_files()

    def load_files(self):
        self.files = []

        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                self.files.append(
                    file_class_for_path(file_path)(file_path, self)
                )
