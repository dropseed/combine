import bs4

from .base import Check
from .issues import Issues, Issue


class MixedContentCheck(Check):
    def __init__(self, html_soup: bs4.BeautifulSoup) -> None:
        self.html_soup = html_soup

    def run(self) -> Issues:
        issues = Issues()

        to_check = {
            "img": {"attr": "src"},
            "link": {"attr": "href", "ignore": {"rel": "profile"}},
            "iframe": {"attr": "src"},
            # TODO missing script? but src needs to be optional (could be inline)
        }

        for tag, cfg in to_check.items():
            for el in self.html_soup.findAll(tag):
                if any(
                    [
                        el.get(k, [None])[0] == v
                        for k, v in cfg.get("ignore", {}).items()  # type: ignore
                    ]
                ):
                    continue

                attr = cfg["attr"]  # type: ignore

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
