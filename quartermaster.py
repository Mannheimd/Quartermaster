#!/usr/bin/env python3

import argparse
from collections import ChainMap
import errno
import json
import logging
import sys
import os

import discord


class Client(discord.Client):
    """Quatermaster client."""

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


async def run_shutdown(message):
    if message.author.server_permissions.administrator:
        await client.send_message(message.channel, 'Goodbye')
        raise KeyboardInterrupt()
    else:
        await client.send_message(message.channel, f"Sorry, I can't let you do that {message.author.mention}.")


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
    try:
        *_, argument = message.content.partition(' ')
    except:
        await client.send_message(
                message.channel,
                f"I'm sorry {message.author.mention}, I couldn't see a valid role. "
                'To light the beacons, use `?lightthebeacons RoleName` without the @ sign on the role. '
                'Example: `?lightthebeacons Overwatchers`')
        return

    for role in message.server.roles:
        if role.name.lower() == argument.lower():
            if role.mentionable:
                await client.delete_message(message)
                await client.send_message(message.channel,
                                   f"The beacons are lit! {role.mention}, will you come to {message.author.mention}'s aid?")
                return
            else:
                await client.send_message(message.channel, f"I'm sorry {message.author.mention}, that role can't be @mentioned.")
                return

    await client.send_message(message.channel, f"I'm sorry {message.author.mention}, I can't find a role called '{argument}'.")


async def run_gentlypats(message):
    await client.send_message(message.channel, '*purrs*')


def run(*args, **kwargs):
    """Run the module level client."""

    default_args = {
            'token_file': 'api.key',
            'verbosity': 'error',
            'log_file_verbosity': 'debug',
            }

    parser = argparse.ArgumentParser(
            description='The "Solitude Of War" Discord Bot')

    parser.add_argument('-f', '--config-file',
                        action='store', type=str,
                        nargs='?', const='config.json',
                        help=f"""
Configuration file containing commandline arguments in JSON format; e.g.,'
    {{
        "token_file": "quatermaster.key",
        "log_file": "quatermaster.log",
        "verbosity": "warning"
    }}
                        ; default: config.json""")


    token_group = parser.add_mutually_exclusive_group()
    token_group.add_argument('-t', '--token',
                             action='store', type=str,
                             help='API Token')
    token_group.add_argument('-tf', '--token-file',
                             action='store', type=str,
                             help='File which contains API Token; default: api.key')

    logging_group = parser.add_argument_group(
            title='logging',
            description='There are various levels of logging, in order of verbosity: '
                        'critical, error, warning, info, debug, noset.')
    logging_group.add_argument('-v', '--verbosity',
                               action='store', type=str,
                               help='Set verbosity for console output; default: error')
    logging_group.add_argument('-l', '--log-file',
                               action='store', type=str,
                               help='File to log bot status. Not used by default.')
    logging_group.add_argument('-vv', '--log-file-verbosity',
                               action='store', type=str,
                               help='Set log file verbosity; default: debug')


    parser.set_defaults(**kwargs)
    args = parser.parse_args(args)
    combined_args = ChainMap({k: v for k, v in vars(args).items() if v is not None})

    def load_config_file(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)

    if args.config_file is not None:
        cfg = load_config_file(args.config_file)
        combined_args.maps.append(cfg)

    combined_args.maps.append(default_args)
    args = argparse.Namespace(**combined_args)

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # get verbosity 'Enum'
    args.verbosity = getattr(logging, args.verbosity.upper())
    args.log_file_verbosity = getattr(logging, args.log_file_verbosity.upper())

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

    args.token_file = os.path.abspath(args.token_file)
    if args.token is None:
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
