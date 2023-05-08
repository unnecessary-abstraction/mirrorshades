# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

from .. import ConfigurationError
from .command import Command
from .git import Git
from .github import Github
from .gitlab import Gitlab
from .rclone import RClone
from .rsync import RSync

agents = {
    "command": Command,
    "git": Git,
    "github": Github,
    "gitlab": Gitlab,
    "rclone": RClone,
    "rsync": RSync,
}


def get(properties, options):
    # The default connection method for a source is the name of the source
    # itself
    if "agent" not in properties:
        properties["agent"] = properties["name"]
    try:
        agent_ctor = agents[properties["agent"]]
    except KeyError:
        raise ConfigurationError(f"No such agent: {properties['agent']}")
    return agent_ctor(properties, options)
