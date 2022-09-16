import os

from .base import Check
from .issues import Issues, Issue


MAX_FILE_SIZES = {
    ".png": 10_000_000,  # 10 MB
    ".jpg": 10_000_000,  # 10 MB
    ".jpeg": 10_000_000,  # 10 MB
}


def sizeof_fmt(num: float) -> str:
    for unit in [" bytes", "KB", "MB", "GB"]:
        if abs(num) < 1000.0:
            return "%3.1f%s" % (num, unit)
        num /= 1000.0
    return "%.1f%s" % (num, "Yi")


class FileSizeCheck(Check):
    def __init__(self, path: str) -> None:
        self.path = path

    def run(self) -> Issues:
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
                        context={
                            "output_path": os.path.relpath(self.path),
                            "file_size": sizeof_fmt(size),
                        },
                    )
                )

        return issues
