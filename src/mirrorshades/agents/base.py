# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0


from dataclasses import dataclass

import desert


class Agent:
    @dataclass
    class Properties:
        name: str

    def __init__(self, properties):
        schema = desert.schema(self.Properties)
        self.properties = schema.load(properties)

    def mirror(self):
        raise NotImplementedError
