from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup


class IncludeRawExtension(Extension):
    tags = {"include_raw"}

    def parse(self, parser):
        lineno = parser.stream.expect("name:include_raw").lineno
        template = parser.parse_expression()
        result = self.call_method("_render", [template], lineno=lineno)
        return nodes.Output([result], lineno=lineno)

    def _render(self, filename):
        return Markup(self.environment.loader.get_source(self.environment, filename)[0])
