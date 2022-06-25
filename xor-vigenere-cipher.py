from ast import BitAnd
import base64
from numpy import argmin
# from bitstring import BitArray


base64_ciphertext = (
    "EjxYTxMKdwYaSBwcGTwfCBxHOwsGLRYdGwsBZSw8GhsaCncIEwdDVQM6AQ1OEzwJEWwJ"
    "FRoBUjIgIFQOFRg+B1QLHRoEJRoHCUchGEUlC1QzBBY2IypTHFIUPgcQRE8XBjoGDgYT"
    "dAcQOEUVVAMeKi43VAAUWTsIGgwDGgYxAEkZDiAARToEFxULBmUtPAAcXlk2BRhIAxob"
    "PhoHCUcyBxc7BAYQRQYqYTcdHAIWJAAaD08aEnUSSQoSORhFOwoGAA1SMTY8VAsdFTsI"
    "BhtPFBoxUwhODzUEA2BFEhsXUiMoNQAWUg0/BgEbDhsQe1MnARB0CQtsBB0GFR03NXMZ"
    "GgENdwYXCxoFDXUSSRgGJxxFIAoAVAoUZS0yGgteWSQGVAsOGxo6B0kdEzUGAWwXHRMN"
    "BmUoPVQOUjo+HQ1PHFUHPRwZHg46D0UoDAcAFxsmNWhUDQcNdw8dBg4ZGCxTCE4FPQ9F"
    "OBcVFxFSMiAgVA0dDDABAERPFBoxUxsHADwcRSULVBYEES5hPBJPBhA5EFQlDgcdNB1O"
    "HUc2CQYnRQ0VFxZkYRoaHAYYOR0YEUNVNzwHEE4vNQQJbBIVB0UUMC0/VAAUWTYZBAQG"
    "FhU7BxpOATsaRSoJDR0LFWUDIRUBBhY5STwBAxkHclMPBxUnHEUtDAYXFxMjNX1UOx1Z"
    "EAgQGw0MUyZTAwEeeEgEIQoaExYGZTU7FRtSGyIHFwBPAhUmUyEPFTsEAWwxHBsIAjYu"
    "PVhPExd3BhgMTzoGMhIHBx01HAwjC1QYBBZpYSQcAFIONhpUAwEaAztTCBwIIQYBbBEb"
    "AwtSJDJzFU8RETYZVB8HGlQ2HBwCA3QMCmwEFhsQBmUgPQ0bGhA5DlQLDhkYPB0OTgE7"
    "GkUuFxUdCwFrYRIHTxMXdwgdGh8aBiFTAB1HOgcRbAkVHQFSKjQnVAYcWTZJEAkWWVQd"
    "EhsBCzBIAiMRVBYQATxhJB0bGlknCB0MTxQCPBIdARUnSAQiAVQHCh0rYSQVHFIJPgUb"
    "HAYbE3USSQ0VNQ4RbBIdAA0dMDVzFQYWQncIGgxPGxshUwYACy1IJz4EGgAKHGUJOhgD"
    "AVkxBhgDHFlUNwYdTgg4DEUtEx0VER03Mn9UHBMOdwAaSCcUBjofDUJHNUhHLgwGEEgf"
    "JC9xVAAUWTkGVBsCFBg5UwgMDjgBETVLVDULFmUyPFQbGxcuSTkJHRwVO1QaTkUiARYl"
    "ChpWRQUkMnMVTxQYNB1PSAUAByFTCB1HdgoMK0UTHRceZ2EfAQwLXiRJLgcATlQ0HQ1C"
    "RzUbRTsMABxFEyktcxYGFVkUAAARTxQSMxIAHBR4SAQiRT0aBAciNCEVGxsWOUkHAAAA"
    "GDFTGhoGJhxFJRFUGwMUa2EdGxheWTgHVAkDGVQmBgoGRzUOAy0MBgdFCyo0cxUDBRgu"
    "GlQOBhsQdRJJTBE9Gww4CgZUChRlKTwaAABbbEkVBgtVGztTHQYOJ0gCPgQaEEUWJDhz"
    "Mw4WCjUQVAsAABgxHU4aRyAADCIOVBsDUiQvKhYAFgB3DxsaTwEcNAdJBwokBxc4BBoA"
    "RQIqMidUDQcNdyQVGgYUGntTKAADeEgEP0UdAEUFKjQ/EE8dGjQcBkgGG1QUBg4bFCBE"
    "RS0LDVQBEzxhJBsaHh13DRtETxQHdQcBDxN0ARZsBFQHBhoqLj9UGRMaNh0dBwFVGTod"
    "HQZJ"
)


def split_raw_bytes(base64_str, n=-1):
    if n <= 0:
        n = len(base64_str)
    padding = 0
    if n % 4 != 0:
        padding = abs(4 - n % 4)
    ct = base64.b64decode(base64_str.ljust(n + padding, "="))
    return [ct[i:i + n] for i in range(0, len(ct), n)]


def int_hamming_distance(a, b):
    x = a ^ b
    set_bits = 0

    while (x > 0):
        set_bits += x & 1
        x >>= 1

    return set_bits


def chunk_hamming_distance(chunk_a, chunk_b):
    length_a = len(chunk_a)
    length_b = len(chunk_b)
    distance = abs(length_a - length_b) * 8
    max_idx = min(length_a, length_b)
    for i in range(max_idx):
        distance += int_hamming_distance(chunk_a[i], chunk_b[i])
    return distance


def hamming_distance(pairs, key_length):
    score = 0
    for a, b in pairs:
        score += chunk_hamming_distance(a, b)/key_length
    return key_length, score


def test_key_length(chunks, key_length):
    n = len(chunks)
    pairs = [(chunks[i], chunks[j]) for i in range(n) for j in range(i+1, n)]
    return hamming_distance(pairs, key_length)


def recover_key_length(base64_ciphertext):
    max_key_length = len(base64_ciphertext)
    min_score = float("inf")
    key_length = float("inf")
    scores = []
    for i in range(1, max_key_length):
        sp = split_raw_bytes(base64_ciphertext, i)
        if len(sp) == 1:
            continue
        t_key_length, t_score = test_key_length(sp, i)
        scores.append((t_key_length, t_score))
        if min_score > t_score:
            key_length = t_key_length
            min_score = t_score
    return key_length, min_score, scores

key_length, min_score, scores = recover_key_length(base64_ciphertext)

print(key_length, min_score)

for s in sorted(scores, key=lambda a: a[1]):
    print(s)
# print(int_hamming_distance(539840637068609577218455531587,369307302017048399005276503216))