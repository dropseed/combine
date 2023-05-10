import logging
import os
import sys
from typing import List

import click
import pygments
import barrel
from honcho.manager import Manager as HonchoManager
from honcho.printer import Printer as HonchoPrinter
from repaint import Repaint

from .core import Combine
from .logger import logger
from .dev import Watcher, Server
from .exceptions import BuildError
from . import __version__


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    pass


@cli.command()
@click.option("--check", is_flag=True, default=False)
@click.option("--env", default="production")
@click.option("--var", multiple=True, default=[])
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def build(
    ctx: click.Context, check: bool, env: str, var: List[str], debug: bool
) -> None:
    """Build the site (typically during deployment)"""
    if debug:
        logger.setLevel(logging.DEBUG)

    variables = dict(x.split("=") for x in var)
    config_path = os.path.abspath("combine.yml")
    combine = Combine(config_path=config_path, env=env, variables=variables)

    click.secho("Building site", bold=True, color=True)
    try:
        combine.build(check=check)
    except BuildError:
        click.secho("Build error (see above)", fg="red", color=True)
        exit(1)

    if check:
        if combine.issues:
            click.secho(
                f"{len(combine.issues)} check{'s' if len(combine.issues) > 1 else ''} failed",
                fg="red",
                color=True,
            )
            exit(1)
        else:
            click.secho("✓ All checks passed", fg="green", color=True)


@cli.command()
@click.option("--port", type=int, default=8000)
@click.option("--debug", is_flag=True, default=False)
@click.option("--repaint", is_flag=True, default=True)
@click.pass_context
def work(ctx: click.Context, port: int, debug: bool, repaint: bool) -> None:
    """Start a local server to build the site while you work"""
    if debug:
        logger.setLevel(logging.DEBUG)

    config_path = os.path.abspath("combine.yml")
    combine = Combine(
        config_path=config_path,
        env="development",
        variables={"base_url": f"http://127.0.0.1:{port}"},
    )
    click.secho("Building site", bold=True, color=True)
    try:
        combine.build(check=True)
    except BuildError:
        click.secho("Build error (see above)", fg="red", color=True)
        exit(1)

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

    click.secho(header, fg="green", bold=True, color=True)

    debug_flag = "--debug" if debug else ""
    repaint_flag = "--repaint" if repaint else ""

    bin_path = os.path.dirname(sys.executable)
    combine_path = os.path.join(bin_path, "combine")
    honcho_env = {
        **os.environ,
        "PYTHONUNBUFFERED": "1",
    }

    manager = HonchoManager(HonchoPrinter())
    manager._system_print = lambda x: None
    manager.add_process(
        "server",
        f"{combine_path} utils server --port {port} {debug_flag} {repaint_flag}",
        env=honcho_env,
    )
    manager.add_process(
        "combine",
        f"{combine_path} utils watch --port {port} {debug_flag} {repaint_flag}",
        env=honcho_env,
    )

    if repaint:
        manager.add_process(
            "repaint",
            f"{os.path.join(bin_path, 'repaint')} serve {'--quiet' if not debug else ''}",
            env=honcho_env,
        )

    # Add additional custom watch processes
    process_names = set()
    for i, step in enumerate(combine.config.steps):
        if step.has_watch_process:
            name = step.get_name() or f"step-{i}"
            if name in process_names:
                # Can get an error for duplicate process names
                # (ex. tailwindcss)
                name = f"{name}-{i}"

            process_names.add(name)
            manager.add_process(
                name,
                step.watch,
            )

    manager.loop()


@cli.group()
@click.pass_context
def utils(ctx: click.Context) -> None:
    """Utility commands"""
    pass


@utils.command()
@click.option("--port", type=int, default=8000)
@click.option("--debug", is_flag=True, default=False)
@click.option("--repaint", is_flag=True, default=False)
@click.pass_context
def server(ctx: click.Context, port: int, debug: bool, repaint: bool) -> None:
    if debug:
        logger.setLevel(logging.DEBUG)

    config_path = os.path.abspath("combine.yml")
    combine = Combine(
        config_path=config_path,
        env="development",
        variables={"base_url": f"http://127.0.0.1:{port}"},
    )

    Server(combine.output_path, Repaint() if repaint else None, port).serve()


@utils.command()
@click.option("--port", type=int, default=8000)
@click.option("--debug", is_flag=True, default=False)
@click.option("--repaint", is_flag=True, default=False)
@click.pass_context
def watch(ctx: click.Context, port: int, debug: bool, repaint: bool) -> None:
    if debug:
        logger.setLevel(logging.DEBUG)

    config_path = os.path.abspath("combine.yml")
    combine = Combine(
        config_path=config_path,
        env="development",
        variables={"base_url": f"http://127.0.0.1:{port}"},
    )

    Watcher(
        ".", combine=combine, repaint=Repaint() if repaint else None, debug=debug
    ).watch()


@utils.command()
@click.option(
    "--style",
    default="default",
    show_default=True,
    type=click.Choice(list(pygments.styles.get_all_styles())),
)
@click.pass_context
def highlight_css(ctx: click.Context, style: str) -> None:
    """Outputs the CSS which can be customized for highlighted code"""
    for line in (
        pygments.formatters.HtmlFormatter(style=style).get_style_defs().splitlines()
    ):
        click.echo(f".highlight {line}")


@cli.command()
def update() -> None:
    """Update your version of combine"""
    barrel.update("combine")


if __name__ == "__main__":
    cli()
