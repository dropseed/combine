import os
import datetime

import yaml


class Config:
    def __init__(self, path):
        self.path = path
        self.data = {}

        if os.path.exists(self.path):
            self.data = yaml.safe_load(open(self.path, "r"))
            if self.data is None:
                # allow an empty file to start with
                self.data = {}

    @property
    def output_path(self):
        return os.path.abspath(self.data.get("output_path", "output"))

    @property
    def content_paths(self):
        if "content_paths" in self.data:
            paths = self.data["content_paths"]
        else:
            paths = ["content"]
            if os.path.exists(os.path.join("theme", "content")):
                paths.append(os.path.join("theme", "content"))

        # add the built-in content from combine itself
        paths.append(os.path.join(os.path.dirname(__file__), "base_content"))

        return [os.path.abspath(x) for x in paths]

    @property
    def variables(self):
        variables = self.default_variables

        for name, data in self.data.get("variables", {}).items():
            if isinstance(data, dict):
                if "default" in data:
                    variables[name] = data["default"]

                if "from_env" in data and data["from_env"] in os.environ:
                    variables[name] = os.environ[data["from_env"]]
            else:
                variables[name] = data

        return variables

    @property
    def default_variables(self):
        return {"now": datetime.datetime.now}  # as a function

    @property
    def steps(self):
        return self.data.get("steps", [])
