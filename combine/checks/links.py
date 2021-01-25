import os
from urllib.parse import urljoin

from .base import Check
from .issues import Issues, Issue


class InternalLinkBrokenCheck(Check):
    def __init__(self, html_soup, file_path, output_dir):
        self.html_soup = html_soup
        self.file_path = file_path
        self.output_dir = output_dir

    def run(self):
        issues = Issues()

        types = {
            "img": "src",
            "script": "src",
            "a": "href",
            "link": "href",
        }

        skip_prefixes = (
            "//",
            "http:",
            "https:",
            "tel:",
            "mailto:",
            "ftp:",
            "file:",
            "#",
        )

        for nodeType, nodeAttribute in types.items():
            for node in self.html_soup.findAll(nodeType):
                value = node.get(nodeAttribute)

                if value:
                    # Remove whitespace on both ends
                    value = value.strip()

                if value and "?" in value:
                    # Remove query params too (style.css?v=1.0)
                    value = value.split("?")[0]

                if not value:
                    # Skip empty ones for now, not our responsibility
                    continue

                should_skip = False

                for p in skip_prefixes:
                    if value.startswith(p):
                        should_skip = True
                        break

                if should_skip:
                    continue

                if value.startswith("/"):
                    # remove the leading / and join to output_dir
                    output_path = urljoin(self.output_dir, value[1:])
                else:
                    output_path = urljoin(self.file_path, value)

                _, ext = os.path.splitext(output_path)
                if not ext:
                    # If it's a directory, pretend we're a webserver and
                    # look for index.html
                    if not output_path.endswith("/"):
                        output_path += "/"
                    output_path = urljoin(output_path, "index.html")

                # TODO if not in output_dir, that's an error ("../../../ that takes you out of combine")

                if not os.path.exists(output_path):
                    issues.append(
                        Issue(
                            type="internal-link-broken",
                            description="You have a link that doesn't point to an existing file.",
                            context={
                                "element": str(node),
                                "target_path": os.path.relpath(output_path),
                            },
                        )
                    )

        return issues
