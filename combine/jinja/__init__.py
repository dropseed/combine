from .code import CodeHighlightExtension
from .markdown import MarkdownExtension, markdown_filter
from .include_raw import IncludeRawExtension
from .urls import absolute_url


default_extensions = [CodeHighlightExtension, MarkdownExtension, IncludeRawExtension]
default_filters = {
    "absolute_url": absolute_url,
    "markdown": markdown_filter,
}
