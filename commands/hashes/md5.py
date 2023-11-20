import discord
from discord import option, ApplicationContext
from discord.ext import commands

from hashlib import md5

def _md5(message: str):
    try:
        return md5(message.encode()).hexdigest()
    except:
        return ""

class MD5Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    @option("message", description="Message to be hashed in MD5.")
    async def md5(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{_md5(message)}`")

def setup(bot):
    bot.add_cog(MD5Command(bot))