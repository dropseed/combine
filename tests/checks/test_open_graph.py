from bs4 import BeautifulSoup

from combine.checks.open_graph import (
    OpenGraphTitleCheck,
    OpenGraphDescriptionCheck,
    OpenGraphTypeCheck,
    OpenGraphURLCheck,
    OpenGraphImageCheck,
    OpenGraphSiteNameCheck,
)


def test_open_graph_missing_checks(snapshot):
    content = """<!doctype html>
<html>
    <head>
    </head>
    <body>
    </body>
</html>"""
    soup = BeautifulSoup(content, "html.parser")

    check_classes = (
        OpenGraphTitleCheck,
        OpenGraphDescriptionCheck,
        OpenGraphTypeCheck,
        OpenGraphURLCheck,
        OpenGraphImageCheck,
        OpenGraphSiteNameCheck,
    )

    for check_class in check_classes:
        check = check_class(soup)
        issues = check.run()
        snapshot.assert_match(issues.as_data())


def test_open_graph_url_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <meta property="og:url" content="/page" />
    </head>
    <body>
    </body>
</html>"""
    check = OpenGraphURLCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())


def test_open_graph_url_check_invalid(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <meta property="og:url" content="https:///" />
    </head>
    <body>
    </body>
</html>"""
    check = OpenGraphURLCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    assert len(issues) > 0
    snapshot.assert_match(issues.as_data())


def test_open_graph_image_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <meta property="og:image" content="/page" />
    </head>
    <body>
    </body>
</html>"""
    check = OpenGraphImageCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())
