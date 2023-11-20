import discord
from discord import option, ApplicationContext
from discord.ext import commands
import helper

def _pycdc(file: bytes):
    # save file to disk temporarily
    filename = helper.generate_filename("pyc")
    with open(filename, "wb") as f:
        f.write(file)
    # decompile
    try:
        stdout, stderr = helper.call_process(f"pycdc {filename}")
        helper.cleanup(filename)
        return stdout
    except:
        helper.cleanup(filename)
        return "Something went wrong."

class PycdcCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    @option("file", description="Python pyc to decompile.")
    async def pycdc(self, ctx: ApplicationContext, file: discord.Attachment):
        file_data = await file.read()
        pycdc_output = _pycdc(file_data)
        if len(pycdc_output) > 2000:
            filename = generate_filename("py")
            with open(filename, "w") as f:
                f.write(pycdc_output)
            await ctx.send(file=discord.File(filename))
            cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```py\n{pycdc_output}```")
        

def setup(bot):
    bot.add_cog(PycdcCommand(bot))