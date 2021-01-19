from pprint import pformat

import click


class Issue:
    def __init__(self, type, description, context={}):
        self.type = type
        self.description = description
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
        click.secho("\n" + header, fg="yellow")
        for index, issue in enumerate(self._issues):
            # TODO could just be yaml format?
            click.secho(
                f"\n  {index+1}. {issue.description}", fg="yellow", bold=True,
            )
            click.secho(
                f"     https://combine.dropseed.io/checks/#{issue.type}\n", fg="yellow"
            )
            for k, v in issue.context.items():
                click.secho(f"     {k}: {pformat(v)}", fg="yellow")
        click.echo()

    def as_data(self):
        return [issue.as_data() for issue in self._issues]
