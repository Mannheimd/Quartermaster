#!/usr/bin/env python3

import argparse
from collections import ChainMap, OrderedDict
import json
from pathlib import Path
import textwrap

from quartermaster.utils import flatten
from quartermaster import logging


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _split_lines(self, text, width):
        lines = flatten(textwrap.wrap(t, width) for t in text.splitlines())
        return tuple(lines)


default = {
        'config_files': Path('config.json').absolute(),
        'verbosity': 'error',
        'log_file_mode': 'a',
        'log_file_verbosity': 'debug',
        }


def args(*args, **kwargs):
    """Parse arguments semantically."""

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
                        (default: {default['config_files'].name})""")


    token_group = parser.add_mutually_exclusive_group()
    token_group.add_argument('-t', '--token',
                             help='API Token')
    token_group.add_argument('-tf', '--token-file',
                             nargs='?', const='api.key',
                             help='File which contains API Token. (default: api.key)')


    logging_group = parser.add_argument_group(
            title='logging',
            description='There are various levels of logging, in order of verbosity.')
    logging_group.add_argument('-v', '--verbosity',
                               choices=logging.levels,
                               help=f'Set verbosity for console output. (default: {default["verbosity"]})')
    logging_group.add_argument('-l', '--log-file',
                               nargs='?', const='server.log',
                               help='File to log bot status. (default: server.log)')
    logging_group.add_argument('-lm', '--log-file-mode',
                               choices=('w', 'a'),
                               help=f'Set mode for log file, (over)write, or append. (default: {default["log_file_mode"]})')
    logging_group.add_argument('-lv', '--log-file-verbosity',
                               choices=logging.levels,
                               help=f'Set log file verbosity. (default: {default["log_file_verbosity"]})')


    parser.set_defaults(**kwargs)
    args = parser.parse_args(args)

    # flatten any given configuration files
    if args.config_files is not None:
        filenames = flatten(args.config_files, default['config_files'])
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
    combined_args.maps.append(default)
    combined_args.maps.append(vars(parser.parse_args([])))

    # flatten configuration into most precedence for each argument into given API
    args = argparse.Namespace(**combined_args)

    # get verbosity 'Enum'
    args.verbosity = logging.levels[args.verbosity]
    args.log_file_verbosity = logging.levels[args.log_file_verbosity]
    if args.log_file:
        args.log_file = Path(args.log_file).absolute()

    if args.token_file:
        args.token_file = Path(args.token_file).absolute()

    return args, parser.format_usage(), parser.format_help()


