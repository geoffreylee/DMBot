import discord
from dotenv import load_dotenv
import utils
import os
import re
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
	channel = message.channel
	if message.content[0:2] == ">>":
		spell_query = message.content[2:]
		try:
			resp = utils.lookup(spell_query)
			await channel.send(resp)
		except:
			await channel.send("Spell not found")

	if message.content[0:5] == "!roll":
		expression = message.content[4:]
		try:
			resp = utils.parseRoll(expression.strip())
			await channel.send(resp)
		except:
			await channel.send("Invalid expression")

client.run(TOKEN)