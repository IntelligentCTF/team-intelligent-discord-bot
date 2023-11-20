import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _hex_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'x') for x in message)
    except:
        return ""

def _hex_decode(message: str):
    try:
        if (len(message.split(' ')) == 1):
            # every 2 characters = 1 byte
            return ''.join(chr(int(message[i:i+2], 16)) for i in range(0, len(message), 2))
        else:
            return ''.join(chr(int(x, 16)) for x in message.split(' '))
    except:
        return ""

class HexadecimalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in hexadecimal.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def hex(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_hex_encode(message)}`")
        return await ctx.respond(f"`{_hex_decode(message)}`")

def setup(bot):
    bot.add_cog(HexadecimalCommand(bot))