import os
import glob

from bs4 import BeautifulSoup

from .core import Check, Message
from .registry import register


@register
class PageTitlesCheck(Check):
    """Ensures that the output directory actually has files in it"""
    def run(self):
        messages = []
        page_titles = {}

        for path in glob.iglob(os.path.join(self.combine.output_path, '**', '*.html'), recursive=True):
            with open(path, 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
                title = soup.title
                if title:
                    if title.string in page_titles:
                        page_titles[title.string].append(path)
                    else:
                        page_titles[title.string] = [path]
                else:
                    messages.append(Message('Page title is missing', 'seo.E001', hint='Add a <title> in <head>', object=path))

        for title, paths in page_titles.items():
            if len(paths) > 1:
                messages.append(Message('Duplicate page title', 'seo.W001', hint='Change the <title> attribute', object=paths))

            if len(title) > 60:
                messages.append(Message('Long page title', 'seo.W002', hint='Make the title shorter. https://moz.com/learn/seo/title-tag', object=paths))

        # TODO put brand at the end? Check if lots of titles start with the same thing and warn to move it to the end...

        return messages
