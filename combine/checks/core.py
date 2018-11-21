class Check:
    def __init__(self, combine):
        self.combine = combine

    def run(self):
        return None


class Message:
    def __init__(self, message, id, hint=None, object=None):
        self.message = message
        self.id = id
        self.hint = hint
        self.object = object

    def __str__(self):
        return (
            f"{self.id}: {self.message}\n  Hint: {self.hint}\n  Object: {self.object}"
        )

    def __repr__(self):
        return "<%s: message=%r, hint=%r, object=%r, id=%r>" % (
            self.__class__.__name__,
            self.message,
            self.hint,
            self.object,
            self.id,
        )

    @property
    def id_number(self):
        return self.id.split(".")[1]

    @property
    def color(self):
        if self.id_number.startswith("E"):
            return "red"
        elif self.id_number.startswith("W"):
            return "yellow"
        return None
