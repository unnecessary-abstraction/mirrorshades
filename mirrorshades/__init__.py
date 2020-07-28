# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

from .config import load_config


def main():
    config = load_config("local/mirrorshades.yml")

    for source in config.sources():
        source.mirror()
