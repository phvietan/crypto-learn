from typing import List
from .scorer import score_frequency

english_words = set(open('../english.txt').read().strip().split('\n')) # http://www.mieliestronk.com/corncob_lowercase.txt

def initial_potential_key(keyLength: int) -> List[List[int]]:
    result: List[List[int]] = []
    for i in range(keyLength):
        cur: List[int] = []
        for j in range(256): cur.append(j)
        result.append(cur)
    return result

def parse_to_one_length_key(ciphertext: bytes, keyLength: int) -> List[bytes]:
    arr: List[bytes] = []
    for i in range(keyLength):
        cur = []
        for iter in range(i, len(ciphertext), keyLength):
            cur.append(ciphertext[iter])
        arr.append(bytes(cur))
    return arr

def xor(s: bytes, b: int) -> bytes:
    res = []
    for c in s:
        cur = c ^ b
        res.append(cur)
    return bytes(res)

def is_char_readdable(c: int):
    return c < 128 and c >= 10

def is_string_readdable(s: bytes):
    for c in s:
        if not is_char_readdable(c):
            return False
    return True

def filter_readdable(ciphertext: bytes, potential_key: List[int]) -> List[int]:
    res = []
    for key in potential_key:
        current = xor(ciphertext, key)
        if is_string_readdable(current):
            res.append(key)
    return res

def filter_letter_and_space_frequency(ciphertext: bytes, potential_keys: List[int]) -> List[int]:
    score = []
    for key in potential_keys:
        current = xor(ciphertext, key)
        num_space, cnt_others, cnt_chars = 0, 0, [0]*26
        for c in current:
            if c == ord(' '): num_space += 1
            elif (c >= 65 and c <= 90) or (c >= 97 and c <= 122):
                if c <= 90: cnt_chars[c - 65] += 1
                else: cnt_chars[c - 97] += 1
            else:
                cnt_others += 1
        score.append(score_frequency(len(ciphertext), num_space, cnt_others, cnt_chars))

    sorted_score = sorted(score)
    best_4 = sorted_score[-4]
    res = []
    for i in range(len(potential_keys)):
        if score[i] >= best_4:
            res.append(potential_keys[i])
    return res

def xor_str(a, b):
    res = []
    for i in range(len(a)):
        cur = a[i] ^ b[i]
        res.append(cur)
    return bytes(res)

def count_english(decrypted: List[bytes]) -> int:
    global english_words
    decodeDecrypted = ''
    for val in decrypted:
        decodeDecrypted += ' ' + val.decode('utf-8')
    decodeDecrypted = decodeDecrypted[1:]

    decodeDecrypted = decodeDecrypted.replace('\n', ' ')
    decodeDecrypted = decodeDecrypted.split(' ')
    cnt = 0
    for val in decodeDecrypted:
        if val.strip().lower() in english_words: cnt += 1
    return cnt

def decrypt_part(ciphertext: bytes, key: List[int], start_idx: int, keyLength: int) -> List[bytes]:
    res = []
    for i in range(start_idx, len(ciphertext), keyLength):
        current = xor_str(ciphertext[i : i+len(key)], key)
        res.append(current)
    return res

keys = []
dequy_keys: List[int] = []
stored_dequy_keys = []
max_num_english_words = -1
potential_key = [[]]
def dq(ciphertext: bytes, start_idx, current, keyLength: int):
    global keys, dequy_keys, stored_dequy_keys, max_num_english_words, potential_key
    if current == start_idx + 7 or current == keyLength:
        decrypted = decrypt_part(ciphertext, dequy_keys, start_idx, keyLength)
        cnt = count_english(decrypted)
        if cnt > max_num_english_words:
            stored_dequy_keys = dequy_keys.copy()
            max_num_english_words = cnt
        return
    dequy_keys.append(0)
    for key in potential_key[current]:
        dequy_keys[-1] = key
        dq(ciphertext, start_idx, current+1, keyLength)
    dequy_keys.pop()

def decrypt(ciphertext: bytes, key: List[int]):
    message = []
    for i in range(len(ciphertext)):
        current = ciphertext[i] ^ key[i % len(key)]
        message.append(current)
    return bytes(message)

def count_possible_keys(potential_key: List[List[int]]):
    possibilities = 1
    for key in potential_key:
        possibilities *= len(key)
    return possibilities

def solve_with_key_length(keyLength: int, ciphertext: bytes, debug = False):
    global keys, dequy_keys, stored_dequy_keys, max_num_english_words, potential_key

    try:
        potential_key = initial_potential_key(keyLength)

        if debug:
            print("Initializing all possibilities that key can be")
            print("Number of possible keys = %d\n" % count_possible_keys(potential_key))
            print("Reformat ciphertext, now we only need to deal with key of size 1 (and solve %d times individually)" % keyLength)

        arr = parse_to_one_length_key(ciphertext, keyLength)

        if debug: print("Apply first filter: only take keys that produce readdable output")
        for i in range(keyLength):
            newPotential = filter_readdable(arr[i], potential_key[i])
            if len(newPotential) != len(potential_key[i]):
                potential_key[i] = newPotential
        if debug:
            print("Number of possible keys after first filter = %d\n" % count_possible_keys(potential_key))
            print("Apply second filter: use statistical scoring based on number of space, number of characters in english")

        for i in range(keyLength):
            potential_key[i] = filter_letter_and_space_frequency(arr[i], potential_key[i])

        if debug:
            print("Number of possible keys after second filter = %d\n" % count_possible_keys(potential_key))
            print("Now it should be easy enough, try to bruteforce the key and count number of english in sentence")
            print("I bruteforce the key for each 7 bytes")

        keys = []
        dequy_keys = []
        stored_dequy_keys = []
        max_num_english_words = -1
        while len(keys) < keyLength:
            max_num_english_words, dequy_keys, stored_dequy_keys = -1, [], []
            dq(ciphertext, len(keys), len(keys), keyLength)
            keys.extend(stored_dequy_keys)
            if debug: print("Keys =", keys, len(keys))
        if debug:
            print("Done reproduce keys")
        message = decrypt(ciphertext, keys)
        return message.decode("utf-8")
    except Exception as e:
        # raise e
        print("Can't do")
        return None
