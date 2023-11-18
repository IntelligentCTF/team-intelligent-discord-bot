import discord
from discord import option, ApplicationContext
from discord.ext import commands
from functions import strings

class StringsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("message", description="Count the number of occurrences of a letter in a message.")
    @option("letter", description="The letter to count.")
    async def occurrences(self, ctx: ApplicationContext, message, letter):
        return await ctx.respond(f"`{strings.count_occurences(message, letter)}`")
        
    @commands.slash_command()
    @option("message", description="Count the number of words in a message.")
    async def words(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{strings.count_words(message)}`")

    @commands.slash_command()
    @option("message", description="Count the number of characters in a message.")
    async def characters(self, ctx: ApplicationContext, message):
        return await ctx.respond(f"`{strings.count_characters(message)}`")
    
    @commands.slash_command()
    @option("message", description="The message to replace characters in.")
    @option("old", description="The character to replace.")
    @option("new", description="The character to replace with.")
    async def replace(self, ctx: ApplicationContext, message, old, new):
        return await ctx.respond(f"`{strings.replace(message, old, new)}`")

def setup(bot):
    bot.add_cog(StringsCog(bot))