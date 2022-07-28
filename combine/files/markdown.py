import jinja2
import os

import frontmatter

from ..jinja.references import get_references_in_path
from .html import HTMLFile
from .utils import create_parent_directory
from ..components import Components


class MarkdownFile(HTMLFile):
    def _get_output_relative_path(self) -> str:
        if self.name_without_extension.endswith(".keep"):
            # remove .keep.md from the end and replace with .html
            return super()._get_output_relative_path()[:-8] + ".html"

        if self.name_without_extension == "index":
            return super()._get_output_relative_path()[:-3] + ".html"

        return os.path.join(*self.root_parts, "index.html")

    def load(self, jinja_environment: jinja2.Environment) -> None:
        filename = self._get_jinja_template(
            jinja_environment, self._get_variables()
        ).filename
        if filename:
            self.references = [os.path.basename(filename)] + get_references_in_path(
                filename, jinja_environment
            )
        else:
            self.references = []

    def _get_variables(self) -> dict:
        post = frontmatter.load(self.path)

        variables = post.metadata
        variables["url"] = self._get_url()
        variables["content"] = post.content

        return variables

    def _get_jinja_template(
        self, jinja_environment: jinja2.Environment, variables: dict
    ) -> jinja2.Template:
        template_name = variables.get("template", "markdown.template.html")
        return jinja_environment.get_template(template_name)

    def _render_to_output(
        self,
        output_path: str,
        jinja_environment: jinja2.Environment,
        components: Components,
    ) -> str:
        variables = self._get_variables()

        # TODO can post.content be jinja rendered to use variables?
        template = self._get_jinja_template(jinja_environment, variables)

        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        rendered = template.render(**variables)

        rendered = components.inject_components(self, rendered)

        with open(target_path, "w+") as f:
            f.write(rendered)

        return target_path
