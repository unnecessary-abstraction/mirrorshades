# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import subprocess
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

from .. import config
from .base import Agent


def do_fetch(url, local_path):
    logging.info(f"Fetching in {local_path}")
    subprocess.run(
        ["git", "fetch", "--all", "--prune", "-q"], cwd=local_path, check=True
    )


def do_clone(url, local_path):
    logging.info(f"Cloning into {local_path}")
    parent_path = os.path.dirname(local_path)
    os.makedirs(parent_path, exist_ok=True)
    subprocess.run(["git", "clone", "--mirror", "-q", url, local_path], check=True)


class Git(Agent):
    @dataclass
    class Properties(Agent.Properties):
        repositories: List[str]
        url_prefix: str = ""

    def mirror(self):
        dest = config.get().option("dest")

        for repo in self.properties.repositories:
            url = urljoin(self.properties.url_prefix, repo)
            local_path = os.path.join(dest, self.properties.name, repo)
            if not local_path.endswith(".git"):
                local_path += ".git"

            if os.path.exists(local_path):
                do_fetch(url, local_path)
            else:
                do_clone(url, local_path)
