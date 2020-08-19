from urllib.parse import urlparse
from jinja2 import contextfilter
from .exceptions import MissingVariableError


@contextfilter
def absolute_url(ctx, value):
    try:
        base_url = ctx["base_url"]
    except KeyError:
        raise MissingVariableError("base_url")

    # TODO any way to use jinja error and point to line number etc?

    if not base_url:
        raise Exception("absolute_url error: base_url can't be empty")

    if not value:
        raise Exception("absolute_url error: url argument can't be empty")

    if base_url.endswith("/") and value.startswith("/"):
        url = base_url + value.lstrip("/")

    if not base_url.endswith("/") and not value.startswith("/"):
        url = base_url + "/" + value

    url = base_url + value

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise Exception(f"absolute_url error: absolute url doesn't look valid\n{url}")

    return url
