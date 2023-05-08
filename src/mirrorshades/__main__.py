# Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import sys

from . import __version__, config


def parse_args():
    parser = argparse.ArgumentParser(
        prog="mirrorshades",
        description="An easily extensible tool for mirroring data from "
        "git repositories, cloud storage, mail servers and other remote sources.",
    )
    parser.add_argument(
        "config_path",
        default="mirrorshades.yml",
        nargs="?",
        help="path to the configuration file "
        "(defaults to 'mirrorshades.yml' in the current directory)",
    )
    parser.add_argument("--source", "-s", help="select a single source to synchronize")
    parser.add_argument(
        "--version", action="version", version=f"mirrorshades {__version__}"
    )
    return parser.parse_args()


def main():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    args = parse_args()
    config.load(args.config_path)

    if args.source:
        try:
            config.sources[args.source].mirror()
        except KeyError:
            logging.error(f"Source '{args.source}' does not exist in config file")
            sys.exit(1)
    else:
        for source in config.sources.values():
            source.mirror()
