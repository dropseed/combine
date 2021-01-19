import os

from .base import Check
from .issues import Issues, Issue


class FaviconCheck(Check):
    def __init__(self, site_dir):
        self.site_dir = site_dir

    def run(self):
        issues = Issues()

        if not os.path.exists(os.path.join(self.site_dir, "favicon.ico")):
            issues.append(
                Issue(
                    type="favicon-missing",
                    description="Your site should have a Favicon at /favicon.ico.",
                )
            )

        return issues
