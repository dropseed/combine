from jinja2 import nodes
from jinja2.ext import Extension
from jinja2 import Markup

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension


class MarkdownExtension(Extension):
    tags = set(["markdown"])

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(["name:endmarkdown"], drop_needle=True)
        return nodes.CallBlock(self.call_method("_support"), [], [], body).set_lineno(
            lineno
        )

    def _support(self, caller):
        """Helper callback."""
        markdown_content = caller()
        # jinja will have escaped by default, so we want to unescape
        # for now and leave that to markdown rendering
        markdown_content = Markup(markdown_content).unescape()
        html_content = markdown.markdown(
            markdown_content,
            extensions=[
                "markdown.extensions.fenced_code",
                CodeHiliteExtension(css_class="highlight"),
                "markdown.extensions.tables",
                "markdown.extensions.toc",
            ],
        )
        return html_content
