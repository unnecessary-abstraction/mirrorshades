# Copyright (c) 2020 Paul Barker <pbarker@konsulko.com>
# SPDX-License-Identifier: Apache-2.0

import gitlab
from urllib.parse import urlparse


from .base import Agent
from .git import Git


class Gitlab(Agent):
    def mirror(self):
        name = self.properties.get("name")
        private_token = self.properties.get("private_token")
        server = self.properties.get("server", "https://gitlab.com")
        groups = self.properties.get("groups", [])
        projects = self.properties.get("projects", [])
        repositories = []

        gl = gitlab.Gitlab(server, private_token=private_token)

        for group_path in groups:
            group = gl.groups.get(group_path)
            for project in group.projects.list(include_subgroups=True):
                repositories.append(project.path_with_namespace)

        for project_path in projects:
            project = gl.projects.get(project_path)
            repositories.append(project.path_with_namespace)

        url = urlparse(server)
        location_with_auth = f"oauth2:{private_token}@{url.netloc}"
        url_prefix = url._replace(netloc=location_with_auth).geturl()
        git_properties = {
            "name": name,
            "url_prefix": url_prefix,
            "repositories": repositories,
        }
        git = Git(git_properties)
        git.mirror()
