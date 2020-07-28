# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
from urllib.parse import urljoin


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


class Git(Agent):
    def mirror(self):
        name = self.properties.get("name")
        url_prefix = self.properties.get("url_prefix", "")
        repositories = self.properties.get("repositories")
        dest = config.get().option("dest")

        for repo in repositories:
            url = urljoin(url_prefix, repo)
            local_path = os.path.join(dest, name, repo)
            if not local_path.endswith(".git"):
                local_path += ".git"

            if os.path.exists(local_path):
                do_fetch(url, local_path)
            else:
                do_clone(url, local_path)
