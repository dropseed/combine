from .core import Check


class CheckRegistry:
    def __init__(self):
        self.registered_checks = set()

    def register(self, check):
        assert issubclass(check, Check), "Check must be an instance of Check"
        self.registered_checks.add(check)
        return check


registry = CheckRegistry()
register = registry.register
