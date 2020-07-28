# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import yaml


from .agents import get_agent


class Source:
    def __init__(self, name, properties):
        self.properties = properties
        self.properties["name"] = name
        self.agent = get_agent(properties)

    def mirror(self):
        return self.agent.mirror()


class Config:
    def __init__(self, cfg):
        self.cfg = cfg

    def sources(self):
        cfg_sources = self.cfg.get("sources", [])
        return [Source(name, properties) for name, properties in cfg_sources.items()]


def load_config(filename):
    f = open(filename, "r")
    return Config(yaml.safe_load(f))
