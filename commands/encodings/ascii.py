import discord
from discord import option, ApplicationContext
from discord.ext import commands

from prettytable import PrettyTable

def _print_ascii_table():
    table_width = 6  # Set the desired number of columns
    table = ""
    for i in range(0, 128, table_width):
        row = [f"{j:3} {hex(j)} {chr(j)}" for j in range(i, min(i + table_width, 128))]
        table += " ".join(row) + "\n"
    return table

def _lookup_ascii(char: str):
    if (len(char) != 1):
        return "Please enter a single character."
    
    table = PrettyTable()
    table.field_names = ["Decimal", "Hex", "Char"]
    table.add_row([ord(char), hex(ord(char)), char])
    return f"{table.get_string()}"

class AsciiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ASCII lookup
    @commands.slash_command(name="ascii", description="Lookup a character on the ASCII table.")
    @option("char", description="Character to lookup on the ASCII table.")
    async def ascii_lookup(self, ctx: ApplicationContext, char: str):
        ascii_output = _lookup_ascii(char)
        return await ctx.respond(f"```{ascii_output}```")

    # ASCII table
    @commands.slash_command(name="ascii_table", description="Print the ASCII table.")
    async def ascii_table(self, ctx: ApplicationContext):
        ascii_output = _print_ascii_table()
        return await ctx.respond(f"```{ascii_output}```")

def setup(bot):
    bot.add_cog(AsciiCommands(bot))