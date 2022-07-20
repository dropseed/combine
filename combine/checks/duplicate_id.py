from typing import Dict, List
from .base import Check
from .issues import Issues, Issue
import bs4


class DuplicateIDCheck(Check):
    def __init__(self, html_soup: bs4.BeautifulSoup) -> None:
        self.html_soup = html_soup

    def run(self) -> Issues:
        issues = Issues()

        ids_seen: Dict[str, List[bs4.element.Tag]] = {}

        for el in self.html_soup.findAll():
            id = el.get("id")
            if not id:
                continue

            if id in ids_seen:
                ids_seen[id].append(el)
            else:
                ids_seen[id] = [el]

        for id, elements in ids_seen.items():
            if len(elements) > 1:
                issues.append(
                    Issue(
                        type="duplicate-id",
                        description="The same `id` should not be used on a page more than once.",
                        context={"id": id, "elements": [str(x) for x in elements]},
                    )
                )

        return issues
