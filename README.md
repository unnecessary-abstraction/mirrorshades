# mirrorshades

<!--
Copyright The mirrorshades Contributors.
SPDX-License-Identifier: CC-BY-4.0
-->

[![pre-commit.ci status][pre-commit badge]][pre-commit link]
[![PyPI][pypi badge]][pypi link]

[pre-commit badge]:     https://results.pre-commit.ci/badge/github/unnecessary-abstraction/mirrorshades/main.svg
[pre-commit link]:      https://results.pre-commit.ci/latest/github/unnecessary-abstraction/mirrorshades/main
[pypi badge]:           https://img.shields.io/pypi/v/mirrorshades
[pypi link]:            https://pypi.org/project/mirrorshades/

An easily extensible tool for mirroring data from git repositories, cloud
storage, mail servers and other remote sources.

Mirrorshades was written to help maintain mirrors and backups by regularly
pulling content from remote locations. Tools such as rsync, rclone and `git
clone --mirror` already exist, but what this tool provides is integration and
automation. A single invocation of mirrorshades can update a set of mirrors of
different types of content from various remote sources. For example, the author
uses this tool to sync content from Dropbox, GitLab and multiple mail servers
to a local mirror on a nightly basis for disaster recovery purposes.

A configuration file is used to control the operation of mirrorshades, and
command line arguments are kept to a minimum. This makes it easy to invoke the
tool regularly and reliably. In line with the [Unix philosophy][], mirrorshades
does not include any way to schedule when mirrors are updated. Instead, it is
expected that [systemd timers][] or a cron implementation (such as [cronie][] or
[yacron][]) will be used if scheduling is required.

[Unix philosophy]:      https://en.wikipedia.org/wiki/Unix_philosophy
[systemd timers]:       https://opensource.com/article/20/7/systemd-timers
[cronie]:               https://github.com/cronie-crond/cronie
[yacron]:               https://pypi.org/project/yacron/

Mirrorshades is intended to be trivial to extend to handle new types of remote
source. Users familiar with Python are encouraged to look at the source code
for the existing mirroring agents and to add new agents as required. Such
extensions or other modifications to mirrorshades are welcome to be submitted
following the [contribution guidelines](#contribution), we will greatly
appreciate them!

## Installation

Mirrorshades is published on [PyPI][] so the following command is usually
sufficient to install the application:

[pypi]:                 https://pypi.org/

```shell
pip install mirrorshades
```

The following mirroring agents have additional dependencies which must be
installed if you wish to use them in your configuration:

* `git`: Requires the [git][] command line tool.

* `github`: Requires the Python module [PyGithub][] and the [git][] command line
  tool.

* `gitlab`: Requires the Python module [python-gitlab][] and the [git][] command
  line tool.

* `rclone`: Requires the [rclone][] command line tool.

[git]:                  https://git-scm.com/
[pygithub]:             https://pypi.org/project/PyGithub/
[python-gitlab]:        https://pypi.org/project/python-gitlab/
[rclone]:               https://rclone.org/

## Usage

All significant options for mirrorshades are set via a YAML configuration file.
Command line arguments may optionally be used to specify the config file to use
and to select one source defined in the config file to mirror (instead of
mirroring all sources defined in the config file).

```text
usage: mirrorshades [-h] [--source SOURCE] [--version] [config_path]

Data mirroring tool

positional arguments:
  config_path           path to the configuration file (defaults to 'mirrorshades.yml' in the current directory)

options:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        select a single source to synchronize
  --version             show program's version number and exit
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

  # Specify a list of additional command line arguments to be passed to all
  # invocations of rsync by the rsync agent.
  rsync_extra_options: ["-v"]

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

  # 'rsync' agent: Mirror local or remote data using rsync.
  rsync:

    # Remote host to sync from over ssh. This property is optional and may be
    # used as an alternative to specifying the remote host in 'prefix'.
    host: example.com

    # Username to use when connecting to the remote host. This property is
    # optional and may be used as an alternative to specifying the username in
    # 'prefix'. This property may only be set if 'host' is also set.
    user: root

    # Prefix applied to all entries in 'paths'. This property is optional and
    # may include remote connection details in the form 'user@host:path' (for
    # ssh) or 'rsync://user@host:path' (for rsync protocol), where 'user@' is
    # optional.
    prefix: /srv

    # List of paths to mirror. For each path entry, the full source path is
    # constructed by prepending the 'host', 'user' and 'prefix' properties
    # described above if they are provided. The destination path is constructed
    # using only the global 'dest' option, source name and path entry. So for
    # example, the 'www' path entry below will result in mirroring
    # 'root@example.com:/srv/www' to '/srv/mirror/rsync/www'
    paths:
      - www
      - ftp

    # Specify a list of additional command line arguments to be passed to
    # invocations of rsync for this source. These arguments are passed after
    # those specified in the global 'extra_rsync_args' option.
    extra_args: ["--delete-after"]

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

## Maintainers

* Paul Barker [:envelope:](mailto:paul@pbarker.dev)

## Contribution

mirrorshades is developed on GitHub at
<https://github.com/unnecessary-abstraction/mirrorshades>.

If you find any bugs or have a feature request feel free to open a ticket in the
[issue tracker][].

To submit patches to mirrorshades please fork the repository on GitHub and open
a [pull request][] where your changes are ready to merge. Pull requests should
generally be targeted at the `main` branch.

[issue tracker]:        https://github.com/unnecessary-abstraction/mirrorshades/issues
[pull request]:         https://github.com/unnecessary-abstraction/mirrorshades/pulls

### Setting up a development environment

The best way to setup a development environment for this project is to create a
[venv][] then make an [editable installation][] of mirrorshades into this new
venv, along with all the required development dependencies. This can be done
using the following commands:

[venv]: https://docs.python.org/3/tutorial/venv.html
[editable installation]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .[test,github,gitlab,development]
```

### Testing changes

When a pull request is opened on GitHub for this project, automated testing will
be performed to validate the proposed changes. It can also be helpful to run
these automated tests locally during development to catch any potential issues
prior to submission of a PR.

Two tools are used in the automated testing of this project:

* [pre-commit][] is used to perform linting, check code formatting, catch common
  errors and ensure that licensing information for the project is complete.

* [pytest][] is used to run a suite of unit and integrations tests to ensure that
  the program behaviour is correct.

[pre-commit]: https://pre-commit.com/
[pytest]: https://pytest.org/

All automated tests can be run using the following commands:

```sh
pre-commit run -a
pytest
```

Additionally, you may wish to install the pre-commit git hook so that the
pre-commit tests run on every `git commit` operation. This can be achieved using
the following command:

```sh
pre-commit install
```

## License

Copyright (c) 2020-2023, mirrorshades contributors.

* Code files are distributed under the [Apache-2.0 License][].

* Documentation files are distributed under the [CC-BY-4.0 License][].

* Trivial data files are distributed under the [CC0-1.0 License][].

[Apache-2.0 License]:   https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)
[CC-BY-4.0 License]:    https://tldrlegal.com/license/creative-commons-attribution-4.0-international-(cc-by-4)
[CC0-1.0 License]:      https://tldrlegal.com/license/creative-commons-cc0-1.0-universal
