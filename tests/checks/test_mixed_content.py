from bs4 import BeautifulSoup

from combine.checks.mixed_content import MixedContentCheck


def test_duplicate_id_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
        <link rel="profile" href="http://gmpg.org/xfn/11">

        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="http://another.com/style.css">
    </head>
    <body>
        <img src="https://example.com/image.png">
        <img src="http://example.com/image.png">

        <iframe src="https://external.com">
        <iframe src="http://external.com">
    </body>
</html>"""
    check = MixedContentCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())
