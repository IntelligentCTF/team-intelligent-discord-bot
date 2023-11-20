import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _octal_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'o') for x in message)
    except:
        return ""

def _octal_decode(message: str):
    try:
        return ''.join(chr(int(x, 8)) for x in message.split(' '))
    except:
        return ""

class OctalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Octal (base8)
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in octal.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def octal(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_octal_encode(message)}`")
        return await ctx.respond(f"`{_octal_decode(message)}`")

def setup(bot):
    bot.add_cog(OctalCommand(bot))