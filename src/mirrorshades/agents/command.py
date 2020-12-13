# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import subprocess


from .. import config
from .base import Agent


class Command(Agent):
    def mirror(self):
        command = self.properties.get("command")
        subprocess.run(command, shell=True, check=True)
