# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import subprocess
from dataclasses import dataclass

from .base import Agent


class Command(Agent):
    @dataclass
    class Properties(Agent.Properties):
        command: str
        attempts: int = 1

    def mirror(self):
        for i in range(self.properties.attempts):
            if self.properties.attempts > 1:
                suffix = f" [attempt {i+1} of {self.properties.attempts}]"
            else:
                suffix = ""
            logging.info(f"Running `{self.properties.command}`{suffix}")
            try:
                subprocess.run(self.properties.command, shell=True, check=True)
                return
            except subprocess.CalledProcessError:
                if i == self.properties.attempts:
                    raise
