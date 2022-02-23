from chal3 import bruteKey

if __name__ == "__main__":
    f = open("4.txt").read().strip().split("\n")
    mxScore = 0
    remKey = -1
    remPlain = ''
    remCipher = ''
    for l in f:
        ciphertext = bytes.fromhex(l)
        key, sc, res = bruteKey(ciphertext)
        if mxScore < sc:
            mxScore = sc
            remKey = key
            remPlain = res
            remCipher = l
    print("Ciphertext is:", remCipher)
    print("Key:", remKey)
    print("Score:", mxScore)
    print("Plain text:", remPlain.decode("utf-8"))
