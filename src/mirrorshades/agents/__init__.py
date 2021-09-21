# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import sys

from .command import Command
from .git import Git
from .github import Github
from .gitlab import Gitlab
from .rclone import RClone

agents = {
    "command": Command,
    "git": Git,
    "github": Github,
    "gitlab": Gitlab,
    "rclone": RClone,
}


def get(properties):
    # The default connection method for a source is the name of the source
    # itself
    agent_name = properties.get("agent", properties.get("name"))
    try:
        agent_ctor = agents[agent_name]
    except KeyError:
        logging.error(f"No such agent: {agent_name}")
        sys.exit(1)
    return agent_ctor(properties)
