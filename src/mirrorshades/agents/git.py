# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

import desert

from .. import config
from .base import Agent


def do_fetch(url, local_path):
    print(f"Fetching in {local_path}")
    subprocess.run(["git", "fetch", "--all", "-q"], cwd=local_path, check=True)


def do_clone(url, local_path):
    print(f"Cloning into {local_path}")
    parent_path = os.path.dirname(local_path)
    os.makedirs(parent_path, exist_ok=True)
    subprocess.run(["git", "clone", "--mirror", "-q", url, local_path], check=True)


@dataclass
class GitProperties:
    name: str
    repositories: List[str]
    url_prefix: str = ""


class Git(Agent):
    def mirror(self):
        schema = desert.schema(GitProperties)
        props = schema.load(self.properties)
        dest = config.get().option("dest")

        for repo in props.repositories:
            url = urljoin(props.url_prefix, repo)
            local_path = os.path.join(dest, props.name, repo)
            if not local_path.endswith(".git"):
                local_path += ".git"

            if os.path.exists(local_path):
                do_fetch(url, local_path)
            else:
                do_clone(url, local_path)
