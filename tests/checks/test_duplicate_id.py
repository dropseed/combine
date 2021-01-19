from bs4 import BeautifulSoup

from combine.checks.duplicate_id import DuplicateIDCheck


def test_duplicate_id_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
    </head>
    <body>
        <img id="foo" src="https://example.com/image.png">
        <div id="foo"></div>
        <div id="bar"></div>
    </body>
</html>"""
    check = DuplicateIDCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())
