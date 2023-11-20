import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _decimal_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'd') for x in message)
    except:
        return ""

def _decimal_decode(message: str):
    try:
        return ''.join(chr(int(x, 10)) for x in message.split(' '))
    except:
        return ""

class DecimalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Decimal (base10)
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in decimal.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def decimal(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_decimal_encode(message)}`")
        return await ctx.respond(f"`{_decimal_decode(message)}`")


def setup(bot):
    bot.add_cog(DecimalCommand(bot))