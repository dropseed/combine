from .base import Check
from .issues import Issues, Issue


# @Settings.register
# class TitleSuffixSetting(Setting):
#     name = "title-suffix"
#     default = ""


# _titles_seen = set()


class TitleCheck(Check):
    def __init__(self, html_soup):
        self.html_soup = html_soup

    def run(self):
        issues = Issues()

        title = self.html_soup.title

        if not title:
            issues.append(
                Issue(type="title-missing", description="The title tag is missing.")
            )
            return issues

        title = title.string

        # if title in _titles_seen:
        #     issues.append(
        #         Issue(
        #             type="duplicate-title", context={"title": title},
        #         )
        #     )
        # else:
        #     _titles_seen.add(title)

        # if len(title.split()) < 2 and not url_is_root(self.url):
        #     issues.append(
        #         Issue(type="title-too-short", context={"title": title},)
        #     )

        # suffix = Settings["title-suffix"]
        # if suffix and title.endswith(suffix):
        #     title = title[: -len(suffix)]

        # if len(title) > 60:
        #     issues.append(Issue(type="title-too-long", context={"title": title}))

        # TODO also check title-empty here? suffix used but template forgot to put something before it...

        if not title:
            issues.append(
                Issue(type="title-empty", description="The title tag has no content.")
            )

        return issues
