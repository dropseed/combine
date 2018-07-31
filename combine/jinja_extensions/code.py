from jinja2 import nodes
from jinja2.ext import Extension

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


class CodeHighlightExtension(Extension):
    tags = set(['code'])

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcode'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_code_support', args),
                               [], [], body).set_lineno(lineno)

    def _code_support(self, language, caller):
        """Helper callback."""
        code = caller()

        if language:
            lexer = get_lexer_by_name(language, stripall=True)
        else:
            lexer = guess_lexer(code)

        highlighted = highlight(code, lexer, HtmlFormatter())

        return highlighted
