<!--
Copyright (c) 2020-2021 Paul Barker <paul@pbarker.dev>
SPDX-License-Identifier: CC-BY-4.0
-->

# mirrorshades

Mirroring tool written in Python.

Copyright (c) 2020-2021 Paul Barker.

Code distributed under the [Apache 2.0 License](https://choosealicense.com/licenses/apache-2.0/),
documentation distributed under the [CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/).

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
```

## Contribution

mirrorshades is developed on [sourcehut](https://sr.ht/) at
<https://sr.ht/~pbarker/mirrorshades/>.

If you find any bugs or have a feature request feel free to open a ticket in
the [issue tracker](https://todo.sr.ht/~pbarker/mirrorshades).

To submit patches to mirrorshades please
[send them to my public inbox](mailto:~pbarker/public-inbox@lists.sr.ht?subject=[mirrorshades])
with `[mirrorshades]` in the subject line. Please use
[plain text email](https://useplaintext.email/) when sending messages to this
list. Submitted patches and other discussions may be found in the
[archives](https://lists.sr.ht/~pbarker/public-inbox) of this mailing list. The
following commands can be used to configure git to format patches appropriately:

```
git config format.to '~pbarker/public-inbox@lists.sr.ht'
git config format.subjectPrefix 'mirrorshades][PATCH'
```

Further instructions on how to set up git to send emails can be found at
[git-send-email.io](https://git-send-email.io/).
