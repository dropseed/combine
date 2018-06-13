import os

import yaml


class Config:
    def __init__(self, path):
        self.path = path
        self.data = {}

        if os.path.exists(self.path):
            self.data = yaml.safe_load(open(self.path, 'r'))

    def get_variables(self):
        return self.data.get('variables', {})
