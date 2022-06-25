import base64
from itertools import cycle
from numpy import argmin


def xor(msg, key):
    return bytes(a.to_bytes(1, "big") ^ key.to_bytes(1, "big") for a in msg)


def compute_frequencies(p):
    freq = [0 for _ in range(max(p) + 1)]
    for c in p:
        freq[c] += 1
    return freq


def plaintexts_freqs(plaintexts):
    return [compute_frequencies(pt_freq) for pt_freq in plaintexts]


"""
prX: Is the probability list of X for each letter v_i in V
prY: Is the probability list of Y for each letter v_i in V
"""


def statistical_distance(prX, prY):
    return 1/2 * sum(abs(a - b) for a, b in zip(prX, prY))


"""
Returns the index of the plaintext with the minimum statistical distance
"""


def identify_plaintext(alphabet, plaintexts):
    return argmin([statistical_distance(alphabet, pt) for pt in plaintexts])


base64_ciphertext = (
    "KxRIRjMSEgMUFQkIRhIOA0YKBxEfAxRGEQcVRgdGCwcIRgkARgdGFBMB"
    "AQMCRgUJEwgSAwgHCAUDRhIOBxJGEQcVRggDEAMURgoPAQ4SAwJGBB9G"
    "B0YVCw8KA11GBQkKAkpGFQUHCBIfRgcIAkYDCwQHFBQHFRUDAkYPCEYC"
    "DxUFCRMUFQNdRgQHBQ0RBxQCRg8IRhUDCBIPCwMIEl1GCgMHCEpGCgkI"
    "AUpGAhMVEh9KRgIUAwcUH0YHCAJGHwMSRhUJCwMOCRFGCgkQBwQKA0g="
)

ct = base64.b64decode(base64_ciphertext)
# texto = bytes(
# "Mr. Utterson the lawyer was a man of a rugged countenance that was never lighted by a smile; cold, s", "ascii")
key = 1
plaintexts = []
for i in ct:
    print(i)
# while key < 256:
#     plaintext = xor(ct, key)
#     plaintexts.append(plaintext)
#     print(f"Key = {key}: {plaintext}")
#     key += 1
# english_statistical_distribution = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772,
#                                     0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

# print(ct)

# recovered_plaintext_idx = identify_plaintext(
#     english_statistical_distribution, pts_freqs)
# recovered_plaintext = plaintexts[recovered_plaintext_idx]
