from . import states


class Check:
    def __init__(self, combine):
        self.combine = combine
        self.state = states.UNKNOWN

    def run(self):
        self.state = states.FAILED
