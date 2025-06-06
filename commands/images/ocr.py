import discord
from discord import option, ApplicationContext
from discord.ext import commands

from PIL import Image
import pytesseract
import io

def _ocr(image_data: bytes):
    try:
        image = Image.open(io.BytesIO(image_data))
        return pytesseract.image_to_string(image)
    except Exception as e:
        return str(e)

class OCRCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ocr", description="Perform OCR on an image.")
    @option("image", description="Image to perform OCR on.")
    async def ocr(self, ctx: ApplicationContext, image: discord.Attachment):
        image_data = await image.read()
        ocr_text = _ocr(image_data)
        return await ctx.respond(f"```{ocr_text}```")

def setup(bot):
    bot.add_cog(OCRCommand(bot))