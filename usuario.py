import json
import pickle
import base64
import os
from sistema import Sistema
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from file_manager import FileManager
from data.password import Password
from data.username import Username
from data.sugar import Sugar
from data.date import Date

Sistema.generar_guardar_claves("sistema_privada","sistema_publico")


class Usuario:
    def __init__(self,nombre,contraseña):
        self.nombre = nombre
        self.contraseña =  contraseña
    

    @classmethod
    def register_app(cls, user_in, password_in) -> int:
        file_manager = FileManager()
        
        database = file_manager.load("database.json")

        # Comprobamos que la contraseña sea válida -> Decision de diseño antes del bucle para ahorrar
        try:
            password = Password(password_in).value
        except:
            return -1
            
        try:
            user = Username(user_in).value
        except:
            return -2
        
        # Buscamos si el usuario ya está registrado
        for i in database:
            if i["userid"] == user:
                print("-El usuario ya está registrado")
                return -3
        
        # Crear token de usuario
        salt = os.urandom(16)
        # derive
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
        )
        token = kdf.derive(bytes(password, "utf-8")) #Lo pasamos a bytes y creamos el token
        token_64 = base64.b64encode(token).decode("utf-8") #Pasamos el token a base 64 para poder introducirlo en el json
        salt_64 = base64.b64encode(salt).decode("utf-8") #Pasamos el salt a base 64 para poder introducirlo en el json

        # Crear nonce y key para chacha20Poly1305
        nonce = os.urandom(12) #Creamos el nonce
        nonce_64 = base64.b64encode(nonce).decode("utf-8") #Pasamos el nonce a base 64 para poder introducirlo en el json


        #Si no está registrado, lo registramos
        database.append({"userid":user,"pwd_token":token_64,"meditions":"", "salt":salt_64,
                         "nonce":nonce_64})
        
        # Guardamos los cambios
        file_manager.save(database,"database.json")
        
        return 0

    
    @classmethod
    def login_app(cls, user, password):
        file_manager = FileManager()
        
        database = file_manager.load("database.json")

        #Buscamos si el usuario ya está registrado
        for user_info in database:
            if user_info["userid"] == user:
                # verify
                salt_bytes = base64.b64decode(user_info["salt"]) #Pasamos el base 64 que hay en el json a bytes para poder verificar
                token_bytes = base64.b64decode(user_info["pwd_token"])

                kdf = Scrypt(
                    salt=salt_bytes,
                    length=32,
                    n=2**14,
                    r=8,
                    p=1,
                )
                try:
                    kdf.verify(bytes(password, "utf-8"), token_bytes)
                    pbkdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt_bytes,
                        iterations=100000,  
                    )
                    key_token = pbkdf.derive(bytes(password, "utf-8"))
                    user_info["key_token"] = base64.b64encode(key_token).decode("utf-8") ## ¡¡ESTO NO VA A LA BASE DE DATOS; ESTÁ "VIVO" EN LA SESIÓN DE USUARIO  
                    # decrypt meditions
                    if user_info["meditions"] == "":
                        user_info["meditions"] = {}
                    else:
                        # Decrypt meditions
                        meditions_encrypted_64 = user_info["meditions"]
                        meditions_encr_bytes = base64.b64decode(meditions_encrypted_64)
                        nonce = base64.b64decode(user_info["nonce"])
                        
                        chacha = ChaCha20Poly1305(key_token)
                        decrypted_meditions = chacha.decrypt(nonce, meditions_encr_bytes, None) #El except se tira en esta línea
                        meditions_64 = base64.b64encode(decrypted_meditions).decode("utf-8")

                        # serializado a dict
                        meditions_bytes = base64.b64decode(meditions_64)                     # pasarlo de base64 -> bytes
                        meditions_dict = pickle.loads(meditions_bytes)                       # pasarlo de bytes -> dict
                        print(meditions_dict)
                        user_info["meditions"] = meditions_dict


                        # Nuevo nonce
                        nonce = os.urandom(12) #Creamos el nonce
                        nonce_64 = base64.b64encode(nonce).decode("utf-8") #Pasamos el nonce a base 64 para poder introducirlo en el json
                        user_info["nonce"] = nonce_64
                    
                        # Nuevo salt y nuevo token de password
                        salt_new = os.urandom(16)
                        # derive
                        kdf = Scrypt(
                            salt=salt_new,
                            length=32,
                            n=2**14,
                            r=8,
                            p=1,
                        )

                        pbkdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt_new,
                        iterations=100000,  
                    )
                        new_key_token = pbkdf.derive(bytes(password, "utf-8"))
                        user_info["key_token"] = base64.b64encode(new_key_token).decode("utf-8") ## ¡¡ESTO NO VA A LA BASE DE DATOS; ESTÁ "VIVO" EN LA SESIÓN DE USUARIO  



                        pwd_token = kdf.derive(bytes(password, "utf-8")) #Lo pasamos a bytes y creamos el token
                        pwd_token_64 = base64.b64encode(pwd_token).decode("utf-8") #Pasamos el token a base 64 para poder introducirlo en el json
                        salt_64 = base64.b64encode(salt_new).decode("utf-8") #Pasamos el salt a base 64 para poder introducirlo en el json
                        user_info["salt"] = salt_64
                        user_info["pwd_token"] = pwd_token_64
                        


                        
                    return user_info
                except:
                    print("-Contraseña incorrecta")
                    return -1
                         
        print("-El usuario no está registrado")
        return -2
    

    @classmethod
    def solicitar_informe_usuario(cls,user_info):
        clave_privada = Sistema.tomar_clave_privada("sistema_privada")
        mensaje_a_firmar={
            "usuario":user_info["userid"],
            "meditions":user_info["meditions"]
        }
        mensaje_a_firmar_bytes = pickle.dumps(mensaje_a_firmar)   #mensaje en bytes
        #mensaje_a_firmar_base64 = base64.b64encode(mensaje_a_firmar_bytes).decode("utf-8")
        print(mensaje_a_firmar)
        #sistema firma
        signature = clave_privada.sign(
            mensaje_a_firmar_bytes,
            padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
        )
        with open("firma"+user_info["userid"], 'wb') as file:
            file.write(signature)

        with open("mensaje"+user_info["userid"], 'wb') as file:
            file.write(mensaje_a_firmar_bytes)

   
    @classmethod
    def comprobar_informe_usuario(cls, firma, mensaje) -> bool:
        
        #obtengo la firma (del cliente)
        #with open("firma", 'rb') as file:
        #    firma = file.read()
        #obtengo el mensaje a firmar
        #with open("mensaje", 'rb') as file:
        #    mensaje = mensaje.read()

        #sistema verifica
        clave_publica = Sistema.tomar_clave_publica("sistema_publico")
        try: 
            clave_publica.verify(
                firma,
                mensaje,
                padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                    ),
                hashes.SHA256()
            )
            return True
        except:
            return False


    @classmethod
    def new_medition_app(cls, user_new_data,new_day,new_medition) -> None:
        
        try:
            new_day = Date(new_day).value
        except:
            return -1

        try:
            new_medition = Sugar(new_medition).value
        except:
            return -2
 
        print(new_day) 
        user_new_data["meditions"][new_day] = new_medition
        print(user_new_data["meditions"])


        file_manager = FileManager()

        database = file_manager.load("database.json")

        for user in database:
            if user["userid"] == user_new_data["userid"]:
                user["meditions"] = user_new_data["meditions"]
                break

        file_manager.save(database, "database.json")
        print("-Medición guardada")
        return

    @classmethod
    def log_out_app(cls, user_info):
        print(user_info["key_token"])
        meditions_old = user_info["meditions"]
        
        nonce = base64.b64decode(user_info["nonce"]) #Pasamos el nonce a bytes
        # serializar
        meditions_bytes = pickle.dumps(meditions_old)                                     # pasarlo de dict -> bytes                 # pasarlo de bytes -> base64
        
        # chacha encrypt
        key_token = base64.b64decode(user_info["key_token"])   ## ¡¡ESTO NO VA A LA BASE DE DATOS; ESTÁ "VIVO" EN LA SESIÓN DE USUARIO!!
        chacha = ChaCha20Poly1305(key_token)
        encrypted_bytes = chacha.encrypt(nonce, meditions_bytes, None)

        # encrypted dictionary to 64
        meditions_encrypted = base64.b64encode(encrypted_bytes).decode("utf-8")
        user_info["meditions"] = meditions_encrypted

        file_manager = FileManager()
        database = file_manager.load("database.json")

        for user in database:
            if user["userid"] == user_info["userid"]:
                user["meditions"] = user_info["meditions"]
                user["nonce"] = user_info["nonce"]
                user["salt"] = user_info["salt"]
                user["pwd_token"] = user_info["pwd_token"]
                break
        
        file_manager.save(database, "database.json")
        print("-Sesión cerrada")
        return



