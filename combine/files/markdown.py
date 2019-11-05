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

    def get_render_variables(self):
        variables = super().get_render_variables()

        # Use frontmatter
        post = frontmatter.load(self.path)
        variables.update(post.metadata)
        variables["content"] = post.content

        return variables

    def get_template_path(self):
        # TODO get from frontmatter too?
        return "markdown.template.html"
