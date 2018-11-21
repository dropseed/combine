import os

from .core import Check, Message
from .registry import register


@register
class EmptyBuildCheck(Check):
    """Ensures that the output directory actually has files in it"""

    def run(self):
        if not os.listdir(self.combine.output_path):
            return [Message("Output directory is empty", "empty.E001")]
