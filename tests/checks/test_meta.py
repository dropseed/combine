from bs4 import BeautifulSoup

from combine.checks.meta import MetaDescriptionCheck


def test_meta_description_empty_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <meta name="description" />
    </head>
    <body>
    </body>
</html>"""
    check = MetaDescriptionCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())


def test_meta_description_length_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <meta name="description" content="Whoops" />
    </head>
    <body>
    </body>
</html>"""
    check = MetaDescriptionCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())
