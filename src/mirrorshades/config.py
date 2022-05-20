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

cfg = None
options = None
sources = None


@dataclass
class Options:
    dest: str = ""
    rsync_extra_args: List[str] = field(default_factory=list)


class Source:
    def __init__(self, name, properties):
        self.properties = properties
        self.properties["name"] = name
        self.agent = agents.get(properties)

    def mirror(self):
        return self.agent.mirror()


def parse_options():
    global options

    schema = desert.schema(Options)
    try:
        options = schema.load(cfg.get("options", {}))
    except ValidationError as e:
        for field_name, message in e.normalized_messages().items():
            if isinstance(message, list):
                message = " ".join(message)
            logging.error(f"Validation error on option '{field_name}': {message}")
        sys.exit(1)


def parse_sources():
    global sources

    cfg_sources = cfg.get("sources", [])
    sources = {
        name: Source(name, properties) for name, properties in cfg_sources.items()
    }


def load(filename):
    global cfg

    f = open(filename, "r")
    cfg = yaml.safe_load(f)
    parse_options()
    parse_sources()
