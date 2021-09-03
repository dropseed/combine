import os

import click
import pygments
import cls_client

from .core import Combine
from .dev import Watcher, Server
from .exceptions import BuildError
from . import __version__


cls_client.set_project_key("cls_pk_QFp5bJFR1RXauHdvRUDpDngE")
cls_client.set_project_slug("combine")
cls_client.set_version(__version__)
cls_client.set_noninteractive_tracking_enabled(True)


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit.")
@click.pass_context
def cli(ctx, version):
    if not ctx.invoked_subcommand:
        if version:
            click.echo(__version__)
        else:
            click.echo(ctx.get_help())


@cli.command()
@click.option("--check", is_flag=True, default=False)
@click.option("--env", default="production")
@click.option("--var", multiple=True, default=[])
@click.pass_context
@cls_client.track_command(
    include_kwargs=["check", "env"],
    include_env=["NETLIFY", "CIRCLECI", "TRAVIS", "GITLAB_CI", "GITHUB_ACTIONS", "CI"],
)
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
@cls_client.track_command()
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
┃    ┃ ┏┻━━━┻┓ ┃      Docs: https://combine.dropseed.dev     ┃
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
@cls_client.track_command(include_kwargs=["style"])
def highlight_css(ctx, style):
    """Outputs the CSS which can be customized for highlighted code"""
    for line in (
        pygments.formatters.HtmlFormatter(style=style).get_style_defs().splitlines()
    ):
        click.echo(f".highlight {line}")


if __name__ == "__main__":
    cli()
