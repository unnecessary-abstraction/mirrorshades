# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import subprocess
from dataclasses import dataclass

from .base import Agent


class Command(Agent):
    @dataclass
    class Properties(Agent.Properties):
        command: str

    def mirror(self):
        subprocess.run(self.properties.command, shell=True, check=True)
