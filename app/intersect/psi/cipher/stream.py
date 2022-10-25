from .sm2 import KDF


def encrypt(secret: bytes, plaintext: bytes):
    key = KDF(secret, len(plaintext))

    int_key = int.from_bytes(key, "big")
    int_pt = int.from_bytes(plaintext, "big")

    int_ct = int_key ^ int_pt
    return int_ct.to_bytes(len(plaintext), "big")


def decrypt(secret: bytes, ciphertext: bytes):
    key = KDF(secret, len(ciphertext))

    int_key = int.from_bytes(key, "big")
    int_ct = int.from_bytes(ciphertext, "big")

    int_pt = int_key ^ int_ct
    return int_pt.to_bytes(len(ciphertext), "big")
