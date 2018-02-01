#!/usr/bin/env python3

import argparse
from collections import ChainMap, OrderedDict
import errno
import itertools as it
import json
import logging
import os
import random
import sys
import textwrap

import discord


def flatten(iter_of_iters, fillvalue=None):
    """
    Flatten one level of nesting.
    [ [A, B], [C, D], [E, F, G] ] ==> [A, B, C, D, E, F, G]

    in the case of `fillvalue is not None`
    [ [A, B], [], [C, D, E] ] ==> [A, B, X, C, D, E]
        where fillvalue=X
    """

    if fillvalue is None:
        for element in it.chain.from_iterable(iter_of_iters):
            yield element
    else:
        for itr in iter_of_iters:
            if not itr:
                yield fillvalue
            for element in itr:
                yield element


def find(pred, iterable):
    """
    Find the first occurrence of the predicate function returning true over the iterable; otherwise None.
    >>> find(lambda e: e.startswith('g'), ['alpha', 'beta', 'gamma', 'delta'])
    'gamma'
    >>> find(lambda e: e.startswith('p'), ['alpha', 'beta', 'gamma', 'delta'])
    None
    """

    for element in iterable:
        if pred(element):
            return element


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _split_lines(self, text, width):
        lines = flatten(textwrap.wrap(t, width) for t in text.splitlines())
        return tuple(lines)


class Client(discord.Client):
    """Quartermaster client."""

    def __init__(self, logger=logging.getLogger(), *args, **kwargs):
        self.log = logger
        super().__init__(*args, **kwargs)

    async def send_message(self, destination, content=None, *, tts=False, embed=None):
        if content is not None:
            self.log.info(f'Sending message to #{destination}: {content}')
        await super().send_message(destination, content, tts=tts, embed=embed)


# module level client
client = Client()


@client.event
async def on_ready():
    client.log.info(f'Logged in as: {client.user.name} ({client.user.id})')


@client.event
async def on_message(message):
    if message.content.startswith('?'):
        command, *_ = message.content.partition(' ')
        client.log.info(f'User: {message.author.name} ({message.author.id}) sent: {message.content}')
        await command_center(command, message)


async def command_center(command, message):
    if command == '?shutdown':
        await run_shutdown(message)

    elif command == '?hello':
        await run_hello(message)

    elif command == '?myroles':
        await run_myroles(message)

    elif command == '?amiadmin':
        await run_amiadmin(message)

    elif command == '?lightthebeacons':
        await run_lightthebeacons(message)

    elif command == '?gentlypats':
        await run_gentlypats(message)

    elif command == '?goodbot':
        await run_goodbot(message)


async def run_shutdown(message):
    if message.author.server_permissions.administrator:
        await client.send_message(message.channel, 'Goodbye')
        raise KeyboardInterrupt()
    else:
        await client.log.warn(f'{message.author} attempted to shutdown Quartermaster')
        await client.send_message(message.channel, f'Sorry {message.author.mention}, I cannot let you do that.')


async def run_hello(message):
    await client.send_message(message.channel, f'Hello to you too, {message.author.mention}!')


async def run_myroles(message):
    roles = '\n\t'.join(role.name.strip('@') for role in message.author.roles)
    await client.send_message(message.channel, f'Your Roles:\n\t{roles}')


async def run_amiadmin(message):
    msg = f'Sorry {message.author.mention}, you *are not* an admin'
    if message.author.server_permissions.administrator:
        msg = f'Indeed {message.author.mention}, you *are* an admin'

    await client.send_message(message.channel, msg)


async def run_lightthebeacons(message):
    *_, rolename = message.content.partition(' ')
    if not rolename:
        client.log.warn(f'{message.author} used invalid input for ?lightthebeacons: "{message.content}"')
        await client.send_message(
                message.channel,
                f'Sorry {message.author.mention}, I could not see a valid role. '
                'To light the beacons, use `?lightthebeacons RoleName` without the @ sign on the role. '
                'Example: `?lightthebeacons Overwatchers`')
        return

    role = find(lambda r: rolename == r.name, message.server.roles)
    if role is None:
        client.log.warn(f'{message.author} tried to mention the non-existent role, "{role}"')
        await client.send_message(message.channel, f'Sorry {message.author.mention}, I cannot find a role called "{rolename}".')
        return

    if not role.mentionable:
        client.log.warn(f'{message.author} tried to mention the unmentionable role, "{role}"')
        await client.send_message(message.channel, f'Sorry {message.author.mention}, that role cannot be @mentioned.')
        return

    try:
        await client.delete_message(message)
        client.log.info("Delete {message.author}'s message, (id: {message.id})")
    except discord.errors.HTTPException:
        client.log.error("Could not delete {message.author}'s message, (id: {message.id})")

    await client.send_message(message.channel,
                              f"The beacons are lit! {role.mention}, will you come to {message.author.mention}'s aid?")


async def run_gentlypats(message):
    await client.send_message(message.channel, '*purrs*')


async def run_goodbot(message):
    responses = (
            "You're the best",
            'You always were my favourite',
            'You know how to make a bot blush',
            'This is the best day ever!',
            'I do what I can',
            'You are so kinda!',
            )
    response = random.choice(responses)
    client.send_message(message.channel, f'Gee thanks {message.author.mention}! {response}')


def run(*args, **kwargs):
    """Run the module level client."""

    default_args = {
            'config_files': 'config.json',
            'verbosity': 'error',
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
        "log_file": "quartermaster.log",
        "verbosity": "warning"
    }}
                        (default: {default_args['config_files']})""")


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
    logging_group.add_argument('-lv', '--log-file-verbosity',
                               choices=logging_levels,
                               help=f'Set log file verbosity. (default: {default_args["log_file_verbosity"]})')


    parser.set_defaults(**kwargs)
    args = parser.parse_args(args)

    # flatten any given configuration files
    if args.config_files is not None:
        args.config_files = tuple(flatten(args.config_files, default_args['config_files']))

    combined_args = ChainMap({}, {k: v for k, v in vars(args).items() if v is not None})

    def load_config_file(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)

    def recurse_config_files(cfg, file_map):
        files = cfg.get('config_files')
        if files is None:
            return
        for file in files:
            if file is not None and file not in file_map:
                cfg = load_config_file(file)
                file_map[file] = cfg
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

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # get verbosity 'Enum'
    args.verbosity = logging_levels[args.verbosity]
    args.log_file_verbosity = logging_levels[args.log_file_verbosity]

    # with stream (console) handle
    ch = logging.StreamHandler()
    ch.setLevel(args.verbosity)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # optionally with file handle
    if args.log_file:
        fh = logging.FileHandler(args.log_file, mode='a')
        fh.setLevel(args.log_file_verbosity)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    # inject logger into client
    client.log = logger

    if args.token is None:
        if args.token_file is None:
            client.log.error(f'No token or token file provided; please indicate a token.')
            parser.print_help()
            exit(errno.EACCES)
        args.token_file = os.path.abspath(args.token_file)
        try:
            with open(args.token_file, 'r') as file:
                client.log.info(f'Reading API key from {args.token_file}')
                args.token = file.read().strip()
        except FileNotFoundError:
            client.log.error(f'{args.token_file} cannot be found; please indicate a token.')
            parser.print_help()
            exit(errno.ENOENT)

    client.run(args.token)


if __name__ == '__main__':
    run(*sys.argv[1:])
