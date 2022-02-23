def get_bit(a: int, n: int) -> int:
    return ((1 << n) & a) != 0

def hamming_byte(a: int, b: int) -> int:
    cnt = 0
    for i in range(8):
        cnt += get_bit(a, i) != get_bit(b, i)
    return cnt

def hamming(a: str, b: str) -> int:
    a_bytes = a.encode('utf-8')
    b_bytes = b.encode('utf-8')
    while len(a_bytes) < len(b_bytes): a += b'\x00'
    while len(b_bytes) < len(a_bytes): b += b'\x00'

    cnt = 0
    for i in range(len(a_bytes)):
        cnt += hamming_byte(a_bytes[i], b_bytes[i])
    return cnt

if __name__ == '__main__':
    print(hamming("this is a test", "wokka wokka!!!"))
