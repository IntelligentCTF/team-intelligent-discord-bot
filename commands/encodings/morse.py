import discord
from discord import option, ApplicationContext
from discord.ext import commands

def _morse_encode(message: str):
    morse = {
        'A':'.-', 'B':'-...', 
        'C':'-.-.', 'D':'-..', 'E':'.', 
        'F':'..-.', 'G':'--.', 'H':'....', 
        'I':'..', 'J':'.---', 'K':'-.-', 
        'L':'.-..', 'M':'--', 'N':'-.', 
        'O':'---', 'P':'.--.', 'Q':'--.-', 
        'R':'.-.', 'S':'...', 'T':'-', 
        'U':'..-', 'V':'...-', 'W':'.--', 
        'X':'-..-', 'Y':'-.--', 'Z':'--..', 
        '1':'.----', '2':'..---', '3':'...--', 
        '4':'....-', '5':'.....', '6':'-....', 
        '7':'--...', '8':'---..', '9':'----.', 
        '0':'-----', ', ':'--..--', '.':'.-.-.-', 
        '?':'..--..', '/':'-..-.', '-':'-....-', 
        '(':'-.--.', ')':'-.--.-', ' ':'/'
    }
    morse_message = ""
    message = message.upper()
    for x in message:
        try:
            morse_message += morse[x] + " "
        except:
            pass
    return morse_message

def _morse_decode(message: str):
    morse = {
        '.-':'A', '-...':'B', 
        '-.-.':'C', '-..':'D', '.':'E', 
        '..-.':'F', '--.':'G', '....':'H', 
        '..':'I', '.---':'J', '-.-':'K', 
        '.-..':'L', '--':'M', '-.':'N', 
        '---':'O', '.--.':'P', '--.-':'Q', 
        '.-.':'R', '...':'S', '-':'T', 
        '..-':'U', '...-':'V', '.--':'W', 
        '-..-':'X', '-.--':'Y', '--..':'Z', 
        '.----':'1', '..---':'2', '...--':'3', 
        '....-':'4', '.....':'5', '-....':'6', 
        '--...':'7', '---..':'8', '----.':'9', 
        '-----':'0', '--..--':', ', '.-.-.-':'.', 
        '..--..':'?', '-..-.':'/', '-....-':'-', 
        '-.--.':'(', '-.--.-':')', '/':' '
    }
    morse_message = ""
    message = message.upper()
    for x in message.split(' '):
        try:
            morse_message += morse[x]
        except:
            pass
    return morse_message

class MorseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Morse
    @commands.slash_command(name="morse", description="Encode or decode a message in Morse code.")
    @option("message", description="Message to be encoded or decoded in Morse code.")
    @option("method", description="Encode or decode", choices=["encode", "decode"])
    async def morse(self, ctx: ApplicationContext, message, method):
        if method == "encode":
            return await ctx.respond(f"`{_morse_encode(message)}`")
        return await ctx.respond(f"`{_morse_decode(message)}`")
    

def setup(bot):
    bot.add_cog(MorseCommand(bot))