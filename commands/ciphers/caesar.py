import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _caesar_brute(ciphertext: str):
    possibilities = {}
    for shift in range(26):
        try:
            caesar = ""
            for j in range(len(ciphertext)):
                if ciphertext[j].isalpha():
                    if ciphertext[j].isupper():
                        caesar += chr((ord(ciphertext[j]) + shift - 65) % 26 + 65)
                    else:
                        caesar += chr((ord(ciphertext[j]) + shift - 97) % 26 + 97)
                else:
                    caesar += ciphertext[j]
            possibilities[shift] = caesar
        except:
            pass
    return possibilities

class CaesarCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("ciphertext", description="The message to bruteforce.")
    async def caesar(self, ctx: ApplicationContext, ciphertext):
        caesar_messages = _caesar_brute(ciphertext)
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

def setup(bot):
    bot.add_cog(CaesarCommand(bot))