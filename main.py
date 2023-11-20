import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import glob

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

@bot.event
async def on_application_command(ctx):
    print(f"{ctx.author} used {ctx.command} in {ctx.guild}")

# Load all commands
for py_file in glob.glob(f"./commands/*"):
    for py_file in glob.glob(f"{py_file}/*.py"):
        if py_file.endswith('__init__.py'):
            continue
        # Normalize the path for Pycord loader
        py_file = py_file.replace('.py', '').replace('\\', '/').replace('/', '.').replace('..', '')
        print(f"Loaded " + py_file)
        bot.load_extension(py_file)

bot.run(TOKEN)