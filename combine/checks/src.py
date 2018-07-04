import os
import glob

from bs4 import BeautifulSoup

from .core import Check, Message
from .registry import register


@register
class SrcCheck(Check):
    def run(self):
        messages = []

        # a href
        # img src
        # link href
        # script src

        # if inside site, check file exists
        # if remote, check exists too?
        # if empty, error (except script with content)

        # for path in glob.iglob(os.path.join(self.combine.output_path, '**', '*.html'), recursive=True):
        #     with open(path, 'r') as f:
        #         soup = BeautifulSoup(f, 'html.parser')
        #         for img in soup.findAll('img'):
        #             if not img.attrs.get('alt', ''):
        #                 messages.append(Message('Alt text missing on img', 'seo.E002', hint=f'Add alt attribute to img tag', object=(img, path)))

        return messages
