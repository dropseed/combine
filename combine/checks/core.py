class Check:
    def __init__(self, combine):
        self.combine = combine
        self.state = 'unknown'

    def run(self):
        self.state = 'failed'


class CheckRunner:
    def __init__(self, checks):
        self.checks = checks
        self.state = 'unknown'

    def run(self):
        self.state = 'running'
