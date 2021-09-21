# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
from dataclasses import dataclass
from typing import List

from .. import config
from .base import Agent


class RClone(Agent):
    @dataclass
    class Properties:
        name: str
        remote: str
        paths: List[str]

    def mirror(self):
        dest = config.get().option("dest")

        for path in self.properties.paths:
            if path == ".":
                path = ""
            full_path = ":".join([self.properties.remote, path])
            local_path = os.path.join(dest, self.properties.name, path)
            subprocess.run(
                ["rclone", "sync", "--create-empty-src-dirs", full_path, local_path],
                check=True,
            )
