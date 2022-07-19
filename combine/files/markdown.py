import os

import frontmatter

from ..jinja.references import get_references_in_path
from .html import HTMLFile
from .utils import create_parent_directory


class MarkdownFile(HTMLFile):
    def _get_output_relative_path(self):
        if self.name_without_extension.endswith(".keep"):
            # remove .keep.md from the end and replace with .html
            return super()._get_output_relative_path()[:-8] + ".html"

        if self.name_without_extension == "index":
            return super()._get_output_relative_path()[:-3] + ".html"

        return os.path.join(*self.root_parts, "index.html")

    def load(self, jinja_environment):
        template = self._get_jinja_template(jinja_environment, self._get_variables())
        self.references = [
            os.path.basename(template.filename)
        ] + get_references_in_path(template.filename, jinja_environment)

    def _get_variables(self):
        post = frontmatter.load(self.path)

        variables = post.metadata
        variables["url"] = self._get_url()
        variables["content"] = post.content

        return variables

    def _get_jinja_template(self, jinja_environment, variables):
        template_name = variables.get("template", "markdown.template.html")
        return jinja_environment.get_template(template_name)

    def _render_to_output(self, output_path, jinja_environment):
        variables = self._get_variables()

        # TODO can post.content be jinja rendered to use variables?
        template = self._get_jinja_template(jinja_environment, variables)

        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        with open(target_path, "w+") as f:
            f.write(template.render(**variables))

        return target_path
