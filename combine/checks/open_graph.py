import bs4
from urllib.parse import urlparse

from .base import Check
from .issues import Issues, Issue


def url_is_valid_absolute(url: str) -> bool:
    parsed = urlparse(url)

    if parsed.netloc.startswith("127.0.0.1"):
        # TODO ideally this would only be allowed in local development
        # https not required
        return True

    if not parsed.netloc:
        # domain missing, probably broken url like "https:///"
        return False

    if parsed.scheme != "https":
        # must be https
        return False

    return True


class BaseOpenGraphCheck(Check):
    og_property = ""

    def __init__(self, html_soup: bs4.BeautifulSoup) -> None:
        self.html_soup = html_soup

    def run(self) -> Issues:
        issues = Issues()

        meta = self.html_soup.find("meta", {"property": f"og:{self.og_property}"})
        self.meta_tag_content = meta.get("content", "") if meta else ""
        if not self.meta_tag_content:
            property_slug = self.og_property.replace("_", "-")
            issues.append(
                Issue(
                    type=f"open-graph-{property_slug}-missing",
                    description=f"The og:{property_slug} meta tag is missing.",
                )
            )

        return issues


class OpenGraphTitleCheck(BaseOpenGraphCheck):
    og_property = "title"


class OpenGraphDescriptionCheck(BaseOpenGraphCheck):
    og_property = "description"

    def run(self) -> Issues:
        issues = super().run()
        meta = self.html_soup.find("meta", {"name": "description"})
        if meta and meta.get("content", ""):
            # if there is a meta description, that is a fine alternative
            # to the more specific og:description
            issues = Issues()
        return issues


class OpenGraphTypeCheck(BaseOpenGraphCheck):
    og_property = "type"


class OpenGraphURLCheck(BaseOpenGraphCheck):
    og_property = "url"

    def run(self) -> Issues:
        issues = super().run()

        url = self.meta_tag_content

        if url:
            # try:
            #     response = fetch.head(url)
            #     if response.status_code != 405:
            #         # just skip for now if HEAD not allowed
            #         response.raise_for_status()
            # except Exception as e:
            #     issues.append(
            #         Issue(
            #             type="open-graph-url-broken",

            #             context={"exception": str(e)},
            #         )
            #     )

            if not url_is_valid_absolute(url):
                issues.append(
                    Issue(
                        type="open-graph-url-not-canonical-https",
                        description="The og:url should be an absolute, HTTPS url.",
                        context={"content": url},
                    )
                )

        return issues


class OpenGraphImageCheck(BaseOpenGraphCheck):
    og_property = "image"

    def run(self) -> Issues:
        issues = super().run()

        url = self.meta_tag_content

        if url:
            # try:
            #     response = fetch.head(url)
            #     if response.status_code != 405:
            #         # just skip for now if HEAD not allowed
            #         response.raise_for_status()
            # except Exception as e:
            #     issues.append(
            #         Issue(
            #             type="open-graph-image-broken", context={"exception": str(e)},
            #         )
            #     )

            if not url_is_valid_absolute(url):
                issues.append(
                    Issue(
                        type="open-graph-image-not-canonical-https",
                        description="The og:image should be an absolute, HTTPS url.",
                        context={"content": url},
                    )
                )

        return issues


class OpenGraphSiteNameCheck(BaseOpenGraphCheck):
    og_property = "site_name"
