import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _atbash(ciphertext: str):
    plaintext = ""
    for x in ciphertext:
        if x.isalpha():
            if x.isupper():
                plaintext += chr(ord('Z') - (ord(x) - ord('A')))
            else:
                plaintext += chr(ord('z') - (ord(x) - ord('a')))
        else:
            plaintext += x
    return plaintext

class AtbashCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("ciphertext", description="Decode a message using the Atbash cipher.")
    async def atbash(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"```{_atbash(ciphertext)}```")

def setup(bot):
    bot.add_cog(AtbashCommand(bot))