from .issues import Issues


class Check:
    def run(self) -> Issues:
        raise NotImplementedError
