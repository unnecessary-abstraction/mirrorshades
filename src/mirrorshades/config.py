# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
from dataclasses import dataclass, field
from typing import List

import desert
import yaml
from marshmallow.exceptions import ValidationError

from . import agents

_CONFIG = None


class Source:
    def __init__(self, name, properties):
        self.properties = properties
        self.properties["name"] = name
        self.agent = agents.get(properties)

    def mirror(self):
        return self.agent.mirror()


class Config:
    @dataclass
    class Options:
        dest: str = ""
        rsync_extra_args: List[str] = field(default_factory=list)

    def parse_options(self):
        schema = desert.schema(self.Options)
        try:
            self.options = schema.load(self._cfg.get("options", {}))
        except ValidationError as e:
            for field_name, message in e.normalized_messages().items():
                if isinstance(message, list):
                    message = " ".join(message)
                logging.error(f"Validation error on option '{field_name}': {message}")
            sys.exit(1)

    def parse_sources(self):
        cfg_sources = self._cfg.get("sources", [])
        self.sources = [
            Source(name, properties) for name, properties in cfg_sources.items()
        ]

    def __init__(self, cfg):
        self._cfg = cfg
        self.parse_options()
        self.parse_sources()


def load(filename):
    global _CONFIG
    f = open(filename, "r")
    _CONFIG = Config(yaml.safe_load(f))
    return _CONFIG


def get():
    return _CONFIG
