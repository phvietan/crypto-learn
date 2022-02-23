import base64
from typing import Any
from chal6folder.a import solve_with_key_length
from chal6folder.hamming import hamming

c = open("chal6folder/6.txt").read().replace("\n", "").strip()
c = base64.b64decode(c)

def potential_key_sizes(ciphertext: bytes):
    potential = []
    for keyLength in range(1, 50):
        first = ciphertext[0:keyLength].decode("ascii")
        second = ciphertext[keyLength:keyLength*2].decode("ascii")
        potential.append({
            "keyLength": keyLength,
            "hamming": hamming(first, second) / keyLength,
        })
    def sort_by_key(list: Any):
        return list['hamming']
    potential = sorted(potential, key=sort_by_key)
    print(potential)
    return potential

p = potential_key_sizes(c)

for v in p:
    res = solve_with_key_length(v["keyLength"], c, True)
    if res != None:
        print(v["keyLength"])
        print(res)

# solve_with_key_length(17, c, True)
