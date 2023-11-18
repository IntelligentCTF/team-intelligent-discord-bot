def count_occurences(msg: str, letter: str):
    return msg.count(letter)

def count_words(msg: str):
    return len(msg.split(' '))

def count_characters(msg: str):
    return len(msg)

def replace(msg: str, old: str, new: str):
    return msg.replace(old, new)