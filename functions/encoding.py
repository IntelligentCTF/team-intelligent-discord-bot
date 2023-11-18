from base64 import b64encode, b64decode
from base64 import b32encode, b32decode
from base64 import b16encode, b16decode
from base64 import b85encode, b85decode
from base58 import b58encode, b58decode
import re
from prettytable import PrettyTable
from helper import b91encode, b91decode

def binary_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'b') for x in message)
    except:
        return ""

def binary_decode(message: str):
    try:
        if (len(message.split(' ')) == 1):
            # every 7 characters = 1 character
            return ''.join(chr(int(message[i:i+7], 2)) for i in range(0, len(message), 7))
        else:
            return ''.join(chr(int(x, 2)) for x in message.split(' '))
    except:
        return ""

def trinary_encode(message: str):
    try:
        return ' '.join(format(ord(x), 't') for x in message)
    except:
        return ""

def trinary_decode(message: str):
    try:
        return ''.join(chr(int(x, 3)) for x in message.split(' '))
    except:
        return ""

def octal_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'o') for x in message)
    except:
        return ""

def octal_decode(message: str):
    try:
        return ''.join(chr(int(x, 8)) for x in message.split(' '))
    except:
        return ""

def decimal_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'd') for x in message)
    except:
        return ""

def decimal_decode(message: str):
    try:
        return ''.join(chr(int(x, 10)) for x in message.split(' '))
    except:
        return ""

def hex_encode(message: str):
    try:
        return ' '.join(format(ord(x), 'x') for x in message)
    except:
        return ""

def hex_decode(message: str):
    try:
        if (len(message.split(' ')) == 1):
            # every 2 characters = 1 byte
            return ''.join(chr(int(message[i:i+2], 16)) for i in range(0, len(message), 2))
        else:
            return ''.join(chr(int(x, 16)) for x in message.split(' '))
    except:
        return ""

def base32_encode(message: str):
    try:
        return b32encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base32_decode(message: str):
    try:
        return b32decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base58_encode(message: str):
    try:
        return b58encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base58_decode(message: str):
    try:
        return b58decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base64_encode(message: str):
    try:
        return b64encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base64_decode(message: str):
    try:
        return b64decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base85_encode(message: str):
    try:
        return b85encode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base85_decode(message: str):
    try:
        return b85decode(message.encode('utf-8')).decode('utf-8')
    except:
        return ""

def base91_encode(message: str):
    try:
        return b91encode(message.encode('utf-8'))
    except:
        return ""

def base91_decode(message: str):
    try:
        return b91decode(message).decode('utf-8')
    except:
        return ""

def morse_encode(message: str):
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

def morse_decode(message: str):
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

def url_encode(message: str):
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

def url_decode(message: str):
    while "%" in message:
        message = re.sub(r"%([0-9a-fA-F]{2})", lambda x: chr(int(x.group(1), 16)), message)
    return message

def print_ascii_table():
    table_width = 6  # Set the desired number of columns
    table = ""
    for i in range(0, 128, table_width):
        row = [f"{j:3} {hex(j)} {chr(j)}" for j in range(i, min(i + table_width, 128))]
        table += " ".join(row) + "\n"
    return table

def lookup_ascii(char: str):
    if (len(char) != 1):
        return "Please enter a single character."
    
    table = PrettyTable()
    table.field_names = ["Decimal", "Hex", "Char"]
    table.add_row([ord(char), hex(ord(char)), char])
    return f"{table.get_string()}"
        