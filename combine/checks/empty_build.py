import os

from .core import Check
from . import states


class EmptyBuildCheck(Check):
    """Ensures that the output directory actually has files in it"""
    def run(self):
        if not os.listdir(self.combine.output_path):
            self.state = states.FAILED
        else:
            self.state = states.SUCCEEDED
