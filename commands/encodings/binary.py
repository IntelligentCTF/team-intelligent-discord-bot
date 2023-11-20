import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _binary_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'b') for x in message)
    except:
        return ""

def _binary_decode(message: str):
    try:
        if (len(message.split(' ')) == 1):
            # every 7 characters = 1 character
            return ''.join(chr(int(message[i:i+7], 2)) for i in range(0, len(message), 7))
        else:
            return ''.join(chr(int(x, 2)) for x in message.split(' '))
    except:
        return ""

class BinaryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in binary.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def binary(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_binary_encode(message)}`")
        return await ctx.respond(f"`{_binary_decode(message)}`")

def setup(bot):
    bot.add_cog(BinaryCommand(bot))