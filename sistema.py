import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

os.environ["system_password"] = "passwordveryverysecure"
system_password = os.environ.get("system_password")
print(system_password)

class Sistema():
    @classmethod
    def generar_guardar_claves(cls, filename_priv, filename_pub):
        # Si la clave privada ya existe, simplemente cárgala
        if os.path.exists(filename_priv):
            private_key = cls.tomar_clave_privada(filename_priv)
        else:
            # Genera la clave privada si no existe
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # Serializa y guarda la clave privada en formato PEM
            pem_private = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(bytes(system_password, "utf-8"))
            )

            with open(filename_priv, 'wb') as file:
                file.write(pem_private)

        # Deriva la clave pública de la clave privada
        public_key = private_key.public_key()

        # Serializa y guarda la clave pública en formato PEM
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(filename_pub, 'wb') as file:
            file.write(pem_public)

    @classmethod
    def tomar_clave_privada(cls, filename_priv):
        with open(filename_priv, 'rb') as private_file:
            pem_private = private_file.read()
            private_key = serialization.load_pem_private_key(
                pem_private,
                password=bytes(system_password, "utf-8"),
            )
        return private_key

    @classmethod
    def tomar_clave_publica(cls, filename_pub):
        with open(filename_pub, 'rb') as public_file:
            pem_public = public_file.read()
            public_key = serialization.load_pem_public_key(pem_public)
        return public_key
