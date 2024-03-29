# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

from ..util import runcmd
from .base import Agent


def do_fetch(url, local_path):
    logging.info(f"Fetching in {local_path}")
    runcmd("git", "fetch", "--all", "--prune", "-q", cwd=local_path)


def do_clone(url, local_path):
    logging.info(f"Cloning into {local_path}")
    parent_path = os.path.dirname(local_path)
    os.makedirs(parent_path, exist_ok=True)
    runcmd("git", "clone", "--mirror", "-q", url, local_path)


class Git(Agent):
    @dataclass
    class Properties(Agent.Properties):
        repositories: List[str]
        url_prefix: str = ""

    def do_mirror(self):
        dest = self.options.dest

        for repo in self.properties.repositories:
            url = urljoin(self.properties.url_prefix, repo)
            local_path = os.path.join(dest, self.properties.name, repo)
            if not local_path.endswith(".git"):
                local_path += ".git"

            if os.path.exists(local_path):
                do_fetch(url, local_path)
            else:
                do_clone(url, local_path)
