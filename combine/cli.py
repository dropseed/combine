import os

import click

from .core import Combine
from .checks import checks
from .dev import Watcher, Server


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
def build(ctx):
    content_paths = [
        os.path.abspath('content'),
        os.path.abspath(os.path.join('theme', 'content')),
    ]

    output_path = os.path.abspath('output')

    config_path = os.path.abspath('combine.yml')

    combine = Combine(
        config_path=config_path,
        content_paths=content_paths,
        output_path=output_path,
    )

    click.secho('Building site', fg='cyan')
    combine.clean_and_build()

    return combine


@cli.command()
@click.pass_context
def work(ctx):
    combine = ctx.invoke(build)

    click.secho('Watching for file changes...', fg='green')

    server = Server(combine.output_path)
    watcher = Watcher('.', combine=combine)
    watcher.watch(server.serve)


@cli.command()
@click.pass_context
def check(ctx):
    combine = ctx.invoke(build)

    for check in checks:
        check(combine).run()


if __name__ == '__main__':
    cli()


# Want to make it as easy and friendly as possible, hard to screw up
# pretty print output html? or don't want to screw with js, etc.
# validate html
# check "output" in .gitignore (if git) -- use warning codes FW101
# asset pipeline (asset fingerprinting - hash)

# redirects
# → curl https://help.github.com/articles/creating-an-issue-template-for-your-repository/
# <!DOCTYPE html>
# <html>
# <head>
# <meta charset=utf-8>
# <title>Redirecting...</title>
# <link rel=canonical href="/articles/manually-creating-a-single-issue-template-for-your-repository/">
# <meta http-equiv=refresh content="0; url=/articles/manually-creating-a-single-issue-template-for-your-repository/">
# <h1>Redirecting...</h1>
# <a href="/articles/manually-creating-a-single-issue-template-for-your-repository/">Click here if you are not redirected.</a>
# <script>location='/articles/manually-creating-a-single-issue-template-for-your-repository/'</script>
# </body>
# </html>

# rel canonical?

# build in pre-commit hook helper -- you don't have a pre-commit hook, do you want one?
# then it runs check command before commit (not on every run if costly)

# no links to same page (empty links too)
