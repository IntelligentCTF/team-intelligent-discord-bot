def caesar_brute(ciphertext: str):
    possibilities = {}
    for shift in range(26):
        try:
            caesar = ""
            for j in range(len(ciphertext)):
                if ciphertext[j].isalpha():
                    if ciphertext[j].isupper():
                        caesar += chr((ord(ciphertext[j]) + shift - 65) % 26 + 65)
                    else:
                        caesar += chr((ord(ciphertext[j]) + shift - 97) % 26 + 97)
                else:
                    caesar += ciphertext[j]
            possibilities[shift] = caesar
        except:
            pass
    return possibilities

def atbash(ciphertext: str):
    plaintext = ""
    for x in ciphertext:
        if x.isalpha():
            if x.isupper():
                plaintext += chr(ord('Z') - (ord(x) - ord('A')))
            else:
                plaintext += chr(ord('z') - (ord(x) - ord('a')))
        else:
            plaintext += x
    return plaintext

# https://inventwithpython.com/hacking/chapter21.html
# TODO: Vigenère cipher brute force
    

# https://gist.github.com/terrorbyte/7967039
def rot47(ciphertext: str):
    x = []
    for i in range(len(ciphertext)):
        j = ord(ciphertext[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(ciphertext[i])
    return ''.join(x)

def rot8000(ciphertext: str):
    y = ''
    for x in ciphertext:
            y += chr(ord(x) ^ 0x8000)
    return y

def rot80000(ciphertext: str):
    y = ''
    for x in ciphertext:
        y += chr(ord(x) ^ 0x80000)
    return y