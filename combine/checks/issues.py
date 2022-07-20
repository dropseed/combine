from typing import Iterator, List
from pprint import pformat

import click


class Issue:
    def __init__(self, type: str, description: str, context: dict = {}) -> None:
        self.type = type
        self.description = description
        self.context = context

    def as_data(self) -> dict:
        return {
            "type": self.type,
            "context": self.context,
        }


class Issues:
    def __init__(self) -> None:
        self._issues: List[Issue] = []

    def __str__(self) -> str:
        return f"{len(self._issues)} issues"

    def __len__(self) -> int:
        return len(self._issues)

    def __iter__(self) -> Iterator[Issue]:
        return iter(self._issues)

    def append(self, issue: Issue) -> None:
        self._issues.append(issue)

    def print(self, header: str) -> None:
        click.secho("\n" + header, fg="yellow", color=True)
        for index, issue in enumerate(self._issues):
            # TODO could just be yaml format?
            click.secho(
                f"\n  {index+1}. {issue.description}",
                fg="yellow",
                bold=True,
                color=True,
            )
            click.secho(
                f"     https://combine.dropseed.dev/checks/#{issue.type}\n",
                fg="yellow",
                color=True,
            )
            for k, v in issue.context.items():
                click.secho(f"     {k}: {pformat(v)}", fg="yellow", color=True)
        click.echo()

    def as_data(self) -> List[dict]:
        return [issue.as_data() for issue in self._issues]
