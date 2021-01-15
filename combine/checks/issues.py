import click


class Issue:
    def __init__(self, type, context={}):
        self.type = type
        self.context = context

    def as_data(self):
        return {
            "type": self.type,
            "context": self.context,
        }


class Issues:
    def __init__(self):
        self._issues = []

    def __str__(self):
        return f"{len(self._issues)} issues"

    def __len__(self):
        return len(self._issues)

    def __iter__(self):
        return iter(self._issues)

    def append(self, issue):
        self._issues.append(issue)

    def print(self, header):
        click.secho(header, fg="yellow")
        for index, issue in enumerate(self._issues):
            click.secho(f"  {index+1}. {issue.type}\n", fg="yellow", bold=True)
            for k, v in issue.context.items():
                click.secho(f"     {k}: {json.dumps(v)}", fg="yellow")
        click.echo()

    def as_data(self):
        return [issue.as_data() for issue in self._issues]
