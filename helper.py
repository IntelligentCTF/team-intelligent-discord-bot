import subprocess
import random

DIRECTORY = '/tmp/'

def call_process(cmd: str):
    print(f"Running command: {cmd}")
    cmd = cmd.split(' ')
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = output.communicate()
    return stdout.decode(), stderr.decode()

def generate_filename(ext: str = "txt"):
    return f"{DIRECTORY}temp{random.randint(0, 1000000)}.{ext}"

def cleanup(filename: str):
    subprocess.Popen(["rm", filename])