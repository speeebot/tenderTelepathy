import discord
import pymongo
import urllib
import os
from pymongo import MongoClient
from discord.ext import commands
from dotenv import load_dotenv

#intents = discord.Intents(messages=True, guilds=True, message_content=True)
intents = discord.Intents.all()

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')

conn_username = os.getenv('CONN_USERNAME')
conn_password = os.getenv('CONN_PASSWORD')
mongo_cluster = os.getenv('MONGO_CLUSTER')
conn_string = (f"mongodb+srv://{conn_username}:" + urllib.parse.quote(conn_password) 
                + f"{mongo_cluster}")

client = MongoClient(conn_string)
db = client.tender_database 

image_cache = db.image_cache #load message cache collection from database

bot = commands.Bot(command_prefix='>', description="bad to the bone", intents=intents)

async def get_oauth_url():
    try:
        data = await bot.application_info()
    except AttributeError:
        return "Couldn't retrieve invite link."
    return discord.utils.oauth_url(data.id)

@bot.event
async def on_ready():
  url = await get_oauth_url()
  bot.oauth_url = url
  print("Use this link to invite the bot to your server: \n" + url)

#keep a stored running list of all message ids which contain images across all channels
#update db when bot comes online

#@bot.command(name='localimagecount')
#async def message_count(ctx, channel: discord.TextChannel=None):
#  channel = channel or ctx.channel
#  count = 0
#  async for message in channel.history(limit=None):
#    if message.embeds:
#      for embed in message.embeds:
#        count += 1
#    if message.attachments:
#      for attachment in message.attachments:
#        count += 1
#  await ctx.send("There are {} messages in {} which contain images".format(count, channel.mention))
    

#@bot.command(name='cachelocalimages')
#async def cache_local(ctx, channel: discord.TextChannel=None):
#  channel = channel or ctx.channel
#  count = 0
#  async for message in channel.history(limit=None):
#    if message.embeds:
#      for embed in message.embeds:
#        msg = {
#          "author": message.author.id,
#          "message_id": message.id,
#          "message_content": embed.url #might need to deal with Intents if blank
#        }
#        count += 1
#        image_cache.insert_one(msg)
#
#    if message.attachments:
#      for attachment in message.attachments:
#        msg = {
#          "author": message.author.id,
#          "message_id": message.id,
#          "message_content": attachment.url #might need to deal with Intents if blank
#        }
#        count += 1
#        image_cache.insert_one(msg)
#  await ctx.send("Cached {} messages in {}.".format(count, channel.mention))

#@bot.command(name='cacheglobalmessages')
#async def global_message_count(ctx):
#  msg = {}
#  guild_count = 0
#  for channel in ctx.guild.text_channels:
#    channel_count = 0
#    await ctx.send("Caching messages containing images in {}...".format(channel.mention))
#    async for message in channel.history(limit=None):
      #if message.embeds:
        #for embed in message.embeds:
        #  msg = {
        #    "author": message.author.id,
        #    "message_id": message.id,
        #    "message_content": embed.url #might need to deal with Intents if blank
        #  }
        #  channel_count += 1
        #  guild_count += 1
        #  image_cache.insert_one(msg)

#      if message.attachments:
#        for attachment in message.attachments:
#          msg = {
#            "author": message.author.id,
#            "message_id": message.id,
#            "message_content": attachment.url #might need to deal with Intents if blank
#          }
#          channel_count += 1
#          guild_count += 1
#          image_cache.insert_one(msg)
#    await ctx.send("There are {} messages which contain images in {}".format(channel_count, channel.mention))

@bot.command(name='throwback', description='shows a random image from discord server message history')
async def send_random_image(ctx):
  random_image = db.image_cache.aggregate([{ "$sample": { "size": 1 } }])
  for image in random_image:
    nick = bot.get_user(image['author'])
    await ctx.send("{}: {}".format(nick, image['message_content']))

@bot.listen()
async def on_message(message):
  msg = {}

  if message.embeds or message.attachments: 
    #if message.embeds: 
    #  for embed in message.embeds:
    #    print("embed")
    #    msg = {
    #      "author": message.author.id,
    #      "message_id": message.id,
    #      "message_content": embed.url #might need to deal with Intents if blank
    #    }
     #   image_cache.insert_one(msg)

    if message.attachments: 
      for attachment in message.attachments:
        #print("attach")
        msg = {
          "author": message.author.id,
          "message_id": message.id,
          "message_content": attachment.url
        }
        image_cache.insert_one(msg)

    #send notification message to bot channel
    channel = discord.utils.get(message.guild.channels, name='telepathy')
    await channel.send("cached {}'s message at {}.".format(message.author.nick, message.created_at))
    #await bot.process_commands(message)

bot.run(bot_token)