import os
from subprocess import run

from .core import File
from .utils import create_parent_directory


class SassFile(File):
    # @classmethod
    # def class_pre_build_check(cls):
    #     run(['which', 'scss'], check=True)

    def render_to_output(self, output_path, *args, **kwargs):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        target_root, scss_ext = os.path.splitext(target_path)
        css_target_path = target_root + '.css'

        run(['sass', self.path, css_target_path], check=True)
