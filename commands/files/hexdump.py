import discord
from discord import option, ApplicationContext
from discord.ext import commands
import helper

def _hexdump(file: bytes):
    # convert bytes to hexdump
    return file.hex()

class HexdumpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("file", description="File to hexdump.")
    async def hexdump(self, ctx: ApplicationContext, file: discord.Attachment):
        file_data = await file.read()
        hexdump_output = _hexdump(file_data)
        if len(hexdump_output) > 2000:
            filename = helper.generate_filename()
            with open(filename, "w") as f:
                f.write(hexdump_output)
            await ctx.send(file=discord.File(filename))
            helper.cleanup(filename)
            return await ctx.respond("Too large to send text, sent as file.")
        return await ctx.respond(f"```{hexdump_output}```")


def setup(bot):
    bot.add_cog(HexdumpCommand(bot))