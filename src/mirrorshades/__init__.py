# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

__version__ = "0.3.0-dev"

import logging
from dataclasses import dataclass, field
from typing import List

import desert
import yaml
from marshmallow.exceptions import ValidationError


@dataclass
class Options:
    dest: str = ""
    rsync_extra_args: List[str] = field(default_factory=list)


class Source:
    def __init__(self, name, properties, options):
        from . import agents

        self.properties = properties
        self.properties["name"] = name
        self.agent = agents.get(properties, options)

    def mirror(self):
        return self.agent.mirror()


class ConfigurationError(Exception):
    pass


class ExecutionError(Exception):
    pass


class Configuration:
    def __init__(self, config_dict):
        self._parse_options(config_dict)
        self._parse_sources(config_dict)

    def _parse_options(self, config_dict):
        schema = desert.schema(Options)
        try:
            self.options = schema.load(config_dict.get("options", {}))
        except ValidationError as e:
            msg = "Validation errors occurred on the following options:"
            for field_name, message in e.normalized_messages().items():
                if isinstance(message, list):
                    message = " ".join(message)
                msg += f"\n\t'{field_name}': {message}"
            raise ConfigurationError(msg)

    def _parse_sources(self, config_dict):
        self.sources = {
            name: Source(name, properties, self.options)
            for name, properties in config_dict.get("sources", {}).items()
        }

    @staticmethod
    def from_yaml_file(filename):
        f = open(filename, "r")
        return Configuration(yaml.safe_load(f))

    def mirror_all(self):
        error_count = 0
        for source in self.sources.values():
            try:
                source.mirror()
            except ExecutionError as e:
                error_count += 1
                logging.error(e)
        if error_count:
            raise ExecutionError(f"Mirroring {error_count} sources failed")

    def mirror_one(self, source_name):
        try:
            self.sources[source_name].mirror()
        except KeyError:
            raise ExecutionError(
                f"Source '{source_name}' does not exist in config file"
            )
