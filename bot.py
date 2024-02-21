"""
Main bot script with commands and events.
"""
import os
import discord
import logging
from discord.ext import commands
from discord_functions import mugify_message
from image_effects import approve_image, mugify_image
from image_handling import download_image

# settings
reaction_channel_id = 1129259304868905040

# instantiates log handler object
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# instantiates discord objects
intents = discord.Intents(messages=True, members=True, guilds=True)
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='bgd.', intents=intents)

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
last_burger_message = None


# adds 'mugify' reaction to messages with images in the burger-posting channel
@bot.event
async def on_message(message: discord.Message):
    global last_burger_message

    # if in right channel, not the bot itself, and contains an image...
    if message.channel.id != reaction_channel_id:
        return
    if message.author.id == bot.application_id:
        return
    if not message.attachments:
        return

    # checking for image
    is_image = False
    if '.png' in message.attachments[0].url:
        is_image = True
    elif '.jpg' in message.attachments[0].url:
        is_image = True
    elif '.jpeg' in message.attachments[0].url:
        is_image = True

    if not is_image:
        return

    emoji = bot.get_emoji(1209922997649936424)

    last_burger_message = message
    await message.add_reaction(str(emoji))


# if the added 'mugify' reaction is pressed, mugifies the image
@bot.event
async def on_reaction_add(reaction: discord.reaction.Reaction, user):
    global last_burger_message

    # checks if the original message was reacted to by the actor
    if reaction.emoji != bot.get_emoji(1209922997649936424):
        return
    if last_burger_message is None:
        return
    if reaction.message.id != last_burger_message.id:
        return
    if user.id == bot.application_id:
        return
    if user.id != last_burger_message.author.id:
        return

    channel = bot.get_channel(reaction_channel_id)

    # processes image
    image = download_image(last_burger_message.attachments[0].url)
    await last_burger_message.delete()
    temp_msg = await channel.send(content='Mugifying...')
    mugify_image(image, 'images/mugi.png')
    await temp_msg.delete()
    await channel.send(
        content=f"{last_burger_message.author.mention}'s amazing burger!", file=discord.File('overlayed.png'))

    # cleanup
    try:
        os.remove('image.png')
    except FileNotFoundError:
        os.remove('image.jpg')
    os.remove('overlayed.png')
    last_burger_message = None

# starts bot
token = open('keys/discord_token.txt', 'r').read().strip()
bot.run(token)  # log_handler=handler, log_level=logging.DEBUG)
