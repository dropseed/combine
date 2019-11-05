from .core import File


class IgnoredFile(File):
    def get_path_for_output(self):
        return None

    def render_to_output(self, output_path, combine):
        return None
