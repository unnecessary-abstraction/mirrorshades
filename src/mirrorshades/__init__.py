# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging

from . import config

__version__ = "0.2.0"


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
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    args = parse_args()
    cfg = config.load(args.config_path)

    for source in cfg.sources():
        source.mirror()
