# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass

from ..util import runcmd
from .base import Agent


class Command(Agent):
    @dataclass
    class Properties(Agent.Properties):
        command: str
        attempts: int = 1

    def do_mirror(self):
        runcmd(self.properties.command, attempts=self.properties.attempts, shell=True)
