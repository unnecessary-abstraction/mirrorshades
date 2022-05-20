# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import subprocess
from dataclasses import dataclass, field
from typing import List

from .. import config
from .base import Agent, MirroringError


class RSync(Agent):
    @dataclass
    class Properties(Agent.Properties):
        paths: List[str]
        prefix: str = ""
        host: str = ""
        user: str = ""
        extra_args: List[str] = field(default_factory=list)

    def get_remote_path(self, path):
        remote = ""
        if self.properties.host:
            if self.properties.user:
                remote += f"{self.properties.user}@"
            remote += f"{self.properties.host}:"

        if self.properties.prefix:
            prefixed_path = os.path.join(self.properties.prefix, path)
        else:
            prefixed_path = path

        return remote + prefixed_path

    def get_local_path(self, path):
        if path and path[0] == "/":
            path = path[1:]

        dest = config.options.dest

        return os.path.dirname(os.path.join(dest, self.properties.name, path)) + "/"

    def validate_properties(self):
        if self.properties.user and not self.properties.host:
            raise MirroringError("'user' cannot be set without 'host' in rsync agent")

    def do_mirror(self):
        self.validate_properties()

        for path in self.properties.paths:
            path = os.path.normpath(path)
            remote_path = self.get_remote_path(path)
            local_path = self.get_local_path(path)

            logging.info(f"Syncing '{remote_path}' via rsync")
            try:
                subprocess.run(
                    [
                        "rsync",
                        "-aSH",
                        "--mkpath",
                        *config.options.rsync_extra_args,
                        *self.properties.extra_args,
                        remote_path,
                        local_path,
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError:
                raise MirroringError("rsync command failed")
