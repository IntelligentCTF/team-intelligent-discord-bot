import discord
from discord import option, ApplicationContext
from discord.ext import commands
from functions import images

class ImagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("image", description="Image to perform OCR on.")
    async def ocr(self, ctx: ApplicationContext, image: discord.Attachment):
        image_data = await image.read()
        ocr_text = images.ocr(image_data)
        return await ctx.respond(f"```{ocr_text}```")

def setup(bot):
    bot.add_cog(ImagesCog(bot))