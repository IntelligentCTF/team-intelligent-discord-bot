# CTF Bot
A Discord bot to help assist with common CTF tasks.

## Features
* Ciphers
    * Caesar Bruteforce
    * ATBASH
*    ROT47, ROT8000, ROT80000
* Encodings
    * Binary
    * Octal
    * Decimal
    * Hexadecimal
    * Base32, Base58, Base64, Base85, Base91
    * Morse Code
    * URL Encoding
    * ASCII Table & Lookup
* Hashes
    * MD5
    * SHA1
    * SHA256
    * SHA512
* Images
    * OCR
* Files
    * Strings
    * Hexdump
    * Metadata (EXIF)
    * .pyc Decompiler
* Strings
    * Count character occurrences
    * Count number of words
    * Count number of characters
    * Replace characters
* Magic - Automatically try different ciphers & encodings
* Slash Command Support

## Usage
### Setting up the repository
```bash
git clone
cd ctfer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuring the bot
```bash
cp .env.sample .env
nano .env
```

### Installing other dependencies
Make sure you have the binaries in your PATH

| Dependency | Purpose |
| --- | --- |
| [Tesseract](https://github.com/tesseract-ocr/tesseract) | OCR Command |
| [Decompyle++](https://github.com/zrax/pycdc) | .pyc Decompiler |

## Running the bot
```bash
python3 main.py
```

## Commands
### Ciphers
* /caesar <ciphertext>
* /atbash <ciphertext>
* /rot47 <ciphertext>
* /rot8000 <ciphertext>
* /rot80000 <ciphertext>
### Encodings
* /binary <text> [encode|decode]
* /octal <text> [encode|decode]
* /decimal <text> [encode|decode]
* /hexadecimal <text> [encode|decode]
* /base32 <text> [encode|decode]
* /base58 <text> [encode|decode]
* /base64 <text> [encode|decode]
* /base85 <text> [encode|decode]
* /base91 <text> [encode|decode]
* /morse <text> [encode|decode]
* /url <text> [encode|decode]
* /ascii_table
* /ascii_lookup <character>
### Hashes
* /md5 <text>
* /sha1 <text>
* /sha256 <text>
* /sha512 <text>
### Images
* /ocr <image>
### Files
* /strings <file> [<grep>]
* /exif <file> [<grep>]
* /hexdump <file>
* /pyc <file>
### Strings
* /occurrences <text> <character>
* /words <text>
* /characters <text>
* /replace <text> <old_string> <new_string>
### Magic
* /crackme <ciphertext>












