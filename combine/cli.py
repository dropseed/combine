import os

import click
import pygments

from .core import Combine
from .checks import CheckRunner
from .dev import Watcher, Server


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option("--no-checks", is_flag=True, default=False)
@click.option("--env", default="production")
@click.pass_context
def build(ctx, no_checks, env):
    config_path = os.path.abspath("combine.yml")
    combine = Combine(config_path=config_path, env=env)

    click.secho("Building site", fg="cyan")
    combine.build()

    if not no_checks:
        runner = CheckRunner(combine)
        messages = runner.run()
        if messages:
            click.secho("Checks failed.", fg="red")
            for msg in messages:
                click.secho(str(msg), fg=msg.color)
                click.echo()
            exit(1)
        else:
            click.secho("All checks passed!", fg="green")

    return combine


@cli.command()
@click.option("--port", type=int, default=8000)
@click.pass_context
def work(ctx, port):
    combine = ctx.invoke(build, no_checks=True, env="development")

    click.secho("Watching for file changes...", fg="green")

    server = Server(combine.output_path, port)
    watcher = Watcher(".", combine=combine)
    watcher.watch(server.serve)


@cli.group()
@click.pass_context
def utils(ctx):
    pass


@utils.command()
@click.option("--style", type=str, default="default")
@click.pass_context
def highlight_info(ctx, style):
    """Outputs the CSS which can be customized for highlighted code"""
    click.secho("The following styles are available to choose from:", fg="green")
    click.echo(list(pygments.styles.get_all_styles()))
    click.echo()
    click.secho(
        f'The following CSS for the "{style}" style can be customized:', fg="green"
    )
    click.echo(pygments.formatters.HtmlFormatter(style=style).get_style_defs())


# @cli.command()
# @click.pass_context
# def check(ctx):
#     combine = ctx.invoke(build, no_checks=True)  # should it build?
#     runner = CheckRunner(combine)
#     runner.run()
#     if runner.succeeded:
#         click.secho('All checks passed!', fg='green')
#     else:
#         click.secho('Checks failed.', fg='red')
#         for check in runner.failed_checks:
#             click.echo(check)
#         exit(1)


if __name__ == "__main__":
    cli()


# Want to make it as easy and friendly as possible, hard to screw up
# pretty print output html? or don't want to screw with js, etc.
# validate html
# check "output" in .gitignore (if git) -- use warning codes FW101
# asset pipeline (asset fingerprinting - hash)

# rel canonical?

# build in pre-commit hook helper -- you don't have a pre-commit hook, do you want one?
# then it runs check command before commit (not on every run if costly)

# no links to same page (empty links too)
