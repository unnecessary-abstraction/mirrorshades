# mirrorshades

Mirroring tool written in Python.

## Installation

Mirrorshades is published on [PyPI](https://pypi.org/) so the following command
is usually sufficient to install the application:

```
pip install mirrorshades
```

## Usage

Most options for mirrorshades are set via a YAML configuration file commandline
invocation is very straightforward:

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

mirrorshades is developed on [GitLab](https://gitlab.com/) at
<https://gitlab.com/pbarker.dev/mirrorshades>.

If you find any bugs or have a feature request feel free to open a ticket in
the [issue tracker](https://gitlab.com/pbarker.dev/mirrorshades/-/issues).

To submit patches to mirrorshades please fork the repository on GitLab and
[open a merge request](https://gitlab.com/pbarker.dev/mirrorshades/-/merge_requests).
