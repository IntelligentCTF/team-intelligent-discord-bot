import discord
from discord import option, ApplicationContext
from discord.ext import commands

from base64 import b64encode, b64decode
from base64 import b32encode, b32decode
from base64 import b16encode, b16decode
from base64 import b85encode, b85decode
from base58 import b58encode, b58decode

# https://raw.githubusercontent.com/aberaud/base91-python/master/base91.py
import struct

base91_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
	'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
	'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
	'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$',
	'%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=',
	'>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '"']

decode_table = dict((v,k) for k,v in enumerate(base91_alphabet))

def b91decode(encoded_str):
    ''' Decode Base91 string to a bytearray '''
    v = -1
    b = 0
    n = 0
    out = bytearray()
    for strletter in encoded_str:
        if not strletter in decode_table:
            continue
        c = decode_table[strletter]
        if(v < 0):
            v = c
        else:
            v += c*91
            b |= v << n
            n += 13 if (v & 8191)>88 else 14
            while True:
                out += struct.pack('B', b&255)
                b >>= 8
                n -= 8
                if not n>7:
                    break
            v = -1
    if v+1:
        out += struct.pack('B', (b | v << n) & 255 )
    return out

def b91encode(bindata):
    ''' Encode a bytearray to a Base91 string '''
    b = 0
    n = 0
    out = ''
    for count in range(len(bindata)):
        byte = bindata[count:count+1]
        b |= struct.unpack('B', byte)[0] << n
        n += 8
        if n>13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out += base91_alphabet[v % 91] + base91_alphabet[v // 91]
    if n:
        out += base91_alphabet[b % 91]
        if n>7 or b>90:
            out += base91_alphabet[b // 91]
    return out

def _base32_encode(message: str):
    try:
        return b32encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base32_decode(message: str):
    try:
        return b32decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base58_encode(message: str):
    try:
        return b58encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base58_decode(message: str):
    try:
        return b58decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base64_encode(message: str):
    try:
        return b64encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base64_decode(message: str):
    try:
        return b64decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base85_encode(message: str):
    try:
        return b85encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base85_decode(message: str):
    try:
        return b85decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def _base91_encode(message: str):
    try:
        return b91encode(message.encode('utf-8'))
    except:
        return ""

def _base91_decode(message: str):
    try:
        return b91decode(message).decode('utf-8')
    except:
        return ""

class BaseNCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Base32
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base32.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base32(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_base32_encode(message)}`")
        return await ctx.respond(f"`{_base32_decode(message)}`")

    # Base58
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base58.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base58(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_base58_encode(message)}`")
        return await ctx.respond(f"`{_base58_decode(message)}`")
    
    # Base64
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base64.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base64(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_base64_encode(message)}`")
        return await ctx.respond(f"`{_base64_decode(message)}`")
    
    # Base85
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base85.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base85(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_base85_encode(message)}`")
        return await ctx.respond(f"`{_base85_decode(message)}`")
        
    # Base91
    @commands.slash_command()
    @option("message", description="Message to be encoded or decoded in Base91.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def base91(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_base91_encode(message)}`")
        return await ctx.respond(f"`{_base91_decode(message)}`")

def setup(bot):
    bot.add_cog(BaseNCommands(bot))