from .base import Check
from .issues import Issues, Issue


class ImgAltCheck(Check):
    def __init__(self, html_soup):
        self.html_soup = html_soup

    def run(self):
        issues = Issues()

        for img in self.html_soup.findAll("img"):
            alt = img.get("alt")
            if alt is None:
                issues.append(
                    Issue(
                        type="image-alt-missing",
                        description="All <img> tags should have alt text describing the image, or be set to an empty string (`"
                        "`)",
                        context={"element": str(img)},
                    )
                )

        return issues
