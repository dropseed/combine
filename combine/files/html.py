import os

from .core import File
from .utils import create_parent_directory


class HTMLFile(File):
    def get_path_for_output(self):
        if self.name_without_extension.endswith(".keep"):
            # remove .keep.html from the end and replace with .html
            return super().get_path_for_output()[:-10] + ".html"

        if self.name_without_extension == "index":
            return super().get_path_for_output()

        return os.path.join(*self.root_parts, "index.html")

    def render_to_output(self, output_path, *args, **kwargs):
        target_path = os.path.join(output_path, self.output_relative_path)
        create_parent_directory(target_path)

        template = kwargs["jinja_environment"].get_template(self.content_relative_path)

        with open(target_path, "w+") as f:
            f.write(template.render(url=self._get_url()))

    def _get_url(self):
        url = "/" + self.output_relative_path
        if url.endswith("/index.html"):
            url = url[:-10]
        return url
