from bs4 import BeautifulSoup

from combine.checks.title import TitleCheck


def test_title_empty_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <title></title>
    </head>
    <body>
    </body>
</html>"""
    check = TitleCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())


def test_title_missing_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
    </head>
    <body>
    </body>
</html>"""
    check = TitleCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())


def test_title_ok_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <title>This is a page title</title>
    </head>
    <body>
    </body>
</html>"""
    check = TitleCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())
