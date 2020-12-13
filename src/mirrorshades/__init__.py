# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import argparse


from . import config


__version__ = "0.1"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="mirrorshades", description="Data mirroring tool"
    )
    parser.add_argument(
        "config_path",
        default="mirrorshades.yml",
        nargs="?",
        help="path to the configuration file (defaults to 'mirrorshades.yml' "
        "in the current directory)",
    )
    parser.add_argument(
        "--version", action="version", version=f"mirrorshades {__version__}"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = config.load(args.config_path)

    for source in cfg.sources():
        source.mirror()
