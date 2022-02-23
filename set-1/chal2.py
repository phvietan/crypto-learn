a = "1c0111001f010100061a024b53535009181c"
b = "686974207468652062756c6c277320657965"

a = bytes.fromhex(a)
b = bytes.fromhex(b)

c = b''
for i in range(len(a)):
    c += (a[i] ^ b[i]).to_bytes(1, 'big')

print(c)
print(c.hex())
