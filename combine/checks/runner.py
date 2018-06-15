from . import states
from .empty_build import EmptyBuildCheck


class CheckRunner:
    def __init__(self, combine):
        self.combine = combine
        self.check_classes = (
            EmptyBuildCheck,
        )
        self.checks = [x(self.combine) for x in self.check_classes]
        self.state = states.UNKNOWN

    @property
    def succeeded(self):
        return self.state == states.SUCCEEDED

    @property
    def failed_checks(self):
        return [x for x in self.checks if x.state == states.FAILED]

    def run(self):
        self.state = states.RUNNING

        for check in self.checks:
            check.run()

        checks_succeeded = all([x.state == states.SUCCEEDED for x in self.checks])
        if checks_succeeded:
            self.state = states.SUCCEEDED
        else:
            self.state = states.FAILED
