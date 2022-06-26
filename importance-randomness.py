import base64

base64_ciphertext = (
    "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"
)

sequence = [487488736, 1142881612, 121804679, 3766260381, 3936115597,
            3533079714, 514960507, 3453936634, 3546284790, 566317578]


class MSWS_PRNG:
    def __init__(self, seed=0xb5ad4eceda1ce2a9):
        self.s = seed
        self.w = 0
        self.x = 0

    def _u32(self, x): return x % (1 << 32)

    def _u64(self, x): return x % (1 << 64)

    def _high(self, x): return x >> 32

    _low = _u32

    def next_int(self):
        self.w = self._u64(self.w + self.s)
        self.x = self._u64(self.x * self.x + self.w)
        self.x = (self._low(self.x) << 32) | self._high(self.x)
        return self.x


"""
(b) (1 point) To recover the plaintext from the ciphertext we will need a crib, a part
    of the plaintext that we can predict. What are typically the first 16 bytes of a
    PNG image file?
"""

"""
The first eight bytes of a PNG file indicates that the remainder of the file contains a single PNG image.
It is the PNG file signature (raw bytes):

    89 50 4e 47 0d 0a 1a 0a

The next four bytes are part of the IHDR Image Header chunk:

    00 00 00 0D

Each chunk has a four-byte chunk type field, for IHDR is:

    49 48 44 52

So the 16 bytes are:

    89 50 4e 47 0d 0a 1a 0a
    00 00 00 0D
    49 48 44 52

source:

    https://www.w3.org/TR/PNG/

"""
crib_str = "89504e470d0a1a0a0000000D49484452"
crib = bytes.fromhex(crib_str)
ct = base64.b64decode(base64_ciphertext)

print(ct[0] ^ crib[0])
print(137 ^ 204)
print(ct[0] ^ 69)


"""

"""


def main():
    pass


if __name__ == '__main__':
    main()
