"""Root module, where argument parsing is set up and main() is defined."""
from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path

from hcdb.ops import make, query, add, rm

cmdparser = ArgumentParser(prog="hcdb",
                           description="Create, query and manipulate CDBs.")

# Deal with both files and streams on stdin/stdout
cmdparser.add_argument('--file', '-f',
                       action='store',
                       type=Path,
                       help="operate on FILE (default: stdin)")

# Make/query/update operations will be implemented as sub-commands
subcmds = cmdparser.add_subparsers(required=True)

# Generic key/value parser for adding pairs
kvparser = ArgumentParser(add_help=False)
kvparser.add_argument('--kv',
                      action='append',
                      dest='pairs',
                      nargs=2,
                      metavar='KEY VALUE',
                      help="include the KEY->VALUE pair in the database")

# Make
make_cmd = subcmds.add_parser('make', parents=[kvparser])
make_cmd.set_defaults(cmd=make)

# Query
query_cmd = subcmds.add_parser('query')
query_cmd.set_defaults(cmd=query)
query_cmd.add_argument('key',
                       action='store',
                       help="the key to be retrieved")

# Update
# Needs two more sub-commands: add and rm
update_cmd = subcmds.add_parser('update')
updsub = update_cmd.add_subparsers(required=True)

# add
add_cmd = updsub.add_parser('add', parents=[kvparser])
add_cmd.set_defaults(cmd=add)

# rm
rm_cmd = updsub.add_parser('rm')
rm_cmd.set_defaults(cmd=rm)
rm_cmd.add_argument('key',
                    action='store',
                    help="the key to be deleted")


def main(args: Sequence[str] | None = None):
    """Parse args and dispatch the sub-command.

    If no argument sequence is provided, parse sys.argv.
    """
    # If an argument vector is passed via a parameter, use that
    pargs = cmdparser.parse_args(args)

    # The 'cmd' attribute contains the function implementing the command
    pargs.cmd(pargs)


if __name__ == '__main__':
    main()
