import discord
from discord import option, ApplicationContext
from discord.ext import commands
from functions import encoding

class EncodingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in binary.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def binary(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.binary_encode(message)}`")
        return await ctx.respond(f"`{encoding.binary_decode(message)}`")

    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in hexadecimal.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def hex(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.hex_encode(message)}`")
        return await ctx.respond(f"`{encoding.hex_decode(message)}`")
        
    # Trinary (base3)
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in trinary.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def trinary(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.trinary_encode(message)}`")
        return await ctx.respond(f"`{encoding.trinary_decode(message)}`")
    
    # Ternay (base3)
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in ternary.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def ternary(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.trinary_encode(message)}`")
        return await ctx.respond(f"`{encoding.trinary_decode(message)}`")
    
    # Octal (base8)
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in octal.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def octal(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.octal_encode(message)}`")
        return await ctx.respond(f"`{encoding.octal_decode(message)}`")
    
    # Decimal (base10)
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in decimal.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def decimal(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.decimal_encode(message)}`")
        return await ctx.respond(f"`{encoding.decimal_decode(message)}`")
    
    # Base32
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base32.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base32(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.base32_encode(message)}`")
        return await ctx.respond(f"`{encoding.base32_decode(message)}`")

    # Base58
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base58.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base58(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.base58_encode(message)}`")
        return await ctx.respond(f"`{encoding.base58_decode(message)}`")
    
    # Base64
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base64.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base64(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.base64_encode(message)}`")
        return await ctx.respond(f"`{encoding.base64_decode(message)}`")
    
    # Base85
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base85.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base85(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.base85_encode(message)}`")
        return await ctx.respond(f"`{encoding.base85_decode(message)}`")
        
    # Base91
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base91.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base91(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.base91_encode(message)}`")
        return await ctx.respond(f"`{encoding.base91_decode(message)}`")

    # Morse
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Morse code.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def morse(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.morse_encode(message)}`")
        return await ctx.respond(f"`{encoding.morse_decode(message)}`")
    
    # URL
    @commands.slash_command()
    @option("message", description="Message to be URL encoded or decoded.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def url(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{encoding.url_encode(message)}`")
        return await ctx.respond(f"`{encoding.url_decode(message)}`")

    # ASCII lookup
    @commands.slash_command()
    @option("char", description="Character to lookup on the ASCII table.")
    async def ascii_lookup(self, ctx: ApplicationContext, char: str):
        ascii_output = encoding.lookup_ascii(char)
        return await ctx.respond(f"```{ascii_output}```")

    # ASCII table
    @commands.slash_command()
    async def ascii_table(self, ctx: ApplicationContext):
        ascii_output = encoding.print_ascii_table()
        return await ctx.respond(f"```{ascii_output}```")

def setup(bot):
    bot.add_cog(EncodingsCog(bot))