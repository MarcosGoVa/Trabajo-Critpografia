import json
import pickle
import base64
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from file_manager import FileManager
from data.password import Password
from data.username import Username
from data.sugar import Sugar
from data.date import Date



class Usuario:
    def __init__(self,nombre,contraseña):
        self.nombre = nombre
        self.contraseña =  contraseña
    """"
    @classmethod
    def register(cls):
        user = str(input("-Introduzca su usuario: "))
        password_in = str(input("-Introduzca su contraseña: "))
        password = Password(password_in)
        file_manager = FileManager()
        
        database = file_manager.load("database.json")
            
        #Buscamos si el usuario ya está registrado
        for i in database:
            if i["userid"] == user:
                print("-El usuario ya está registrado")
                return
        
        #Si no está registrado, lo registramos
        database.append({"userid":user,"password":password,"meditions":{}})
        
        # Guardamos los cambios
        file_manager.save(database,"database.json")
        
        print("-Usuario registrado")
    """

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
        token = kdf.derive(bytes(password, "utf-8"))
        token_64 = base64.b64encode(token).decode("utf-8")
        salt_64 = base64.b64encode(salt).decode("utf-8")

        # Crear nonce y key para chacha20Poly1305
        key = ChaCha20Poly1305.generate_key()
        nonce = os.urandom(12)
        key_64 = base64.b64encode(key).decode("utf-8")
        nonce_64 = base64.b64encode(nonce).decode("utf-8")


        #Si no está registrado, lo registramos # TODO: meditions como string
        database.append({"userid":user,"pwd_token":token_64,"meditions":"", "salt":salt_64,
                         "key":key_64, "nonce":nonce_64})
        
        # Guardamos los cambios
        file_manager.save(database,"database.json")
        
        return 0

    """
    @classmethod
    def login(cls):
        user = str(input("-Introduzca su usuario: "))
        password = str(input("-Introduzca su contraseña: "))
        file_manager = FileManager()
        
        database = file_manager.load("database.json")

        #Buscamos si el usuario ya está registrado
        for user_info in database:
            if user_info["userid"] == user:
                if user_info["password"] == password:
                    print("-Bienvenido al sistema ", user_info["userid"])
                    return user_info
                print("-Contraseña incorrecta")
                return
        
        print("-El usuario no está registrado")
        return
    """
    
    @classmethod
    def login_app(cls, user, password):
        file_manager = FileManager()
        
        database = file_manager.load("database.json")

        #Buscamos si el usuario ya está registrado
        for user_info in database:
            if user_info["userid"] == user:
                # verify
                salt_bytes = base64.b64decode(user_info["salt"])
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
                    # decrypt meditions
                    if user_info["meditions"] == "":
                        user_info["meditions"] = {}
                    else:
                        meditions_encrypted_64 = user_info["meditions"]
                        meditions_encr_bytes = base64.b64decode(meditions_encrypted_64)
                        nonce = base64.b64decode(user_info["nonce"])
                        key = base64.b64decode(user_info["key"])
                        chacha = ChaCha20Poly1305(key)
                        decrypted_meditions = chacha.decrypt(nonce, meditions_encr_bytes, meditions_encr_bytes)
                        meditions_64 = base64.b64encode(decrypted_meditions).decode("utf-8")

                        # serializado a dict
                        meditions_bytes = base64.b64decode(meditions_64)                     # pasarlo de base64 -> bytes
                        meditions_dict = pickle.loads(meditions_bytes)                       # pasarlo de bytes -> dict
                        print(meditions_dict)
                        user_info["meditions"] = meditions_dict
                        
                    return user_info
                except:
                    print("-Contraseña incorrecta")
                    return -1
                         
        print("-El usuario no está registrado")
        return -2
    
    """
    @classmethod
    def new_medition(cls, user_new_data):
        new_medition = str(input("-Introduzca el nivel de azucar: "))
        new_day = str(input("-Introduzca el dia en formato DD/MM/YYYY: "))

        user_new_data["meditions"][new_day] = new_medition
        
        file_manager = FileManager()

        database = file_manager.load("database.json")

        for user in database:
            if user["userid"] == user_new_data["userid"]:
                user["meditions"] = user_new_data["meditions"]
                break

        file_manager.save(database, "database.json")
        print("-Medición guardada")
        return
    """
    
    @classmethod
    def new_medition_app(cls, user_new_data,new_day,new_medition) -> None:
        

        # TODO: Validar que el dia sea correcto, que no se repita y que el nivel de azucar sea correcto

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
        # encrypt dictionary again
        meditions_old = user_info["meditions"]
        nonce = base64.b64decode(user_info["nonce"])
        key = base64.b64decode(user_info["key"])
        # serializar
        meditions_bytes = pickle.dumps(meditions_old)                                     # pasarlo de dict -> bytes                 # pasarlo de bytes -> base64
        # chacha encrypt
        chacha = ChaCha20Poly1305(key)
        encrypted_bytes = chacha.encrypt(nonce, meditions_bytes, meditions_bytes)
        # chacha to 64
        meditions_encrypted = base64.b64encode(encrypted_bytes).decode("utf-8")
        user_info["meditions"] = meditions_encrypted

        file_manager = FileManager()
        database = file_manager.load("database.json")

        for user in database:
            if user["userid"] == user_info["userid"]:
                user["meditions"] = user_info["meditions"]
                break
        
        file_manager.save(database, "database.json")
        print("-Sesión cerrada")
        return



