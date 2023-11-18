import discord
from discord import option, ApplicationContext
from discord.ext import commands
from functions import files
import random

class FilesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("file", description="File to perform strings on.")
    @option("grep", description="Filter strings output (optional)", required=False)
    async def strings(self, ctx: ApplicationContext, file: discord.Attachment, grep: str = None):
        file_data = await file.read()
        strings_output = files.strings(file_data, grep)
        if len(strings_output) > 2000:
            filename = f"{random.randint(0, 100000000)}.txt"
            with open(files.DIRECTORY + filename, "w") as f:
                f.write(strings_output)
            await ctx.send(file=discord.File(files.DIRECTORY + filename))
            files.cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```{strings_output}```")

    @commands.slash_command()
    @option("file", description="File to perform exiftool on.")
    @option("grep", description="Filter strings output (optional)", required=False)
    async def exif(self, ctx: ApplicationContext, file: discord.Attachment, grep: str = None):
        file_data = await file.read()
        exif_output = files.exif(file_data, grep)
        if len(exif_output) > 2000:
            filename = f"{random.randint(0, 100000000)}.txt"
            with open(files.DIRECTORY + filename, "w") as f:
                f.write(exif_output)
            await ctx.send(file=discord.File(files.DIRECTORY + filename))
            files.cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```{exif_output}```")

    @commands.slash_command()
    @option("file", description="File to hexdump.")
    async def hexdump(self, ctx: ApplicationContext, file: discord.Attachment):
        file_data = await file.read()
        hexdump_output = files.hexdump(file_data)
        if len(hexdump_output) > 2000:
            filename = f"{random.randint(0, 100000000)}.txt"
            with open(files.DIRECTORY + filename, "w") as f:
                f.write(hexdump_output)
            await ctx.send(file=discord.File(files.DIRECTORY + filename))
            files.cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```{hexdump_output}```")
    
    @commands.slash_command()
    @option("file", description="Python pyc to decompile.")
    async def pycdc(self, ctx: ApplicationContext, file: discord.Attachment):
        file_data = await file.read()
        pycdc_output = files.pycdc(file_data)
        if len(pycdc_output) > 2000:
            filename = f"{random.randint(0, 100000000)}.py"
            with open(files.DIRECTORY + filename, "w") as f:
                f.write(pycdc_output)
            await ctx.send(file=discord.File(files.DIRECTORY + filename))
            files.cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```py\n{pycdc_output}```")
        

def setup(bot):
    bot.add_cog(FilesCog(bot))