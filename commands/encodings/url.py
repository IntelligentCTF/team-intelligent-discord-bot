import discord
from discord import option, ApplicationContext
from discord.ext import commands

import re

def _url_encode(message: str):
    mapping = {
        "%": "%25",
        ":": "%3A",  "/": "%2F", "?": "%3F",
        "#": "%23", "[": "%5B", "]": "%5D",
        "@": "%40", "!": "%21", "$": "%24",
        "&": "%26", "'": "%27", "(": "%28",
        ")": "%29", "*": "%2A", "+": "%2B",
        ",": "%2C", ";": "%3B", "=": "%3D",
        " ": "+", "\\": "%5C", "<": "%3C",
        ">": "%3E", "^": "%5E", "`": "%60", 
        "{": "%7B", "}": "%7D", "|": "%7C", 
        '"': "%22", "~": "%7E"
    }
    for char, code in mapping.items():
        message = message.replace(char, code)
    return message

def _url_decode(message: str):
    while "%" in message:
        message = re.sub(r"%([0-9a-fA-F]{2})", lambda x: chr(int(x.group(1), 16)), message)
    return message

class URLCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # URL
    @commands.slash_command(name="url", description="Encode or decode a message in URL encoding.")
    @option("message", description="Message to be URL encoded or decoded.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def url(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_url_encode(message)}`")
        return await ctx.respond(f"`{_url_decode(message)}`")

def setup(bot):
    bot.add_cog(URLCommand(bot))