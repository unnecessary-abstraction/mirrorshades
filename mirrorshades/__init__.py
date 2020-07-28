# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

from . import config


def main():
    cfg = config.load("local/mirrorshades.yml")

    for source in cfg.sources():
        source.mirror()
