from typing import Tuple

c = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
c = bytes.fromhex(c)

# Score that look like a english sentence
engs = open("../english.txt").read().strip().split('\n')
def score(decrypted: bytes):
    cnt_readable = 0
    eng_cnt = 0
    for v in decrypted:
        cnt_readable += (v >= 48 and v <= 126)

    try:
        decrypted_utf8 = decrypted.decode('utf-8')
        for e in engs:
            eng_cnt += (e in decrypted_utf8)
        return cnt_readable + eng_cnt * 5
    except:
        return 0

def decrypt(cipher: bytes, key: int) -> bytes:
    decrypted = b''
    for v in cipher:
        decrypted += (v ^ key).to_bytes(1, 'big')
    return decrypted

def bruteKey(ciphertext: bytes) -> Tuple[int, int, bytes]:
    mxScore = 0
    remKey = -1
    remResult = b''
    for key in range(256):
        b = decrypt(ciphertext, key)
        sc = score(b)
        if mxScore < sc:
            mxScore = sc
            remKey = key
            remResult = b
    return remKey, mxScore, remResult

if __name__ == "__main__":
    key, sc, res = bruteKey(c)
    print("Key is:", key)
    print("Score is:", sc)
    print("Plaintext is:", res.decode("utf-8"))
