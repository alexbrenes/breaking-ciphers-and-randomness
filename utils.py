
def printable(bytes):
    return ''.join(chr(i) for i in list(filter(lambda x: x >= 32 and x <= 127, bytes)))
