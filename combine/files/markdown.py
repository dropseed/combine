import os

import frontmatter

from .html import HTMLFile
from .utils import create_parent_directory


class MarkdownFile(HTMLFile):
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
