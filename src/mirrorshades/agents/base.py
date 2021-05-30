# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0


class Agent:
    def __init__(self, properties):
        self.properties = properties

    def mirror(self):
        raise NotImplementedError
