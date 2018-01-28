#!/usr/bin/env python3

import argparse
import asyncio
import datetime
import io
import os

import discord


parser = argparse.ArgumentParser(
        description='The "Solitude Of War" Discord Bot')

token_group = parser.add_mutually_exclusive_group()
token_group.add_argument('-t', '--token',
                         action='store', type=str,
                         help='API Token')
token_group.add_argument('-f', '--token-file',
                         action='store', type=str, default='api.key',
                         help='File which contains API Token; default: api.key')

args = parser.parse_args()


def time_now():
    return str(datetime.datetime.now().time())


if args.token is None:
    with open(args.token_file, 'r') as file:
        print(time_now() + ' - Reading API key from ' + args.token_file + '\n')
        args.token = file.read().strip()


client = discord.Client()


@client.event
async def on_ready():
    print(time_now() + ' - Logged in as: ')
    print(client.user.name)
    print(client.user.id)


@client.event
async def on_message(message):
    if message.content.startswith('?'):
        command = message.content.split(' ', 1)[0]
        print(time_now() + ' - User ' + message.author.name + '(' + message.author.id + ') sent: ' + message.content)
        await command_center(command, message)


async def send_message(channel, message):
    print(time_now() + ' - Sending message to ' + channel.name + ': ' + message)
    await client.send_message(channel, message)


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
        await send_message(message.channel, 'Goodbye')
        raise KeyboardInterrupt()
    else:
        await send_message(message.channel, 'Sorry, I can\'t let you do that ' + message.author.mention + '.')


async def run_hello(message):
    await send_message(message.channel, 'Hello to you too, ' + message.author.mention + '!')


async def run_myroles(message):
    roles_textified = 'Your roles:'
    for role in message.author.roles:
        roles_textified = roles_textified + '\n' + role.name.strip('@')
    await send_message(message.channel, roles_textified)


async def run_amiadmin(message):
    await send_message(message.channel, str(message.author.server_permissions.administrator))


async def run_lightthebeacons(message):
    try:
        argument = message.content.split(' ', 1)[1].strip('@')
    except:
        await send_message(message.channel, 'I\'m sorry ' + message.author.mention + ', I couldn\'t see a valid role. To light the beacons, use `?lightthebeacons RoleName` without the @ sign on the role. Example: `?lightthebeacons Overwatchers`')
        return

    for role in message.server.roles:
        if role.name.lower() == argument.lower():
            if role.mentionable:
                await client.delete_message(message)
                await send_message(message.channel, 'The beacons are lit! ' + role.mention + ' , will you come to ' + message.author.mention + '\'s aid?')
                return
            else:
                await send_message(message.channel, 'I\'m sorry ' + message.author.mention + ', that role can\'t be @mentioned.')
                return

    await send_message(message.channel, 'I\'m sorry ' + message.author.mention + ', I can\'t find a role called \'' + argument + '\'.')


client.run(args.token)
