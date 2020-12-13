# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess


from .. import config
from .base import Agent


class RClone(Agent):
    def mirror(self):
        name = self.properties.get("name")
        remote = self.properties.get("remote")
        paths = self.properties.get("paths")
        dest = config.get().option("dest")

        for path in paths:
            if path == ".":
                path = ""
            full_path = ":".join([remote, path])
            local_path = os.path.join(dest, name, path)
            subprocess.run(
                ["rclone", "sync", "--create-empty-src-dirs", full_path, local_path],
                check=True,
            )
