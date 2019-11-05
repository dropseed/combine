import os
import sys
from subprocess import run

import click
import pygments
import babel

from .core import Combine
from .dev import Watcher, Server


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option("--env", default="production")
@click.pass_context
def build(ctx, env):
    config_path = os.path.abspath("combine.yml")
    combine = Combine(config_path=config_path, env=env)

    click.secho("Building site", fg="cyan")
    combine.build()

    return combine


@cli.command()
@click.option("--port", type=int, default=8000)
@click.pass_context
def work(ctx, port):
    combine = ctx.invoke(build, env="development")

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


@utils.command()
@click.pass_context
def extract_translations(ctx):
    """Generates .po files for all found languages"""
    combine = ctx.invoke(build, env="development")
    locales = set()
    for file in combine.iter_files():
        if file.locale:
            locales.add(file.locale)

    if not locales:
        click.secho("No locales found", fg="red")
        exit(1)

    click.echo(f"Found {len(locales)} locales")
    for locale in locales:
        click.echo(f"- {locale}")
    click.echo()

    pybabel = os.path.join(os.path.dirname(sys.executable), "pybabel")
    pybabel_cfg = os.path.join(os.path.dirname(__file__), "babel.cfg")

    if not click.confirm("This will overwrite any existing .po files. Continue?"):
        return

    for locale in locales:
        paths = [os.path.relpath(x.path) for x in combine.content_directories]

        click.echo(f"Extracting {locale}")
        output_path = os.path.join(
            combine.locale_path,
            str(locale),
            "LC_MESSAGES",
            f"{combine.locale_domain}.po",
        )

        if not os.path.exists(output_path):
            # extract to a new path
            # update the old path using it
            # remove the new path and keep the updated old one
            # run([pybabel, "update", "-D", combine.locale_domain, "-l", str(locale), "-i", output_path, "-o", output_path, "--omit-header"] + paths, check=True)
            # else:
            os.makedirs(os.path.dirname(output_path))
        run(
            [pybabel, "extract", "-F", pybabel_cfg, "-o", output_path, "--omit-header"]
            + paths,
            check=True,
        )

    run(
        [pybabel, "compile", "-d", combine.locale_path, "--statistics", "--use-fuzzy"],
        check=True,
    )


if __name__ == "__main__":
    cli()
