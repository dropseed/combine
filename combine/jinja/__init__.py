from .code import CodeHighlightExtension
from .markdown import MarkdownExtension
from .urls import absolute_url


default_extensions = [CodeHighlightExtension, MarkdownExtension]
default_filters = {
    "absolute_url": absolute_url,
}
