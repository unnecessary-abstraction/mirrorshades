# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

import logging
import shlex
import subprocess

from . import ExecutionError


def runcmd(*args, attempts=0, **kwargs):
    if kwargs and "shell" in kwargs and kwargs["shell"]:
        cmd = args[0]
        cmd_string = cmd
    else:
        cmd = args
        cmd_string = shlex.join(cmd)
    logging.debug(f"Running command `{cmd_string}`")

    if kwargs:
        logging.debug(f"    kwargs: {kwargs}")

    if attempts:
        for i in range(attempts):
            logging.debug(f"    attempt {i+1} of {attempts}")
            result = subprocess.run(cmd, **kwargs)
            if result.returncode and (i + 1 == attempts):
                raise ExecutionError(
                    f"Command failed after {attempts} attempts: `{cmd_string}`, kwargs: {kwargs}"
                )
    else:
        result = subprocess.run(cmd, **kwargs)
        if result.returncode:
            raise ExecutionError(f"Command failed: `{cmd_string}`, kwargs: {kwargs}")
