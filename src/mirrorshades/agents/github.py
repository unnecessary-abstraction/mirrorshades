# Copyright (c) 2021 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

import sys


from .base import Agent
from .git import Git


GITHUB_URL = "https://github.com/"


def make_relative_url(url):
    if url.startswith(GITHUB_URL):
        url = url[len(GITHUB_URL) :]
    return url


class Github(Agent):
    def mirror(self):
        try:
            import github
        except ModuleNotFoundError:
            print(
                "The `PyGithub` python package is needed to mirror from Github.",
                file=sys.stderr,
            )
            print(
                "Please install this (for example, using `pip install PyGithub`)"
                " and try again.",
                file=sys.stderr,
            )
            sys.exit(1)

        name = self.properties.get("name")
        access_token = self.properties.get("access_token")
        users = self.properties.get("users", [])
        organizations = self.properties.get("organizations", [])
        repo_fullnames = self.properties.get("repositories")
        repositories = []

        gh = github.Github(access_token)

        for username in users:
            user = gh.get_user(username)
            for repo in user.get_repos(type="owner"):
                relative_url = make_relative_url(repo.clone_url)
                repositories.append(relative_url)

        for orgname in organizations:
            org = gh.get_organization(orgname)
            for repo in org.get_repos():
                relative_url = make_relative_url(repo.clone_url)
                repositories.append(relative_url)

        for fullname in repo_fullnames:
            repo = gh.get_repo(fullname)
            relative_url = make_relative_url(repo.clone_url)
            repositories.append(relative_url)

        git_properties = {
            "name": name,
            "url_prefix": GITHUB_URL,
            "repositories": repositories,
        }
        git = Git(git_properties)
        git.mirror()
