"""
cipher.py — core Caesar cipher encryption and decryption logic.

Caesar Cipher — Version 3.0
"""
# ── Extended character set ────────────────────────────────────────────────────
# All printable ASCII characters that aren't letters (space through ~)
EXTRA_CHARS = [chr(c) for c in range(32, 127) if not chr(c).isalpha()]
EXTRA_LEN   = len(EXTRA_CHARS)


def caesar_cipher(text, shift, encrypt=True):
    """
    Encrypt or decrypt text using a Caesar cipher.
    Letters are shifted within their own alphabet (preserving case).
    All other printable ASCII characters are shifted within EXTRA_CHARS.
    Anything outside that set is passed through unchanged.
    """
    if not encrypt:
        shift = -shift
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        elif char in EXTRA_CHARS:
            idx = EXTRA_CHARS.index(char)
            result.append(EXTRA_CHARS[(idx + shift) % EXTRA_LEN])
        else:
            result.append(char)
    return ''.join(result)
