# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0


class Agent:
    def __init__(self, properties):
        self.properties = properties

    def mirror(self):
        raise NotImplementedError
