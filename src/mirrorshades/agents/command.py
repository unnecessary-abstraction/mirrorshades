# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import subprocess


from .base import Agent


class Command(Agent):
    def mirror(self):
        command = self.properties.get("command")
        subprocess.run(command, shell=True, check=True)
