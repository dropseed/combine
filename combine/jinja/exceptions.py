class MissingVariableError(Exception):
    def __init__(self, name):
        self.name = name
        self.message = f'The required variable "{self.name}" is missing'
        super().__init__(self.message)


class ReservedVariableError(Exception):
    def __init__(self, name):
        self.name = name
        self.message = (
            f'The variable"{self.name}" is reserved and should only be set by combine'
        )
        super().__init__(self.message)
