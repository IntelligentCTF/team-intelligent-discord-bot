import discord
from discord import option, ApplicationContext
from discord.ext import commands
from functions import hashing

class HashingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("message", description="Calculate the MD5 hash of a message.")
    async def md5(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{hashing.md5(message)}`")
        
    @commands.slash_command()
    @option("message", description="Calculate the SHA256 hash of a message.")
    async def sha256(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{hashing.sha256(message)}`")

    @commands.slash_command()
    @option("message", description="Calculate the SHA512 hash of a message.")
    async def sha512(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{hashing.sha512(message)}`")

    @commands.slash_command()
    @option("message", description="Calculate the SHA1 hash of a message.")
    async def sha1(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{hashing.sha1(message)}`")

    @commands.slash_command()
    @option("hash", description="Hash to identify type of.")
    async def hashid(self, ctx: ApplicationContext, hash: str):
        hashid_output = hashing.identify(hash)
        return await ctx.respond(f"```{hashid_output}```")

def setup(bot):
    bot.add_cog(HashingCog(bot))