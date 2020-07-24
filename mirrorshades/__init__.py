# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import yaml


class Agent:
    def __init__(self, properties):
        self.properties = properties

    def mirror(self):
        raise NotImplementedError


class Gitlab(Agent):
    pass


class Git(Agent):
    pass


agents = {"gitlab": Gitlab, "git": Git}


def get_agent(properties):
    # The default connection method for a source is the name of the source
    # itself
    agent_name = properties.get("agent", properties.get("name"))
    agent_ctor = agents[agent_name]
    return agent_ctor(properties)


def main():
    with open("local/mirrorshades.yml", "r") as f:
        config = yaml.safe_load(f)

    for name, properties in config.items():
        properties["name"] = name
        agent = get_agent(properties)
        agent.mirror()
