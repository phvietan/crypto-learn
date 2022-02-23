def encrypt_xor(s: str, key: bytes) -> bytes:
    ciphertext = b''
    for i in range(len(s)):
        ciphertext += (ord(s[i]) ^ key[i % len(key)]).to_bytes(1, 'big')
    return ciphertext

c = encrypt_xor("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", b"ICE")
print(c.hex())
