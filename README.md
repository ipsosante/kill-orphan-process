# Kill Orphan Process

An utility script for kill orphan process tree in linux/unix system.

```shell script
$ killorphanprocess  --help

Usage: killorphanprocess [OPTIONS]

  An utility command for killing all orphan processes on unix/linux system

Options:
  --process-name TEXT         all child processes for <process-name> will be
                              killed

  --terminate-father-process  is father process name must be also kill ?
  -f, --force                 never prompt before removal
  --dry-run                   do not kill anything but log the list of process
                              to kill

  --debug                     debug mode
  --help                      Show this message and exit.
```