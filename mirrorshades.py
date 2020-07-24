#! /usr/bin/env python3
#
# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0
#

import yaml


class ConnectionMethod:
    def __init__(self, properties):
        self.properties = properties

    def mirror(self):
        raise NotImplementedError


class Gitlab(ConnectionMethod):
    pass


class Git(ConnectionMethod):
    pass


connection_methods = {"gitlab": Gitlab, "git": Git}


def get_connection_method(properties):
    # The default connection method for a source is the name of the source
    # itself
    method_name = properties.get("connection_method", properties.get("name"))
    method_ctor = connection_methods[method_name]
    return method_ctor(properties)


def main():
    with open("local/mirrorshades.yml", "r") as f:
        config = yaml.safe_load(f)

    for name, properties in config.items():
        properties["name"] = name
        method = get_connection_method(properties)
        method.mirror()


if __name__ == "__main__":
    main()
