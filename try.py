import os, pickle
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
data = {"userid":"user","password":"password"}
data = pickle.dumps(data)
print(data)
print(pickle.loads(data))    #de bytes a string
aad = b"authenticated but unencrypted data"
key = ChaCha20Poly1305.generate_key()
chacha = ChaCha20Poly1305(key)
nonce = os.urandom(12)
ct = chacha.encrypt(nonce, data, aad)
print(ct)
decrypted = chacha.decrypt(nonce, ct, aad)
decrypted_str = decrypted.decode("utf-8")
print(decrypted)
print(decrypted_str)