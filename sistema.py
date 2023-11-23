import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
#Quitar variable en claro de aquí
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
    
    @classmethod
    def generar_certificate_request(cls):
        # Generate a CSR
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            # Provide various details about who we are.
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, "mysite.com"),
        ])).add_extension(
            x509.SubjectAlternativeName([
                # Describe what sites we want this certificate for.
                x509.DNSName("mysite.com"),
                x509.DNSName("www.mysite.com"),
                x509.DNSName("subdomain.mysite.com"),
            ]),
            critical=False,
        # Sign the CSR with our private key.
        ).sign(Sistema.tomar_clave_privada("sistema_privada"), hashes.SHA256())
        # Write our CSR out to disk.
        with open("CSR", "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM))
    
    @classmethod
    def verificar_certificados(cls):
        with open("Acert.pem", 'rb') as certificado_A:
            cert_A = certificado_A.read()
            #deserializar
            cert_A = x509.load_pem_x509_certificate(cert_A)
            cert_A.serial_number
        
        with open("ac1cert.pem", 'rb') as certificado_AC1:
            cert_AC1 = certificado_AC1.read()
            #deserializar
            cert_AC1 = x509.load_pem_x509_certificate(cert_AC1)
            cert_AC1.serial_number

        """#verificamos certificado de A (del sistema)
        issuer_public_key = load_pem_public_key(cert_AC1)
        issuer_public_key.verify(
            cert_A.signature,
            cert_A.tbs_certificate_bytes,
            # Depends on the algorithm used to create the certificate
            padding.PKCS1v15(),
            cert_A.signature_hash_algorithm,
        )"""
        try:
            cert_AC1.public_key().verify(
                cert_AC1.signature,
                cert_AC1.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert_AC1.signature_hash_algorithm,
            )
            cert_AC1.public_key().verify(
                cert_A.signature,
                cert_A.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert_A.signature_hash_algorithm,
            )
            print("La firma del certificado A es válida.")
            # Si la firma es válida, devolver la clave pública del certificado A
            return cert_A.public_key()
        except Exception as e:
            print(f"Error al verificar la firma del certificado A: {e}")
        return cert_A.public_key()
