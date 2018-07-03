from .registry import registry


class CheckRunner:
    def __init__(self, combine):
        self.combine = combine
        self.registry = registry
        self.checks = [x(self.combine) for x in self.registry.registered_checks]

    def run(self):
        all_messages = []

        for check in self.checks:
            messages = check.run()
            if messages:
                all_messages = all_messages + messages

        return all_messages
