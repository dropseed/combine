from .core import File


class KeepFile(File):
    def _get_output_relative_path(self) -> str:
        # Remove the .keep extension
        return super()._get_output_relative_path()[:-5]
