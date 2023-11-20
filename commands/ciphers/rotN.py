import discord
from discord import option, ApplicationContext
from discord.ext import commands

# https://gist.github.com/terrorbyte/7967039
def _rot47(ciphertext: str):
    x = []
    for i in range(len(ciphertext)):
        j = ord(ciphertext[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(ciphertext[i])
    return ''.join(x)

def _rot8000(ciphertext: str):
    y = ''
    for x in ciphertext:
            y += chr(ord(x) ^ 0x8000)
    return y

def _rot80000(ciphertext: str):
    y = ''
    for x in ciphertext:
        y += chr(ord(x) ^ 0x80000)
    return y

class RotNCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    @option("ciphertext", description="ROT47")
    async def rot47(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"`{_rot47(ciphertext)}`")

    @commands.slash_command()
    @option("ciphertext", description="ROT8000")
    async def rot8000(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"`{_rot8000(ciphertext)}`")

    @commands.slash_command()
    @option("ciphertext", description="ROT80000")
    async def rot80000(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"`{_rot80000(ciphertext)}`")

def setup(bot):
    bot.add_cog(RotNCommand(bot))