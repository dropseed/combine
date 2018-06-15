import os

from .core import File
from .ignored import IgnoredFile
from .html import HTMLFile
from .sass import SassFile


def file_class_for_path(path):
    _, ext = os.path.splitext(path)

    if os.path.basename(path).startswith('_') or os.path.basename(path).startswith('.'):
        return IgnoredFile

    classes = {
        '.html': HTMLFile,
        '.sass': SassFile,
        '.scss': SassFile,
    }

    if ext in classes:
        return classes[ext]

    return File
