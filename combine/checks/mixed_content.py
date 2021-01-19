from urllib.parse import urljoin

from .base import Check
from .issues import Issues, Issue


class MixedContentCheck(Check):
    def __init__(self, html_soup):
        self.html_soup = html_soup

    def run(self):
        issues = Issues()

        to_check = {
            "img": {"attr": "src"},
            "link": {"attr": "href", "ignore": {"rel": "profile"}},
            "iframe": {"attr": "src"},
        }

        for type, cfg in to_check.items():
            for el in self.html_soup.findAll(type):
                if any(
                    [
                        el.get(k, [None])[0] == v
                        for k, v in cfg.get("ignore", {}).items()
                    ]
                ):
                    continue

                attr = cfg["attr"]

                value = el.get(attr)

                if value.startswith("http:"):
                    issues.append(
                        Issue(
                            type="https-mixed-content",
                            description="Any linked resources (CSS, img, iframes) should be linked via HTTPS.",
                            context={"element": str(el)},
                        )
                    )

        return issues
