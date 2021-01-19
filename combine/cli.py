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
@click.option("--check", is_flag=True, default=False)
@click.option("--env", default="production")
@click.option("--var", multiple=True, default=[])
@click.pass_context
def build(ctx, check, env, var):
    variables = dict(x.split("=") for x in var)
    config_path = os.path.abspath("combine.yml")
    combine = Combine(config_path=config_path, env=env, variables=variables)

    click.secho("❯ Building site", bold=True)
    try:
        combine.build(check=check)
    except BuildError:
        click.secho("Build error (see above)", fg="red")
        exit(1)

    if check:
        if combine.issues:
            click.secho(
                f"{len(combine.issues)} check{'s' if len(combine.issues) > 1 else ''} failed",
                fg="red",
            )
            exit(1)
        else:
            click.secho("✓ All checks passed", fg="green")


@cli.command()
@click.option("--port", type=int, default=8000)
@click.pass_context
def work(ctx, port):
    config_path = os.path.abspath("combine.yml")
    combine = Combine(
        config_path=config_path,
        env="development",
        variables={"base_url": f"http://127.0.0.1:{port}"},
    )
    click.secho("❯ Building site", bold=True)
    try:
        combine.build(check=True)
    except BuildError:
        click.secho("Build error (see above)", fg="red")

    server = Server(combine.output_path, port)
    watcher = Watcher(".", combine=combine)

    header = (
        """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      ┏━━━━━┓                                               ┃
┃      ┗┓   ┏┻━━━┓    Site is live: http://127.0.0.1:%s    ┃
┃    ┏━━┫   ┣━━┓ ┃                                           ┃
┃    ┃ ┏┻━━━┻┓ ┃      Docs: https://combine.dropseed.io      ┃
┃ ┏━━┻━┻━━━━━┻━┻━━┓                                          ┃
┃ ┣━━━━━━━━━━━━━━━┫   Watching for file changes...           ┃
┃ ┗━━━━◡◡━━━◡◡━━━━┛                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
        % port
    )

    click.secho(header, fg="green", bold=True)

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
