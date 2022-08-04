import discord
import os
from dotenv import load_dotenv

#https://discord.com/api/oauth2/authorize?client_id=1004485386564804648&permissions=2150697984&scope=bot

load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  if message.content.startswith('$telepath'):
    await message.channel.send('Alive and well.')

client.run(BOT_TOKEN)