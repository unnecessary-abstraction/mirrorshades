# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import yaml

from . import agents

_CONFIG = {}


DEFAULT_OPTIONS = {"dest": ""}


class Source:
    def __init__(self, name, properties):
        self.properties = properties
        self.properties["name"] = name
        self.agent = agents.get(properties)

    def mirror(self):
        return self.agent.mirror()


class Config:
    def __init__(self, cfg):
        self.cfg = cfg

    def sources(self):
        cfg_sources = self.cfg.get("sources", [])
        return [Source(name, properties) for name, properties in cfg_sources.items()]

    def option(self, name):
        options = self.cfg.get("options", {})
        default_value = DEFAULT_OPTIONS.get(name)
        return options.get(name, default_value)


def load(filename):
    global _CONFIG
    f = open(filename, "r")
    _CONFIG = Config(yaml.safe_load(f))
    return _CONFIG


def get():
    return _CONFIG
