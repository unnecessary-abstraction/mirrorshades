# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import subprocess
from dataclasses import dataclass

from .base import Agent


class Command(Agent):
    @dataclass
    class Properties:
        name: str
        command: str

    def mirror(self):
        subprocess.run(self.properties.command, shell=True, check=True)
