import os
import json

import click
import pygments

from .core import Combine
from .dev import Watcher, Server
from .exceptions import BuildError


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option("--env", default="production")
@click.option("--var", multiple=True, default=[])
@click.pass_context
def build(ctx, env, var):
    variables = dict(x.split("=") for x in var)
    config_path = os.path.abspath("combine.yml")
    combine = Combine(config_path=config_path, env=env, variables=variables)

    click.secho("Building site", fg="cyan")
    try:
        combine.build()
    except BuildError:
        click.secho("Build error (see above)", fg="red")
        exit(1)

    return combine


@cli.command()
@click.option("--port", type=int, default=8000)
@click.pass_context
def work(ctx, port):
    combine = ctx.invoke(
        build, env="development", var=[f"base_url=http://127.0.0.1:{port}"]
    )

    click.secho("Watching for file changes...", fg="green")

    server = Server(combine.output_path, port)
    watcher = Watcher(".", combine=combine)
    watcher.watch(server.serve)


@cli.group()
@click.pass_context
def utils(ctx):
    pass


@utils.command()
@click.option(
    "--style",
    default="default",
    show_default=True,
    type=click.Choice(list(pygments.styles.get_all_styles())),
)
@click.pass_context
def highlight_css(ctx, style):
    """Outputs the CSS which can be customized for highlighted code"""
    for line in (
        pygments.formatters.HtmlFormatter(style=style).get_style_defs().splitlines()
    ):
        click.echo(f".highlight {line}")


if __name__ == "__main__":
    cli()
