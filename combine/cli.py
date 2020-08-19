import os
import json

import click
import pygments

from .core import Combine
from .dev import Watcher, Server


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
    combine.build()

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


if __name__ == "__main__":
    cli()
