import os
import glob

from bs4 import BeautifulSoup

from .core import Check, Message
from .registry import register


@register
class PageTitlesCheck(Check):
    def run(self):
        messages = []
        page_titles = {}

        ignored_titles = ["Redirecting..."]

        for path in glob.iglob(
            os.path.join(self.combine.output_path, "**", "*.html"), recursive=True
        ):
            with open(path, "r") as f:
                soup = BeautifulSoup(f, "html.parser")
                title = soup.title
                if title:
                    if title.string in ignored_titles:
                        continue

                    if title.string in page_titles:
                        page_titles[title.string].append(path)
                    else:
                        page_titles[title.string] = [path]
                else:
                    messages.append(
                        Message(
                            "Page title is missing",
                            "seo.E001",
                            hint="Add a <title> in <head>",
                            object=path,
                        )
                    )

        for title, paths in page_titles.items():
            if len(paths) > 1:
                messages.append(
                    Message(
                        "Duplicate page title",
                        "seo.W001",
                        hint="Change the <title> attribute",
                        object=paths,
                    )
                )

            if len(title) > 60:
                messages.append(
                    Message(
                        "Long page title",
                        "seo.W002",
                        hint="Make the title shorter. https://moz.com/learn/seo/title-tag",
                        object=paths,
                    )
                )

        # TODO put brand at the end? Check if lots of titles start with the same thing and warn to move it to the end...

        return messages


@register
class AltTextCheck(Check):
    def run(self):
        messages = []

        for path in glob.iglob(
            os.path.join(self.combine.output_path, "**", "*.html"), recursive=True
        ):
            with open(path, "r") as f:
                soup = BeautifulSoup(f, "html.parser")
                for img in soup.findAll("img"):
                    if img.attrs.get("alt", None) is None:
                        messages.append(
                            Message(
                                "Alt text missing on img",
                                "seo.E002",
                                hint=f"Add alt attribute to img tag",
                                object=(img, path),
                            )
                        )

        return messages
