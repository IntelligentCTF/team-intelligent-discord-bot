import discord
from discord import option, ApplicationContext
from discord.ext import commands

from nostril import nonsense

from commands.ciphers.atbash import _atbash
from commands.ciphers.caesar import _caesar_brute
from commands.ciphers.rotN import _rot47, _rot8000, _rot80000
from commands.encodings.baseN import _base32_decode, _base58_decode, _base64_decode, _base85_decode, _base91_decode
from commands.encodings.binary import _binary_decode
from commands.encodings.decimal import _decimal_decode
from commands.encodings.hexadecimal import _hex_decode
from commands.encodings.octal import _octal_decode
from commands.encodings.url import _url_decode


# async def crackme(ctx: discord.ApplicationContext, message):
#     formula = {}
#     # Ciphers
#     formula["Atbash"] = ciphers.atbash(message)
#     formula["ROT47"] = ciphers.rot47(message)
#     formula["ROT8000"] = ciphers.rot8000(message)
#     formula["ROT80000"] = ciphers.rot80000(message)
#     for shift, caesar in ciphers.caesar_brute(message).items():
#         formula[f"Caesar {shift}"] = caesar
#     # Encodings
#     formula["Base32"] = encoding.base32_decode(message)
#     formula["Base58"] = encoding.base58_decode(message)
#     formula["Base64"] = encoding.base64_decode(message)
#     formula["Base85"] = encoding.base85_decode(message)
#     formula["Base91"] = encoding.base91_decode(message)
#     formula["Binary"] = encoding.binary_decode(message)
#     formula["Trinary"] = encoding.trinary_decode(message)
#     formula["Octal"] = encoding.octal_decode(message)
#     formula["Decimal"] = encoding.decimal_decode(message)
#     formula["Hexadecimal"] = encoding.hex_decode(message)
#     formula["URL"] = encoding.url_decode(message)

#     #print(formula)
#     candidates = []
#     for encoded, decoded in formula.items():
#         try:
#             if not nonsense(decoded):
#                 candidates.append(f"{encoded}: {decoded}")
#         except:
#             pass
#     if len(candidates) == 0:
#         return await ctx.respond("didn't work :<")
#     return await ctx.respond("```" + "\n".join(candidates) + "```")

def _solve(message: str):
    formula = {}
    formula["Atbash"] = _atbash(message)
    formula["ROT47"] = _rot47(message)
    formula["ROT8000"] = _rot8000(message)
    formula["ROT80000"] = _rot80000(message)
    for shift, caesar in _caesar_brute(message).items():
        formula[f"Caesar {shift}"] = caesar
    formula["Base32"] = _base32_decode(message)
    formula["Base58"] = _base58_decode(message)
    formula["Base64"] = _base64_decode(message)
    formula["Base85"] = _base85_decode(message)
    formula["Base91"] = _base91_decode(message)
    formula["Binary"] = _binary_decode(message)
    formula["Octal"] = _octal_decode(message)
    formula["Decimal"] = _decimal_decode(message)
    formula["Hexadecimal"] = _hex_decode(message)
    formula["URL"] = _url_decode(message)
    
    
    candidates = []
    for encoded, decoded in formula.items():
        print(encoded, decoded)
        try:
            if not nonsense(decoded):
                candidates.append(f"{encoded}: {decoded}")
        except:
            pass
    if len(candidates) == 0:
        return "No results :("
    return "\n".join(candidates)
    

class MagicCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("message", description="Try to automatically decode a message.")
    async def magic(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"```{_solve(message)}```")

def setup(bot):
    bot.add_cog(MagicCommand(bot))