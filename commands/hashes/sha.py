import discord
from discord import option, ApplicationContext
from discord.ext import commands

from hashlib import sha1, sha224, sha256, sha384, sha512

def _sha1(message: str):
    try:
        return sha1(message.encode()).hexdigest()
    except:
        return ""

def _sha224(message: str):
    try:
        return sha224(message.encode()).hexdigest()
    except:
        return ""

def _sha256(message: str):
    try:
        return sha256(message.encode()).hexdigest()
    except:
        return ""

def _sha384(message: str):
    try:
        return sha384(message.encode()).hexdigest()
    except:
        return ""

def _sha512(message: str):
    try:
        return sha512(message.encode()).hexdigest()
    except:
        return ""

class SHACommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="sha1", description="Hash a message in SHA1.")
    @option("message", description="Message to be hashed in SHA1.")
    async def sha1(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{_sha1(message)}`")

    @commands.slash_command(name="sha224", description="Hash a message in SHA224.")
    @option("message", description="Message to be hashed in SHA224.")
    async def sha224(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{_sha224(message)}`")
    
    @commands.slash_command(name="sha256", description="Hash a message in SHA256.")
    @option("message", description="Message to be hashed in SHA256.")
    async def sha256(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{_sha256(message)}`")
    
    @commands.slash_command(name="sha384", description="Hash a message in SHA384.")
    @option("message", description="Message to be hashed in SHA384.")
    async def sha384(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{_sha384(message)}`")
    
    @commands.slash_command(name="sha512", description="Hash a message in SHA512.")
    @option("message", description="Message to be hashed in SHA512.")
    async def sha512(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{_sha512(message)}`")

def setup(bot):
    bot.add_cog(SHACommands(bot))