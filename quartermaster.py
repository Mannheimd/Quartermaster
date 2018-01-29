#!/usr/bin/env python3

import argparse
import datetime
import errno
import logging
import sys
import os

import discord


class Client(discord.Client):
    """Quatermaster client."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send_message(self, destination, content=None, *, tts=False, embed=None):
        if content is not None:
            print(time_now(), '- Sending message to', f'#{destination}:', content)
        await super().send_message(destination, content, tts=tts, embed=embed)


# module level client
client = Client()


def time_now():
    return datetime.datetime.now().time()


@client.event
async def on_ready():
    print(time_now(), '- Logged in as:', client.user.name, f'({client.user.id})')


@client.event
async def on_message(message):
    if message.content.startswith('?'):
        command = message.content.split(' ', 1)[0]
        print(time_now(), '- User: ', message.author.name, f'({message.author.id})', 'sent:', message.content)
        await command_center(command, message)


async def command_center(command, message):
    if command == '?shutdown':
        await run_shutdown(message)

    if command == '?hello':
        await run_hello(message)

    if command == '?myroles':
        await run_myroles(message)

    if command == '?amiadmin':
        await run_amiadmin(message)

    if command == '?lightthebeacons':
        await run_lightthebeacons(message)


async def run_shutdown(message):
    if message.author.server_permissions.administrator:
        await client.send_message(message.channel, 'Goodbye')
        raise KeyboardInterrupt()
    else:
        await client.send_message(message.channel, f"Sorry, I can't let you do that {message.author.mention}.")


async def run_hello(message):
    await client.send_message(message.channel, f'Hello to you too, {message.author.mention}!')


async def run_myroles(message):
    roles_textified = 'Your roles:'
    for role in message.author.roles:
        roles_textified = roles_textified + '\n' + role.name.strip('@')
    await client.send_message(message.channel, roles_textified)


async def run_amiadmin(message):
    msg = f'Sorry {message.author.mention}, you *are not* an admin'
    if message.author.server_permissions.administrator:
        msg = f'Indeed {message.author.mention}, you *are* an admin'

    await client.send_message(message.channel, msg)


async def run_lightthebeacons(message):
    try:
        argument = message.content.split(' ', 1)[1].strip('@')
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


def run(*args):
    """Run the module level client."""

    parser = argparse.ArgumentParser(
            description='The "Solitude Of War" Discord Bot')

    token_group = parser.add_mutually_exclusive_group()
    token_group.add_argument('-t', '--token',
                             action='store', type=str,
                             help='API Token')
    token_group.add_argument('-f', '--token-file',
                             action='store', type=str, default='api.key',
                             help='File which contains API Token; default: api.key')

    args = parser.parse_args(args)


    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # with file handle
    fh = logging.FileHandler('test.log', mode='a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # with stream (console) handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(fmt)
    logger.addHandler(ch)


    args.token_file = os.path.abspath(args.token_file)
    if args.token is None:
        try:
            with open(args.token_file, 'r') as file:
                print(time_now(), '- Reading API key from', args.token_file)
                args.token = file.read().strip()
        except FileNotFoundError:
            print(time_now(), '- Error: ', args.token_file, 'cannot be found; please indicate a token.')
            parser.print_help()
            exit(errno.ENOENT)

    client.run(args.token)


if __name__ == '__main__':
    run(*sys.argv[1:])
