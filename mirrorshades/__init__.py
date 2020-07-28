# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

from .agents import get_agent
from .config import load_config


def main():
    config = load_config("local/mirrorshades.yml")

    for name, properties in config.items():
        properties["name"] = name
        agent = get_agent(properties)
        agent.mirror()
