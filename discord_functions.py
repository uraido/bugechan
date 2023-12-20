from image_effects import mugify_image
from image_handling import download_image
import discord
import os


async def mugify_message(ctx, overlay: str):
    print('mugifying...')
    try:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        image = download_image(message.attachments[0].url)

        if image is not None:
            mugify_image(image, overlay)
            await ctx.send(file=discord.File('overlayed.png'))
            os.remove(image)
            os.remove('overlayed.png')
        else:
            await ctx.send('Invalid file type!')
    except Exception as e:
        await ctx.send('Something went wrong :(')
        print(e)
