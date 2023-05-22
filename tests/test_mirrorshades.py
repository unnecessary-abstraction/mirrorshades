# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

from mirrorshades import Configuration, ConfigurationError, ExecutionError


def test_empty():
    config_dict = {}
    cfg = Configuration(config_dict)
    cfg.mirror_all()


def test_hello(tmp_path):
    os.chdir(tmp_path)
    config_dict = {
        "sources": {
            "hello": {"agent": "command", "command": "echo Hello World > hello.txt"}
        }
    }
    cfg = Configuration(config_dict)
    cfg.mirror_all()
    assert os.path.exists("hello.txt")
    with open("hello.txt", "r") as f:
        assert f.read() == "Hello World\n"


def test_mirror_one(tmp_path):
    os.chdir(tmp_path)
    config_dict = {
        "sources": {
            "hello1": {"agent": "command", "command": "echo Hello World > hello1.txt"},
            "hello2": {"agent": "command", "command": "echo Hello World > hello2.txt"},
        }
    }
    cfg = Configuration(config_dict)
    cfg.mirror_one("hello1")
    assert os.path.exists("hello1.txt")
    assert not os.path.exists("hello2.txt")


def test_unknown_source():
    config_dict = {
        "sources": {
            "hello": {"agent": "command", "command": "echo Hello World > hello.txt"}
        }
    }
    cfg = Configuration(config_dict)
    with pytest.raises(ExecutionError):
        cfg.mirror_one("wibble")


@pytest.mark.network
def test_git(tmp_path):
    os.chdir(tmp_path)
    config_dict = {
        "sources": {
            "git": {
                "url_prefix": "https://github.com",
                "repositories": ["unnecessary-abstraction/mirrorshades"],
            }
        }
    }
    cfg = Configuration(config_dict)
    cfg.mirror_all()
    assert os.path.exists("git/unnecessary-abstraction/mirrorshades.git")


def test_invalid_options():
    config_dict = {"options": {"nonsense": True}}
    with pytest.raises(ConfigurationError):
        Configuration(config_dict)


def test_unknown_agent():
    config_dict = {"sources": {"missing": {"some_argument": True}}}
    with pytest.raises(ConfigurationError):
        Configuration(config_dict)


def test_invalid_source():
    config_dict = {"sources": {"hello": {"agent": "command", "wibble": True}}}
    with pytest.raises(ConfigurationError):
        Configuration(config_dict)
