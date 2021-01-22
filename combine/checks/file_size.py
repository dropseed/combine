import os

from .base import Check
from .issues import Issues, Issue


MAX_FILE_SIZES = {
    ".png": 1_000_000,  # 1 MB
    ".jpg": 1_000_000,  # 1 MB
    ".jpeg": 1_000_000,  # 1 MB
}


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


class FileSizeCheck(Check):
    def __init__(self, path):
        self.path = path

    def run(self):
        issues = Issues()

        _, ext = os.path.splitext(self.path)

        if ext in MAX_FILE_SIZES:
            size = os.path.getsize(self.path)
            max_size = MAX_FILE_SIZES[ext]
            if size > max_size:
                issues.append(
                    Issue(
                        type=f"file-size-too-large",
                        description=f"Files of type {ext} shouldn't be bigger than {sizeof_fmt(max_size)}",
                        context={"output_path": os.path.relpath(self.path)},
                    )
                )

        return issues
