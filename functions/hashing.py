import hashlib
import helper

def md5(message: str):
    return hashlib.md5(message.encode('utf-8')).hexdigest()

def sha1(message: str):
    return hashlib.sha1(message.encode('utf-8')).hexdigest()

def sha256(message: str):
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

def sha512(message: str):
    return hashlib.sha512(message.encode('utf-8')).hexdigest()

# https://pypi.org/project/hashID/
def identify(hash: str):
    try:
        cmd = f"hashid -mj -e {hash}"
        stdout, stderr = helper.call_process(cmd)
        return stdout
    except:
        return "Something went wrong."
        
    