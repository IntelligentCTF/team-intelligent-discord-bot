import random
import subprocess
import helper

DIRECTORY = "/tmp/"

def cleanup(filename: str):
    subprocess.Popen(["rm", DIRECTORY + filename])

def strings(file: bytes, grep: str = None):
    # save file to disk temporarily
    filename = f"temp{random.randint(0, 1000000)}"
    with open(DIRECTORY + filename, "wb") as f:
        f.write(file)
    
    if grep:
        try:
            strings_process = subprocess.Popen(["strings", "-n", "6", DIRECTORY + filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            grep_process = subprocess.Popen(["grep", "-i", grep], stdin=strings_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            strings_process.stdout.close()
            stdout, stderr = grep_process.communicate()
            cleanup(filename)
            return stdout.decode()
        except:
            cleanup(filename)
            return "No strings found."
    else:
        try:
            stdout, stderr = helper.call_process(f"strings -n 6 {DIRECTORY + filename}")
            cleanup(filename)
            return stdout
        except:
            cleanup(filename)
            return "Something went wrong."

def exif(file: bytes, grep: str = None):
    filename = f"temp{random.randint(0, 1000000)}"
    with open(DIRECTORY + filename, "wb") as f:
        f.write(file)
    
    if grep:
        try:
            exif_process = subprocess.Popen(["exiftool", DIRECTORY + filename], stdout=subprocess.PIPE)
            grep_process = subprocess.Popen(["grep", "-i", grep], stdin=exif_process.stdout, stdout=subprocess.PIPE)
            exif_process.stdout.close()
            stdout, stderr = grep_process.communicate()
            cleanup(filename)
            return stdout.decode()
        except:
            cleanup(filename)
            return "No exif data found."
    else:
        try:
            stdout, stderr = helper.call_process(f"exiftool {DIRECTORY + filename}")
            cleanup(filename)
            return stdout
        except:
            cleanup(filename)
            return "Something went wrong."

def hexdump(file: bytes):
    # convert bytes to hexdump
    return file.hex()

def pycdc(file: bytes):
    # save file to disk temporarily
    filename = f"temp{random.randint(0, 1000000)}"
    with open(DIRECTORY + filename, "wb") as f:
        f.write(file)
    # decompile
    try:
        stdout, stderr = helper.call_process(f"pycdc {DIRECTORY + filename}")
        cleanup(filename)
        return stdout
    except:
        cleanup(filename)
        return "Something went wrong."


    
    
    
        
    