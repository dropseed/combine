from .core import File


class IgnoredFile(File):
    def _get_path_for_output(self):
        return None

    def _render_to_output(self, *args, **kwargs):
        return None
