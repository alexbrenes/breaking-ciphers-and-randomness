
import base64
from itertools import cycle, islice
from xor_shift_cipher import plaintexts_freqs, recover_plaintext


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


def split_raw_bytes(base64_str, n):
    ct = base64.b64decode(base64_str)
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


def hamming_distance(chunks, n):
    score = 0
    distances = 0
    for i in range(n):
        for j in range(i+1, n):
            distances += 1
            score += chunk_hamming_distance(chunks[i],
                                            chunks[j])  # / (8*min(len(chunks[i]), len(chunks[j])))

    return score / distances  # Average distance between chunks


def test_key_length(chunks):
    n = len(chunks)
    return hamming_distance(chunks, n)


def recover_key_length(base64_ciphertext):
    scores = []
    for i in range(2, 32):
        sp = split_raw_bytes(base64_ciphertext, i)
        score = test_key_length(sp) / i  # Normalized score
        scores.append((i, score))
    return sorted(scores, key=lambda x: x[1])


def split_ciphertext(ct, n):
    sp = []
    for i in range(0, len(ct), n):
        sp.append(ct[i:i + n])
    return sp


def print_iterable(m, sepv="\n"):
    for m_i in m:
        print(m_i, end=sepv)


def possible_keys(ct, key_lentgh):
    ct_chunks = [ct[i::key_lentgh] for i in range(key_lentgh)]
    cracks = [recover_plaintext(chunk) for chunk in ct_chunks]
    combined_score = sum(distance for distance, _, _ in cracks) / key_lentgh
    key = bytes(key for _, key, _ in cracks)
    return combined_score, key


def decrypt_v(key, ct):
    key = islice(cycle(key), len(ct))
    return bytes(a ^ b for a, b in zip(ct, key))


def main():
    key_lengths = recover_key_length(base64_ciphertext)
    ct = base64.b64decode(base64_ciphertext)
    keys = [possible_keys(ct, key)
            for key, _ in key_lengths]
    recovered_plaintext = keys[0]
    plaintext = decrypt_v(recovered_plaintext[1], ct).decode('ascii')
    print("Avg = ", recovered_plaintext[0])
    print("key = ", recovered_plaintext[1])
    print("Message = ", recovered_plaintext[2].decode('ascii'))


if __name__ == '__main__':
    main()
