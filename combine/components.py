import re
from typing import List, Dict, TYPE_CHECKING, Optional
import os
import jinja2

if TYPE_CHECKING:
    from .files.core import File


class Components:
    def __init__(self, components: Dict[str, "Component"]) -> None:
        self.components = components

    @classmethod
    def from_paths(
        cls, paths: List[str], jinja_environment: jinja2.Environment
    ) -> "Components":
        components = {}

        for component_dir in reversed(paths):
            for root, _, files in os.walk(component_dir):
                for file in files:
                    if file.endswith(".html"):
                        component = Component(
                            os.path.join(root, file), jinja_environment
                        )
                        components[component.name] = component

        return cls(components)

    def inject_components(self, file: "File", content: str) -> str:
        for component in self.components.values():
            content = component.inject(file, content)

        return content


class Component:
    def __init__(self, path: str, jinja_environment: jinja2.Environment) -> None:
        self.path = path
        # self.files_referencing = set()
        self.jinja_environment = jinja_environment

        self.name = os.path.basename(self.path).split(".")[0]

        self.components_path = os.path.relpath(self.path, "components")

        if not self.name[0].isupper():
            raise ValueError(
                f"Component name must start with an uppercase letter: {self.name}"
            )

        with open(self.path, "r") as f:
            self.content = f.read()

    def render(self, variables: dict) -> str:
        return self.jinja_environment.get_template(self.components_path).render(
            variables
        )

    def inject(self, file: "File", content: str) -> str:

        # TODO self closing tags not allowed yet...
        pattern = re.compile(
            r"<{}([\s\S]*?)>([\s\S]*?)</{}>".format(self.name, self.name)
        )

        # self.files_referencing.discard(file)  # Assume it isn't referenced

        def cb(match: re.Match) -> str:
            if f"<{self.name}" in match.group(2):
                raise ValueError(f"Component {self.name} cannot be nested in itself")

            attrs_str = match.group(1)
            content_str = match.group(2)

            attrs = parse_key_value_attrs(attrs_str)
            attrs["content"] = content_str or attrs.get("content", "")

            # self.files_referencing.add(file)

            return self.render(attrs)

        return pattern.sub(cb, content)


def parse_key_value_attrs(attrs_str: str) -> Dict[str, str]:
    pattern = re.compile(r"(.+)=[\"'](.+)[\"']")
    attrs = {}

    for match in pattern.finditer(attrs_str):
        attrs[match.group(1).strip()] = match.group(2).strip()

    return attrs
