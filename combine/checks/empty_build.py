from .core import Check


class EmptyBuildCheck(Check):
    def run(self):
        self.state = 'failed'
