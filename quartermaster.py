import asyncio
import datetime
import io
import os

import discord

client = discord.Client()

def get_current_directory():
	return os.getcwd()

def load_text_from_file(path):
	print(time_now() + ' - Reading API key from ' + path + '\n')
	return open(path).read().strip()
	
def time_now():
	return str(datetime.datetime.now().time())

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

async def run_shutdown(message):
	if message.author.server_permissions.administrator:
		await send_message(message.channel, 'Goodbye')
		raise KeyboardInterrupt()
	else:
		await send_message(message.channel, 'Sorry, I can\'t let you do that ' + message.author.name + '.')

async def run_hello(message):
	await send_message(message.channel, 'Hello to you too, ' + message.author.name + '!')

async def run_myroles(message):
	roles_textified = 'Your roles:'
	for role in message.author.roles:
		roles_textified = roles_textified + '\n' + role.name.strip('@')
	await send_message(message.channel, roles_textified)
	
async def run_amiadmin(message):
	await send_message(message.channel, str(message.author.server_permissions.administrator))

client.run(load_text_from_file(get_current_directory() + '\quartermaster.apikey'))