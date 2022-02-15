# Copyright (c) 2022 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
from dataclasses import dataclass, field
from typing import List
from urllib.parse import urlparse

from .base import Agent
from .git import Git

GITHUB_URL = "https://github.com/"


def make_relative_url(url):
    if url.startswith(GITHUB_URL):
        url = url[len(GITHUB_URL) :]
    return url


class Github(Agent):
    @dataclass
    class Properties(Agent.Properties):
        access_token: str
        users: List[str] = field(default_factory=list)
        organizations: List[str] = field(default_factory=list)
        repositories: List[str] = field(default_factory=list)

    def mirror(self):
        try:
            import github
        except ModuleNotFoundError:
            logging.error(
                "The `PyGithub` python package is needed to mirror from Github."
            )
            logging.info(
                "Please install `PyGithub` (for example, using `pip install PyGithub`)"
                " and try again."
            )
            sys.exit(1)

        repositories = []

        gh = github.Github(self.properties.access_token)

        for username in self.properties.users:
            user = gh.get_user(username)
            for repo in user.get_repos(type="owner"):
                relative_url = make_relative_url(repo.clone_url)
                repositories.append(relative_url)

        for orgname in self.properties.organizations:
            org = gh.get_organization(orgname)
            for repo in org.get_repos():
                relative_url = make_relative_url(repo.clone_url)
                repositories.append(relative_url)

        for fullname in self.properties.repositories:
            repo = gh.get_repo(fullname)
            relative_url = make_relative_url(repo.clone_url)
            repositories.append(relative_url)

        url = urlparse(GITHUB_URL)
        location_with_auth = f"{self.properties.access_token}@{url.netloc}"
        url_prefix = url._replace(netloc=location_with_auth).geturl()
        git_properties = {
            "name": self.properties.name,
            "agent": "git",
            "url_prefix": url_prefix,
            "repositories": repositories,
        }
        git = Git(git_properties)
        git.mirror()
