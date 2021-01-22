from .core import File


class IgnoredFile(File):
    def _get_output_relative_path(self):
        return None

    def _render_to_output(self, *args, **kwargs):
        return None
