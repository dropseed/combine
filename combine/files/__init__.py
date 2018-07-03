import os

from .core import File
from .ignored import IgnoredFile
from .template import TemplateFile
from .html import HTMLFile
from .sass import SassFile


def file_class_for_path(path):
    base, ext = os.path.splitext(path)

    if os.path.basename(path).startswith('_') or os.path.basename(path).startswith('.'):
        return IgnoredFile

    secondary_extension_classes = {
        '.template': TemplateFile,
    }

    base2, ext2 = os.path.splitext(base)

    if ext2 in secondary_extension_classes:
        return secondary_extension_classes[ext2]

    classes = {
        '.html': HTMLFile,
        '.sass': SassFile,
        '.scss': SassFile,
    }

    if ext in classes:
        return classes[ext]

    return File
