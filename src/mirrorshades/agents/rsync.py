# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from dataclasses import dataclass, field
from typing import List

from .. import ConfigurationError
from ..util import runcmd
from .base import Agent


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

        dest = self.options.dest

        return os.path.dirname(os.path.join(dest, self.properties.name, path)) + "/"

    def validate_properties(self):
        if self.properties.user and not self.properties.host:
            raise ConfigurationError(
                "'user' cannot be set without 'host' in rsync agent"
            )

    def do_mirror(self):
        for path in self.properties.paths:
            path = os.path.normpath(path)
            remote_path = self.get_remote_path(path)
            local_path = self.get_local_path(path)

            logging.info(f"Syncing '{remote_path}' via rsync")
            runcmd(
                "rsync",
                "-aSH",
                "--mkpath",
                *self.options.rsync_extra_args,
                *self.properties.extra_args,
                remote_path,
                local_path,
            )
