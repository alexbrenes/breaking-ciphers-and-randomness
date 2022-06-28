import base64
from itertools import cycle
from utils import english_statistical_distribution
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


def compute_frequencies(ct, n):
    return [ct.count(b) / n for b in range(256)]


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
    min_dist = float("inf")
    idx = -1
    for i, pt in enumerate(plaintexts):
        temp = statistical_distance(alphabet, pt)
        if temp <= min_dist:
            min_dist = temp
            idx = i
    return idx


def recover_plaintext(ct):
    n = len(ct)
    freqs = compute_frequencies(ct, n)
    min_dist = float("inf")
    min_key = 0
    for key in range(1, 256):
        distance = 0
        for i, frequence in enumerate(english_statistical_distribution):
            distance += abs(frequence -
                            freqs[(i+ord('a')) ^ key])
        if min_dist > distance:
            min_dist = distance
            min_key = key
    plaintext = xor(ct, min_key)
    return min_dist, min_key, plaintext


def main():
    ct = base64.b64decode(base64_ciphertext)
    recovered_plaintext = recover_plaintext(ct)
    print("Avg = ", recovered_plaintext[0])
    print("key = ", recovered_plaintext[1])
    print("Message = ", recovered_plaintext[2].decode('ascii'))


if __name__ == '__main__':
    main()
