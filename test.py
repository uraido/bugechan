import os
import discord
import logging
from discord.ext import commands
from discord_functions import mugify_message
from image_effects import approve_image
from image_handling import download_image

# instantiating discord objects
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='bgd.', intents=intents)

# tracks last burger sent on burgers channel
last_burger_message = None


@bot.event
async def on_message(message: discord.Message):
    global last_burger_message

    # if in right channel, not the bot itself, and contains an image...
    if message.channel.name != 'testes-bugechan':
        return
    if message.author.id == bot.application_id:
        return
    if not message.attachments:
        return

    last_burger_message = message
    await message.add_reaction('✅')


@bot.event
async def on_reaction_add(reaction: discord.reaction.Reaction, user):
    global last_burger_message

    if reaction.message.id != last_burger_message.id:
        return
    if user.id == bot.application_id:
        return
    if user.id != last_burger_message.author.id:
        return
    print('hooo')


token = open('keys/discord_token.txt', 'r').read().strip()
bot.run(token)
