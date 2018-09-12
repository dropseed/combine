from jinja2 import nodes
from jinja2.ext import Extension

import markdown


class MarkdownExtension(Extension):
    tags = set(['markdown'])

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endmarkdown'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_support'),
                               [], [], body).set_lineno(lineno)

    def _support(self, caller):
        """Helper callback."""
        markdown_content = caller()
        html_content = markdown.markdown(markdown_content)
        return html_content
