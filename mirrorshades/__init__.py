# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import yaml


from .agents import get_agent


def main():
    with open("local/mirrorshades.yml", "r") as f:
        config = yaml.safe_load(f)

    for name, properties in config.items():
        properties["name"] = name
        agent = get_agent(properties)
        agent.mirror()
