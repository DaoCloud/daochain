from __future__ import print_function

import logging
import os
import sys
from inspect import getdoc

from utils import DocoptCommand
from utils import NoSuchCommand
from utils import parse_doc_section

log = logging.getLogger(__name__)

console_handler = logging.StreamHandler(sys.stderr)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)
    # Disable requests logging
    logging.getLogger("requests").propagate = False


class TopLevelCommand(DocoptCommand):
    """
    DaoCloud Blockchain Docker Image Verifier

    Usage:
      dao [options] [COMMAND] [ARGS...]

    Options:
      -h, --help     Show this help information and exit.

    Commands:
      status         Show the status of dao service.
      login          Login to daohub.
      images         Show all images.
      sign           Sign a image.
      publish        Publish a image to daochain.
      validate       Validate a image.
      server         Start verifier server.

    """
    base_dir = '.'

    def perform_command(self, options, handler, command_options):
        handler(command_options)
        return

    def docopt_options(self):
        options = super(TopLevelCommand, self).docopt_options()
        options['version'] = 'v0.1'
        return options

    def version(self, options):
        """
        Show the version information

        Usage: version
        """
        print('v0.1')

    def login(self, options):
        """
        Login to daolcoud daohub
        """
        pass

    def list(self, options):
        """
        List local images and their verify stats.

        """
        pass

#     def server(self, options):
#         """
#         Usage: server
#         """
#         from server.gunicorn_runner import run_app
#         run_app()


def main():
    setup_logging()
    try:
        command = TopLevelCommand()
        command.sys_dispatch()
    except NoSuchCommand as e:
        commands = "\n".join(parse_doc_section("commands:", getdoc(e.supercommand)))
        log.error("No such command: %s\n\n%s", e.command, commands)
        sys.exit(1)


if __name__ == '__main__':
    main()
