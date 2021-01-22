import os

from bs4 import BeautifulSoup

from ..jinja.references import get_references_in_path
from .core import File
from .utils import create_parent_directory
from ..checks.duplicate_id import DuplicateIDCheck
from ..checks.mixed_content import MixedContentCheck
from ..checks.img_alt import ImgAltCheck
from ..checks.meta import MetaDescriptionCheck
from ..checks.title import TitleCheck
from ..checks.links import InternalLinkBrokenCheck
from ..checks.open_graph import (
    OpenGraphTitleCheck,
    OpenGraphDescriptionCheck,
    OpenGraphTypeCheck,
    OpenGraphURLCheck,
    OpenGraphImageCheck,
    OpenGraphSiteNameCheck,
)


class HTMLFile(File):
    def _get_output_relative_path(self):
        if self.name_without_extension.endswith(".keep"):
            # remove .keep.html from the end and replace with .html
            return super()._get_output_relative_path()[:-10] + ".html"

        if self.name_without_extension == "index":
            return super()._get_output_relative_path()

        return os.path.join(*self.root_parts, "index.html")

    def _render_to_output(self, output_path, jinja_environment):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        template = jinja_environment.get_template(self.content_relative_path)

        with open(target_path, "w+") as f:
            f.write(template.render(url=self._get_url()))

        self.references = get_references_in_path(self.path, jinja_environment)

        return target_path

    def _get_url(self):
        url = "/" + self.output_relative_path
        if url.endswith("/index.html"):
            url = url[:-10]
        return url

    def get_checks(self):
        with open(self.output_path, "r") as f:
            html_soup = BeautifulSoup(f.read(), "html.parser")

            return super().get_checks() + [
                DuplicateIDCheck(html_soup=html_soup),
                MixedContentCheck(html_soup=html_soup),
                ImgAltCheck(html_soup=html_soup),
                MetaDescriptionCheck(html_soup=html_soup),
                TitleCheck(html_soup=html_soup),
                OpenGraphTitleCheck(html_soup=html_soup),
                OpenGraphDescriptionCheck(html_soup=html_soup),
                OpenGraphTypeCheck(html_soup=html_soup),
                OpenGraphURLCheck(html_soup=html_soup),
                OpenGraphImageCheck(html_soup=html_soup),
                OpenGraphSiteNameCheck(html_soup=html_soup),
                InternalLinkBrokenCheck(
                    html_soup=html_soup,
                    file_path=self.output_path,
                    # reverse engineer the output dir for now
                    output_dir=self.output_path[: -len(self.output_relative_path)],
                ),
            ]
