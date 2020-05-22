import discord
from dotenv import load_dotenv
import lookup
import os

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

async def on_message():
	if message.content.startswith('>>'):
		channel = message.channel
		spell_query = message.content[1:]
		try:
			resp = lookup.lookup(spell_query)
			await channel.send(resp)
		except Exception():
			await channel.send("Spell not found")
client.run(TOKEN)