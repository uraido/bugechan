"""
Main bot script with commands and events.
"""
import os
import discord
import logging
from discord.ext import commands
from discord_functions import mugify_message
from image_effects import approve_image
from image_handling import download_image

# instantiates log handler object
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# instantiates discord objects
intents = discord.Intents(messages=True, members=True, guilds=True)
intents.message_content = True
bot = commands.Bot(command_prefix='bg.', intents=intents)

# -------------------------------- COMMANDS


@bot.command()
async def mugify(ctx):
    await mugify_message(ctx, 'images/mugi.png')


@bot.command()
async def mugify2(ctx):
    await mugify_message(ctx, 'images/mugi2.png')


@bot.command()
async def approve(ctx):
    print('mugifying...')
    try:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        image = download_image(message.attachments[0].url)

        if image is not None:
            approve_image(image)
            await ctx.send(file=discord.File('overlayed.png'))
            os.remove(image)
            os.remove('overlayed.png')
        else:
            await ctx.send('Invalid file type!')
    except Exception as e:
        await ctx.send('Something went wrong :(')
        print(e)

# -------------------------------- EVENTS

# join server
@bot.event
async def on_member_join(member):
    from image_effects import mugify_image

    # proccess image
    image = download_image(member.avatar.url)
    mugify_image(image, 'images/mugi.png')
    file = discord.File('overlayed.png', filename='overlayed.png')

    # create embed
    embed = discord.Embed(title=f'{member.name} is tasty 😋', color=16098851)
    embed.set_image(url="attachment://overlayed.png")

    # get welcome channel
    channel = bot.get_channel(1129245891723796530)

    # send message
    await channel.send(file=file, embed=embed)

    # cleanup
    os.remove('image.png')
    os.remove('overlayed.png')


# leave server
@bot.event
async def on_raw_member_remove(payload):
    # create embed
    embed = discord.Embed(title=f'{payload.user.name} became vegan 🤮', colour=5111634)
    embed.set_image(url='https://cdn.discordapp.com/attachments/1129220202140291165/1129247524176285696/Vegan-Caesar-Braai-Salad-e1688121116658.png?ex=65e14636&is=65ced136&hm=83117be3a131065e6781680ead6c959b0883702ade785fd40bdf0e7b1e30cfac&')

    # get welcome channel
    channel = bot.get_channel(1129245891723796530)

    # send message
    await channel.send(embed=embed)

# add reaction stuff
'''last_burger_message = None


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

    if last_burger_message is None:
        return
    if reaction.message.id != last_burger_message.id:
        return
    if user.id == bot.application_id:
        return
    if user.id != last_burger_message.author.id:
        return

    last_burger_message = None
    print('hooo')'''


# starts bot
token = open('keys/discord_token.txt', 'r').read().strip()
bot.run(token)  # log_handler=handler, log_level=logging.DEBUG)
