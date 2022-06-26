import base64
from itertools import cycle
from numpy import argmin
from utils import printable, english_statistical_distribution
from collections import deque

base64_ciphertext = (
    "KxRIRjMSEgMUFQkIRhIOA0YKBxEfAxRGEQcVRgdGCwcIRgkARgdGFBMB"
    "AQMCRgUJEwgSAwgHCAUDRhIOBxJGEQcVRggDEAMURgoPAQ4SAwJGBB9G"
    "B0YVCw8KA11GBQkKAkpGFQUHCBIfRgcIAkYDCwQHFBQHFRUDAkYPCEYC"
    "DxUFCRMUFQNdRgQHBQ0RBxQCRg8IRhUDCBIPCwMIEl1GCgMHCEpGCgkI"
    "AUpGAhMVEh9KRgIUAwcUH0YHCAJGHwMSRhUJCwMOCRFGCgkQBwQKA0g="
)


def xor(msg, key):
    return bytes(a ^ key for a in msg)


def compute_frequencies(p):
    total_freq = [0 for _ in range(26)]
    for c in p:
        if ord('a') <= ord(c) <= ord('z') or ord('A') <= ord(c) <= ord('Z'):
            total_freq[(ord(c) | 32) - ord('a')] += 1

    return [f/len(p) for f in total_freq]


def plaintexts_freqs(plaintexts):
    return [compute_frequencies(pt_freq) for pt_freq in plaintexts]


"""
prX: Is the probability list of X for each letter v_i in V
prY: Is the probability list of Y for each letter v_i in V
"""


def statistical_distance(X, Y):
    return sum(abs(a - b) for a, b in zip(X, Y))/2


"""
Returns the index of the plaintext with the minimum statistical distance
"""


def identify_plaintext(alphabet, plaintexts):
    return argmin([statistical_distance(alphabet, pt) for pt in plaintexts])


def recover_plaintext(ct):
    plaintexts = [printable(xor(ct, key)) for key in range(1, 256)]
    freqs = plaintexts_freqs(plaintexts)
    i = identify_plaintext(english_statistical_distribution, freqs)
    return i, plaintexts[i]


def main():
    ct = base64.b64decode(base64_ciphertext)
    recovered_plaintext = recover_plaintext(ct)
    print(recovered_plaintext[0])
    print(recovered_plaintext[1])

if __name__ == '__main__':
    main()
