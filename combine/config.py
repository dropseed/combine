import os
import datetime

import yaml


class Config:
    def __init__(self, path):
        self.path = path
        self.data = {}

        if os.path.exists(self.path):
            self.data = yaml.safe_load(open(self.path, 'r'))
            if self.data is None:
                # allow an empty file to start with
                self.data = {}

    def get_variables(self):
        variables = self.default_variables()
        user_variables = self.data.get('variables', {})
        variables.update(user_variables)
        return variables

    def default_variables(self):
        return {
            'now': datetime.datetime.now  # as a function
        }

    def get_commands(self, command_type):
        cmds = self.data.get(command_type, [])
        if not isinstance(cmds, list):
            cmds = [cmds]
        return cmds
