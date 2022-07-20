from jinja2 import nodes, BaseLoader
from jinja2.parser import Parser
from jinja2.ext import Extension
from markupsafe import Markup


class IncludeRawExtension(Extension):
    tags = {"include_raw"}

    def parse(self, parser: Parser) -> nodes.Node:
        lineno = parser.stream.expect("name:include_raw").lineno
        template = parser.parse_expression()
        result = self.call_method("_render", [template], lineno=lineno)
        return nodes.Output([result], lineno=lineno)

    def _render(self, filename: str) -> Markup:
        source = self.environment.loader.get_source(self.environment, filename)  # type: ignore
        return Markup(source[0])
