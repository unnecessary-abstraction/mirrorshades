# Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0


import logging
import sys
from dataclasses import dataclass

import desert
from marshmallow.exceptions import ValidationError


class Agent:
    @dataclass
    class Properties:
        name: str
        agent: str

    def __init__(self, properties):
        schema = desert.schema(self.Properties)
        try:
            self.properties = schema.load(properties)
        except ValidationError as e:
            name = properties.get("name", "(unknown)")
            for field_name, message in e.normalized_messages().items():
                if isinstance(message, list):
                    message = " ".join(message)
                logging.error(
                    f"Validation error on field '{field_name}' for source '{name}': {message}"
                )
            sys.exit(1)

    def mirror(self):
        raise NotImplementedError
