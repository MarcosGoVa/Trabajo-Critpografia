from datetime import datetime
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

info = {
        "userid": "javi",
        "pwd_token": "b\"\\xfe\\x9by\\xf7O'\\x81\\x11\\xe5\\xc7O\\x7f^^\\xc9.B\\x9c<\\xbf-\\xf0[\\xbcs\\xa9\\x05\\xc8\\xa3-\\xd1\\x9c\"",
        "meditions": {},
        "salt": "b\"\\x0e'\\xa4\\xe7r\\x9e\\x02fw\\x92\\x7f\\xb4\\xa5\\x9d\\xa5\\xf0\""
}

salt = os.urandom(16)
print("SALT:",salt)
# derive
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
)

password = "Javier33@"

token = kdf.derive(bytes(password, "utf-8"))

print(token)

# verify
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
)
try:
    kdf.verify(bytes(password, "utf-8"), token)
    print("Se ha verificado correctamente")
except:
    print("No se ha podido verificar")