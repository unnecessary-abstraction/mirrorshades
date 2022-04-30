# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import subprocess
from dataclasses import dataclass
from typing import List

from .. import config
from .base import Agent


class RSync(Agent):
    @dataclass
    class Properties(Agent.Properties):
        paths: List[str]
        prefix: str = ""
        host: str = ""
        user: str = ""

    def mirror(self):
        dest = config.get().option("dest")

        for path in self.properties.paths:
            path = os.path.normpath(path)

            remote = ""
            if self.properties.host:
                if self.properties.user:
                    remote += f"{self.properties.user}@"
                remote += f"{self.properties.host}:"
            elif self.properties.user:
                logging.error(f"`user` cannot be set without `host` in rsync agent")
                continue

            if self.properties.prefix:
                prefixed_path = os.path.join(self.properties.prefix, path)
            else:
                prefixed_path = path
            full_path = remote + prefixed_path

            if path and path[0] == '/':
                path = path[1:]

            local_path = os.path.dirname(os.path.join(dest, self.properties.name, path)) + "/"

            logging.info(f"Syncing `{full_path}` via rsync")
            subprocess.run(
                ["rsync", "-aSH", "--mkpath", full_path, local_path],
                check=True,
            )
