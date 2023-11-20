import discord
from discord import option, ApplicationContext
from discord.ext import commands
import helper

import subprocess

def _exif(file: bytes, grep: str = None):
    filename = helper.generate_filename()
    with open(filename, "wb") as f:
        f.write(file)
    
    if grep:
        try:
            exif_process = subprocess.Popen(["exiftool", filename], stdout=subprocess.PIPE)
            grep_process = subprocess.Popen(["grep", "-i", grep], stdin=exif_process.stdout, stdout=subprocess.PIPE)
            exif_process.stdout.close()
            stdout, stderr = grep_process.communicate()
            helper.cleanup(filename)
            return stdout.decode()
        except:
            helper.cleanup(filename)
            return "No exif data found."
    else:
        try:
            stdout, stderr = helper.call_process(f"exiftool {filename}")
            helper.cleanup(filename)
            return stdout
        except:
            helper.cleanup(filename)
            return "Something went wrong."

class ExifCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("file", description="File to perform exiftool on.")
    @option("grep", description="Filter strings output (optional)", required=False)
    async def exif(self, ctx: ApplicationContext, file: discord.Attachment, grep: str = None):
        file_data = await file.read()
        exif_output = _exif(file_data, grep)
        if len(exif_output) > 2000:
            filename = generate_filename()
            with open(filename, "w") as f:
                f.write(exif_output)
            await ctx.send(file=discord.File(filename))
            cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```{exif_output}```")

def setup(bot):
    bot.add_cog(ExifCommand(bot))