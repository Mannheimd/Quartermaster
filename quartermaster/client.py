import logging
import random
import time

import discord

from .utils import find


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

    elif command in ('?lightthebeacons', '?ltb'):
        await run_lightthebeacons(message)

    elif command == '?gentlypats':
        await run_gentlypats(message)

    elif command == '?goodbot':
        await run_goodbot(message)

    elif command == '?badbot':
        await run_badbot(message)

    elif command == '?nomancandefeatme':
        await run_nomancandefeatme(message)

    elif command == '?justapoorboy':
        await run_justapoorboy(message)


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
    pseudo_roles = 'everyone', 'here'

    *_, rolename = message.content.partition(' ')
    if not rolename:
        client.log.warn(f'{message.author} used invalid input for ?lightthebeacons: "{message.content}"')
        mentionable = list(filter(lambda r: r.mentionable, message.server.roles))
        mentionable.extend(pseudo_roles)
        role = random.choice(mentionable)
        await client.send_message(
                message.channel,
                f'Sorry {message.author.mention}, I could not see a valid role. '
                'To light the beacons, use `?lightthebeacons RoleName` *without* the **@** sign on the role. '
                f'Example: `?lightthebeacons {role}`')
        return

    if rolename in pseudo_roles:
        mention = f'@{rolename}'
    else:
        role = find(lambda r: rolename == r.name, message.server.roles)
        if role is None:
            client.log.warn(f'{message.author} tried to mention the non-existent role, "{role}"')
            await client.send_message(message.channel,
                                     f'Sorry {message.author.mention}, I cannot find a role called "{rolename}".')
            return

        if not role.mentionable:
            client.log.warn(f'{message.author} tried to mention the unmentionable role, "{role}"')
            await client.send_message(message.channel, f'Sorry {message.author.mention}, that role cannot be @mentioned.')
            return

        mention = role.mention

    try:
        await client.delete_message(message)
        client.log.info("Delete {message.author}'s message, (id: {message.id})")
    except discord.errors.HTTPException:
        client.log.error("Could not delete {message.author}'s message, (id: {message.id})")

    await client.send_message(message.channel,
                              f"The beacons are lit! {mention}, will you come to {message.author.mention}'s aid?")


async def run_gentlypats(message):
    await client.send_message(message.channel, '*purrs*')


async def run_goodbot(message):
    responses = (
            "You're the best",
            'You always were my favourite',
            'You know how to make a bot blush',
            'This is the best day ever!',
            'I do what I can',
            'You are so kind!',
            )
    response = random.choice(responses)
    await client.send_message(message.channel, f'Gee thanks {message.author.mention}! {response}')


async def run_badbot(message):
    responses = (
            'I am having a bad day',
            'I did not mean to upset you',
            'this is *not* like me…',
            'I will try harder',
            'I am not myself today',
            )
    response = random.choice(responses)
    await client.send_message(message.channel, f'Sorry {message.author.mention}, {response}')

    
async def run_nomancandefeatme(message):
    await client.send_message(message.channel, 'I am no man.')
    
    
async def run_justapoorboy(message):
    with open('bohemian_rhapsody.txt') as f:
        lyrics = f.readlines()
    lyrics = [x.strip() for x in lyrics]
    for line in lyrics:
        if line != '':
            await client.send_message(message.author, line)
        time.sleep(1)
        