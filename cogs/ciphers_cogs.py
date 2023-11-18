import discord
from discord import option, ApplicationContext
from discord.ext import commands
from nostril import nonsense
from functions import ciphers

class CiphersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("ciphertext", description="The message to bruteforce.")
    async def caesar(self, ctx: ApplicationContext, ciphertext):
        caesar_messages = ciphers.caesar_brute(ciphertext)
        candidates = []
        for shift, caesar in caesar_messages.items():
            try:
                if not nonsense(caesar):
                    candidates.append(f"Shift {shift}: {caesar}")
            except:
                pass
        if len(candidates) == 0:
            return await ctx.respond("Nothing looks English, maybe a different cipher?")
        return await ctx.respond("```" + "\n".join(candidates) + "```")

    @commands.slash_command()
    @option("ciphertext", description="Decode a message using the Atbash cipher.")
    async def atbash(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"```{ciphers.atbash(ciphertext)}```")
    
    @commands.slash_command()
    @option("ciphertext", description="ROT47")
    async def rot47(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"`{ciphers.rot47(ciphertext)}`")

    @commands.slash_command()
    @option("ciphertext", description="ROT8000")
    async def rot8000(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"`{ciphers.rot8000(ciphertext)}`")

    @commands.slash_command()
    @option("ciphertext", description="ROT80000")
    async def rot80000(self, ctx: ApplicationContext, ciphertext):
        return await ctx.respond(f"`{ciphers.rot80000(ciphertext)}`")

def setup(bot):
    bot.add_cog(CiphersCog(bot))