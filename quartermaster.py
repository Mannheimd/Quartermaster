#!/usr/bin/env python3

import argparse
from collections import ChainMap, OrderedDict
import errno
import json
import logging
from pathlib import Path
import sys
import textwrap

from utils import flatten
from client import client


def create_logger(verbosity=logging.ERROR,
                  log_file=None, log_file_mode='a', log_file_verbosity=logging.DEBUG):

    # create/get logger for this instance
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # with stream (console) handle
    ch = logging.StreamHandler()
    ch.setLevel(verbosity)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # optionally with file handle
    if log_file:
        fh = logging.FileHandler(log_file, mode=log_file_mode)
        fh.setLevel(log_file_verbosity)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _split_lines(self, text, width):
        lines = flatten(textwrap.wrap(t, width) for t in text.splitlines())
        return tuple(lines)


def parse_args(*args, **kwargs):
    """Parse arguments semantically."""

    default_args = {
            'config_files': Path('config.json').absolute(),
            'verbosity': 'error',
            'log_file_mode': 'a',
            'log_file_verbosity': 'debug',
            }

    parser = argparse.ArgumentParser(
            description='The "Solitude Of War" Discord Bot',
            formatter_class=HelpFormatter)

    parser.add_argument('-f', '--config-files',
                        action='append', nargs='*',
                        help=f"""
Configuration file(s) containing command line arguments in JSON format; e.g.,'
    {{
        "token_file": "quartermaster.key",
        "verbosity": "warning",
        "log_file": "quartermaster.log"
    }}
                        (default: {default_args['config_files'].name})""")


    token_group = parser.add_mutually_exclusive_group()
    token_group.add_argument('-t', '--token',
                             help='API Token')
    token_group.add_argument('-tf', '--token-file',
                             nargs='?', const='api.key',
                             help='File which contains API Token. (default: api.key)')


    logging_levels = OrderedDict((lvl, getattr(logging, lvl.upper()))
                                 for lvl in ('critical', 'error', 'warning', 'info', 'debug'))
    logging_group = parser.add_argument_group(
            title='logging',
            description='There are various levels of logging, in order of verbosity.')
    logging_group.add_argument('-v', '--verbosity',
                               choices=logging_levels,
                               help=f'Set verbosity for console output. (default: {default_args["verbosity"]})')
    logging_group.add_argument('-l', '--log-file',
                               nargs='?', const='server.log',
                               help='File to log bot status. (default: server.log)')
    logging_group.add_argument('-lm', '--log-file-mode',
                               choices=('w', 'a'),
                               help=f'Set mode for log file, (over)write, or append. (default: {default_args["log_file_mode"]})')
    logging_group.add_argument('-lv', '--log-file-verbosity',
                               choices=logging_levels,
                               help=f'Set log file verbosity. (default: {default_args["log_file_verbosity"]})')


    parser.set_defaults(**kwargs)
    args = parser.parse_args(args)

    # flatten any given configuration files
    if args.config_files is not None:
        filenames = flatten(args.config_files, default_args['config_files'])
        args.config_files = tuple(Path(filename).absolute() for filename in filenames)

    combined_args = ChainMap({}, {k: v for k, v in vars(args).items() if v is not None})

    def recurse_config_files(cfg, file_map):
        paths = cfg.get('config_files')
        if paths is None:
            return
        for path in filter(None, paths):
            path = Path(path).absolute()
            if path not in file_map:
                with path.open() as file:
                    cfg = json.load(file)
                file_map[path] = cfg
                recurse_config_files(cfg,  file_map)

    # recurse the tree and include configures in order of given precedence
    file_map = OrderedDict()
    recurse_config_files(combined_args, file_map)
    combined_args.maps.extend(file_map.values())
    combined_args.update(config_files=file_map.keys())
    combined_args.maps.append(default_args)
    combined_args.maps.append(vars(parser.parse_args([])))

    # flatten configuration into most precedence for each argument into given API
    args = argparse.Namespace(**combined_args)

    # get verbosity 'Enum'
    args.verbosity = logging_levels[args.verbosity]
    args.log_file_verbosity = logging_levels[args.log_file_verbosity]
    if args.log_file:
        args.log_file = Path(args.log_file).absolute()

    # inject logger into client
    client.log = create_logger(args.verbosity,
                               args.log_file, args.log_file_mode, args.log_file_verbosity)

    if args.token is None:
        if args.token_file is None:
            client.log.error(f'No token or token file provided; please indicate a token.')
            parser.print_help()
            exit(errno.EACCES)
        args.token_file = Path(args.token_file).absolute()
        try:
            args.token = args.token_file.read_text().strip()
            client.log.info(f'Reading API key from {args.token_file}')
        except FileNotFoundError:
            client.log.error(f'{args.token_file} cannot be found; please indicate a token.')
            parser.print_help()
            exit(errno.ENOENT)

    return args


def run(*args, **kwargs):
    """Run the module level client."""

    args = parse_args(*args, **kwargs)
    client.run(args.token)


if __name__ == '__main__':
    run(*sys.argv[1:])
