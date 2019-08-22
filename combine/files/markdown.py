import os

import frontmatter

from .html import HTMLFile
from .utils import create_parent_directory


class MarkdownFile(HTMLFile):
    def get_path_for_output(self):
        if self.name_without_extension.endswith(".keep"):
            # remove .keep.md from the end and replace with .html
            return super().get_path_for_output()[:-8] + ".html"

        if self.name_without_extension == "index":
            return super().get_path_for_output()[:-3] + ".html"

        return os.path.join(*self.root_parts, "index.html")

    def render_to_output(self, output_path, *args, **kwargs):
        post = frontmatter.load(self.path)

        variables = post.metadata
        variables["url"] = self._get_url()
        variables["content"] = post.content

        template = kwargs["jinja_environment"].get_template("markdown.template.html")

        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        with open(target_path, "w+") as f:
            f.write(template.render(**variables))
