# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import sys

from . import Configuration, ConfigurationError, ExecutionError, __version__

error_count = 0


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
    parser.add_argument(
        "--log-level",
        "-l",
        help="control the verbosity of logging messages "
        "(accepts 'DEBUG', 'INFO', 'WARNING', 'ERROR' and 'CRITICAL')",
    )
    parser.add_argument("--source", "-s", help="select a single source to synchronize")
    parser.add_argument(
        "--version", action="version", version=f"mirrorshades {__version__}"
    )
    return parser.parse_args()


def get_log_level(log_level_name):
    if log_level_name == "DEBUG":
        return logging.DEBUG
    if log_level_name == "INFO":
        return logging.INFO
    if log_level_name == "WARNING":
        return logging.WARNING
    if log_level_name == "ERROR":
        return logging.ERROR
    if log_level_name == "CRITICAL":
        return logging.CRITICAL


def main():
    args = parse_args()
    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=get_log_level(args.log_level)
    )
    try:
        cfg = Configuration.from_yaml_file(args.config_path)
    except ConfigurationError as e:
        logging.error(f"Configuration Error: {e}")
        sys.exit(1)

    try:
        if args.source:
            cfg.mirror_one(args.source)
        else:
            cfg.mirror_all()
    except ExecutionError as e:
        logging.error(e)
        sys.exit(1)
