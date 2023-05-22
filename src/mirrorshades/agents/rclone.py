# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import subprocess
from dataclasses import dataclass
from typing import List

from .base import Agent


class RClone(Agent):
    @dataclass
    class Properties(Agent.Properties):
        remote: str
        paths: List[str]

    def do_mirror(self):
        dest = self.options.dest

        for path in self.properties.paths:
            if path == ".":
                path = ""
            full_path = ":".join([self.properties.remote, path])
            local_path = os.path.join(dest, self.properties.name, path)
            logging.info(f"Syncing '{full_path}' via rclone")
            subprocess.run(
                ["rclone", "sync", "--create-empty-src-dirs", full_path, local_path],
                check=True,
            )
