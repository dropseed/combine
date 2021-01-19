from bs4 import BeautifulSoup

from combine.checks.img_alt import ImgAltCheck


def test_img_alt_check(snapshot):
    content = """<!doctype html>
<html>
    <head>
    </head>
    <body>
        <img>
        <img alt="">
        <img alt="test">
    </body>
</html>"""
    check = ImgAltCheck(BeautifulSoup(content, "html.parser"))
    issues = check.run()
    snapshot.assert_match(issues.as_data())
