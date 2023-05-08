# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0


from dataclasses import dataclass

import desert
from marshmallow.exceptions import ValidationError

from .. import ConfigurationError, ExecutionError


class Agent:
    @dataclass
    class Properties:
        name: str
        agent: str

    def __init__(self, properties, options):
        self.options = options
        schema = desert.schema(self.Properties)
        try:
            self.properties = schema.load(properties)
        except ValidationError as e:
            name = properties.get("name", "(unknown)")
            msg = f"Validation errors occurred on the following properties for source '{name}':"
            for field_name, message in e.normalized_messages().items():
                if isinstance(message, list):
                    message = " ".join(message)
                msg += f"\n\t'{field_name}': {message}"
            raise ConfigurationError(msg)
        self.validate_properties()

    def validate_properties(self):
        pass

    def do_mirror(self):
        raise NotImplementedError

    def mirror(self):
        try:
            self.do_mirror()
        except ExecutionError as e:
            # Re-raise the error with more context
            raise ExecutionError(
                f"Mirroring source '{self.properties.name}' with agent "
                f"'{self.properties.agent}' failed: {e}"
            )
