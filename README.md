<!--
Copyright (c) 2020-2022 Paul Barker <paul@pbarker.dev>
SPDX-License-Identifier: CC-BY-4.0
-->

# mirrorshades

[mirrorshades](https://github.com/unnecessary-abstraction/mirrorshades)
is a tool for mirroring data from remote sources.

Copyright (c) 2020-2022 Paul Barker.

In this repository,
code files are distributed under the
[Apache 2.0 License](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)),
documentation files are distributed under the
[CC BY 4.0 License](https://tldrlegal.com/license/creative-commons-attribution-4.0-international-(cc-by-4))
and trivial data files are distributed under the
[CC0 1.0 License](https://tldrlegal.com/license/creative-commons-cc0-1.0-universal).

## Summary

Mirrorshades was written to help maintain mirrors and backups by regularly
pulling content from remote locations. Tools such as rsync, rclone, `git clone
--mirror`, etc already exist and can easily be used to create local mirrors of
remote content. What mirrorshades provides is a single command to update a set
of mirrors of different types of content from various remote sources. For
example, the author uses mirrorshades to sync content from Dropbox, GitLab and
multiple mail servers to a local mirror on a nightly basis for disaster
recovery purposes.

All the details of how to pull down the desired content are stored in the
configuration file, it is intended that command line arguments to mirrorshades
remain as minimal as possible and that the config file is the single source of
truth to control the operation of the utility. This makes it very easy to invoke
mirrorshades regularly and reliably using cron, systemd timers or any other
automation mechanism.

Mirrorshades is intended to be trivial to extend to handle new types of remote
source. Users familiar with Python are encouraged to look at the source code
for the existing mirroring agents and to add new agents as required. Such
extensions or other modifications to mirrorshades are welcome to be submitted
following the [contribution guidelines](#contribution), we will greatly
appreciate them!

## Installation

Mirrorshades is published on [PyPI](https://pypi.org/) so the following command
is usually sufficient to install the application:

```
pip install mirrorshades
```

The following mirroring agents have additional dependencies which must be
installed if you wish to use them in your configuration:

* `git`: Requires the [git](https://git-scm.com/) command line tool.

* `github`: Requires the Python module [PyGithub](https://pypi.org/project/PyGithub/)
  and the [git](https://git-scm.com/) command line tool.

* `gitlab`: Requires the Python module [python-gitlab](https://pypi.org/project/python-gitlab/)
  and the [git](https://git-scm.com/) command line tool.

* `rclone`: Requires the [rclone](https://rclone.org/) command line tool.

## Usage

All significant options for mirrorshades are set via a YAML configuration file
so command line invocation is very straightforward:

```
usage: mirrorshades [-h] [--version] [config_path]

Data mirroring tool

positional arguments:
  config_path  path to the configuration file (defaults to 'mirrorshades.yml' in the current directory)

optional arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
```

### Configuration example

The following example shows all the options and mirroring agents supported by
mirrorshades. Not all of these entries are required in your configuration file,
the minimum usable configuration is just one entry under `sources`.

```yaml
# Global options for mirrorshades
options:

  # Select the destination where mirrored content will be written. If no
  # destination is given, the current directory will be used.
  dest: /srv/mirror

# The core of a mirrorshades configuration file is the dictionary of
# sources to mirror. The key of each source entry is used as the default
# for the 'name' and 'agent' properties of that source if they are not set.
sources:

  # 'git' agent: Mirror one or more git repositories.
  # Repositories are cloned into subdirectories of the path
  # '<options.dest>/<source name>'. If local repositories are already
  # present (for example on a subsequent invocation of mirrorshades) then
  # they will be updated instead of freshly cloned.
  git:

    # URL prefix applied to all entries under 'repositories'. This reduces
    # duplication when mirroring multiple repositories from the same
    # upstream server.
    url_prefix: https://git.example.com/

    # List of repositories to mirror.
    repositories:

      # For example, this entry (along with the other example configuration
      # shown here) will mirror 'https://git.example.com/myrepository.git'
      # to '/srv/mirror/git/myrepository.git'.
      - myrepository.git

  # 'github' agent: Mirror repositories from a Github instance by full name,
  # user or organization. Note that this agent only mirrors git repository data
  # and not issues, merge requests, etc. Each git repository is mirrored using
  # the 'git' agent.
  github:

    # Access token. This may be set to allow access to private repositories.
    access_token: ...

    # List of users to mirror. Each user will be looked up using the Github API
    # and the git repositories which they own will be mirrored. The destination
    # path is formed in the same way as for the 'git' agent using the repository
    # clone url without the 'https://github.com/' prefix.
    users:
      - myusername

    # List of organizations to mirror. Each organization will be looked up using
    # the Github API and their git repositories will be mirrored. The
    # destination path is formed in the same way as for the 'git' agent using
    # the repository clone url without the 'https://github.com/' prefix.
    organizations:
      - myorganization

    # List of individual repositories to mirror, identified by their full name
    # (formed of the user or organization name, a '/' and then the repository
    # name). The destination path is formed in the same way as for the 'git'
    # agent using the repository clone url without the 'https://github.com/'
    # prefix.
    repositories:
      - torvalds/linux

  # 'gitlab' agent: Mirror groups and projects from a GitLab instance.
  # Note that this agent only mirrors git repository data and not issues,
  # merge requests, etc. Each git repository is mirrored using the 'git'
  # agent.
  gitlab:

    # GitLab server address. If not set, this defaults to
    # https://gitlab.com.
    server: https://gitlab.example.com

    # Private token used to connect to the GitLab API. Keep this secret!
    private_token: ...

    # List of projects to mirror. Each project will be looked up using the
    # GitLab API and the git repository will be mirrored. The destination
    # path is formed in the same way as for the 'git' agent using the
    # relative repository path given by the GitLab server.
    projects:
      - othergroup/myproject

    # List of groups to mirror. Each group will be recursively enumerated
    # using the GitLab API and all git repositories which are found will be
    # mirrored. Destination paths will be determined in the same way as for
    # individually listed projects.
    groups:
      - mygroup

  # 'rclone' agent: Mirror remote or cloud data which can be accessed using
  # rclone. Note that rclone must be configured separately before invoking
  # mirrorshades for this agent to work.
  #
  # In this example we use our own key 'my_cloud_data' instead of the agent
  # name 'rclone' so that the mirrored data will be placed under
  # '/srv/mirror/my_cloud_data'.
  my_cloud_data:

    # As the key we used does not match the agent we wish to use, we need
    # to explicitly specify the agent.
    agent: rclone

    # The rclone remote from which data will be mirrored. This should be
    # configured as a remote within rclone.
    remote: myremote

    # Paths within the given remote to mirror. To mirror all data from the
    # given rclone remote we can specify a single '.' path as shown here.
    paths:
      - '.'

  # 'command' agent: Invoke a custom command to mirror arbitrary data. In
  # this example we use the 'mbsync' command to create a local mirror of
  # one or more email accounts. This example assumes that appropriate
  # sources and destinations are setup in the mbsyncrc file, for other
  # commands you may similarly need to setup the relevant configuration
  # or pass appropriate command line arguments.
  mbsync:

    # As with the 'rclone' agent example above, the key does not match the
    # agent we wish to use so we need to explicitly specify the agent here.
    agent: command

    # The command to run along with any arguments.
    command: mbsync -a

    # Number of attempts to make. If the command fails, it is retried up to this
    # number of times. If the command succeeds it is not retried. This property
    # is optional, if it is unspecified the default is to only make one attempt
    # to run the command.
    attempts: 5
```

## Contribution

mirrorshades is developed on GitHub at
<https://github.com/unnecessary-abstraction/mirrorshades>.

If you find any bugs or have a feature request feel free to open a ticket in the
[issue tracker](https://github.com/unnecessary-abstraction/mirrorshades/issues).

To submit patches to mirrorshades please fork the repository on GitHub and open
a [pull request](https://github.com/unnecessary-abstraction/mirrorshades/pulls)
where your changes are ready to merge. Pull requests should generally be
targeted at the `dev` branch.
