# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

from .command import Command
from .git import Git
from .gitlab import Gitlab
from .rclone import RClone


agents = {
    "command": Command,
    "gitlab": Gitlab,
    "git": Git,
    "rclone": RClone,
}


def get(properties):
    # The default connection method for a source is the name of the source
    # itself
    agent_name = properties.get("agent", properties.get("name"))
    agent_ctor = agents[agent_name]
    return agent_ctor(properties)
