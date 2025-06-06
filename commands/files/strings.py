import discord
from discord import option, ApplicationContext
from discord.ext import commands
import helper

import subprocess

def _strings(file: bytes, grep: str = None):
    # save file to disk temporarily
    filename = helper.generate_filename()
    with open(filename, "wb") as f:
        f.write(file)
    
    if grep:
        try:
            strings_process = subprocess.Popen(["strings", "-n", "6", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            grep_process = subprocess.Popen(["grep", "-i", grep], stdin=strings_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            strings_process.stdout.close()
            stdout, stderr = grep_process.communicate()
            helper.cleanup(filename)
            return stdout.decode()
        except:
            helper.cleanup(filename)
            return "No strings found."
    else:
        try:
            stdout, stderr = helper.call_process(f"strings -n 6 {filename}")
            helper.cleanup(filename)
            return stdout
        except:
            helper.cleanup(filename)
            return "Something went wrong."

class StringsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="strings", description="Perform strings on a file.")
    @option("file", description="File to perform strings on.")
    @option("grep", description="Filter strings output (optional)", required=False)
    async def strings(self, ctx: ApplicationContext, file: discord.Attachment, grep: str = None):
        file_data = await file.read()
        strings_output = _strings(file_data, grep)
        if len(strings_output) > 2000:
            filename = helper.generate_filename()
            with open(filename, "w") as f:
                f.write(strings_output)
            await ctx.send(file=discord.File(filename))
            helper.cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```{strings_output}```")
        
def setup(bot):
    bot.add_cog(StringsCommand(bot))