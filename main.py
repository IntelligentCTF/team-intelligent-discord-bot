import discord
from discord import option
from discord.ext import commands
from nostril import nonsense
import os
from dotenv import load_dotenv
from functions import ciphers, encoding


# load environment variables
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

# load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.slash_command()
@option("message", description="magically crack a cipher (hopefully)")
async def crackme(ctx: discord.ApplicationContext, message):
    formula = {}
    # Ciphers
    formula["Atbash"] = ciphers.atbash(message)
    formula["ROT47"] = ciphers.rot47(message)
    formula["ROT8000"] = ciphers.rot8000(message)
    formula["ROT80000"] = ciphers.rot80000(message)
    for shift, caesar in ciphers.caesar_brute(message).items():
        formula[f"Caesar {shift}"] = caesar
    # Encodings
    formula["Base32"] = encoding.base32_decode(message)
    formula["Base58"] = encoding.base58_decode(message)
    formula["Base64"] = encoding.base64_decode(message)
    formula["Base85"] = encoding.base85_decode(message)
    formula["Base91"] = encoding.base91_decode(message)
    formula["Binary"] = encoding.binary_decode(message)
    formula["Trinary"] = encoding.trinary_decode(message)
    formula["Octal"] = encoding.octal_decode(message)
    formula["Decimal"] = encoding.decimal_decode(message)
    formula["Hexadecimal"] = encoding.hex_decode(message)
    formula["URL"] = encoding.url_decode(message)

    #print(formula)
    candidates = []
    for encoded, decoded in formula.items():
        try:
            if not nonsense(decoded):
                candidates.append(f"{encoded}: {decoded}")
        except:
            pass
    if len(candidates) == 0:
        return await ctx.respond("didn't work :<")
    return await ctx.respond("```" + "\n".join(candidates) + "```")

bot.run(TOKEN)