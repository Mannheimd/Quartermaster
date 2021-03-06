import errno
import sys

from .client import client
from . import logging, parse
from .meta import *


def run(*args, **kwargs):
    """Run the module level client."""

    args, usage_text, help_text = parse.args(*args, **kwargs)
    
    log_file = None
    if args.log_file:
        log_file = logging.log_file(args.log_file,
                                    args.log_file_mode,
                                    args.log_file_verbosity)

    # inject logger into client
    client.log = logging.logger(args.verbosity, log_file)

    if args.token is None:
        if args.token_file is None:
            client.log.error(f'No token or token file provided; please indicate a token.')
            print(help_text)
            exit(errno.EACCES)
        try:
            args.token = args.token_file.read_text().strip()
            client.log.info(f'Reading API key from {args.token_file}')
        except FileNotFoundError:
            client.log.error(f'{args.token_file} cannot be found; please indicate a token.')
            print(help_text)
            exit(errno.ENOENT)

    client.run(args.token)


def main():
    run(*sys.argv[1:])
