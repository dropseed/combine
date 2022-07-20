from typing import Any, Callable
from jinja2 import nodes, pass_context
from jinja2.parser import Parser
from jinja2.ext import Extension
from markupsafe import Markup

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension


class MarkdownExtension(Extension):
    tags = set(["markdown"])

    def parse(self, parser: Parser) -> nodes.Node:
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(("name:endmarkdown",), drop_needle=True)
        return nodes.CallBlock(self.call_method("_support"), [], [], body).set_lineno(
            lineno
        )

    def _support(self, caller: Callable) -> str:
        """Helper callback."""
        markdown_content = caller()
        # jinja will have escaped by default, so we want to unescape
        # for now and leave that to markdown rendering
        markdown_content = Markup(markdown_content).unescape()
        return markdown_to_html(markdown_content)


@pass_context
def markdown_filter(ctx: dict, value: str) -> Markup:
    html_content = markdown_to_html(value)
    return Markup(html_content)


def markdown_to_html(markdown_content: str) -> str:
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
