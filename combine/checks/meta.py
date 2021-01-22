from .base import Check
from .issues import Issues, Issue


class MetaDescriptionCheck(Check):
    def __init__(self, html_soup):
        self.html_soup = html_soup

    def run(self):
        issues = Issues()

        meta = self.html_soup.find("meta", {"name": "description"})
        if not meta:
            # missing meta is fine for google, except for social if no og:description (checked elsewhere)
            return issues

        description = meta.get("content", "")
        if not description:
            issues.append(
                Issue(
                    type="meta-description-empty",
                    description="The meta description tag is present, but has an empty value.",
                    context={"element": str(meta)},
                )
            )
            return issues

        if len(description) < 50 or len(description) > 320:
            issues.append(
                Issue(
                    type="meta-description-length",
                    description="The meta description text should be between 50 and 320 characters.",
                    context={"length": len(description), "description": description},
                )
            )

        return issues
