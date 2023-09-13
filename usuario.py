import json
import pickle
import base64
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
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

        #Si no está registrado, lo registramos # TODO: meditions como string
        database.append({"userid":user,"pwd_token":token_64,"meditions":"", "salt":salt_64})
        
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
                        user_info["meditions"] = pickle.loads((user_info["meditions"]))
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
        user_info["meditions"] = pickle.dumps(user_info["meditions"])

        file_manager = FileManager()
        database = file_manager.load("database.json")

        for user in database:
            if user["userid"] == user_info["userid"]:
                user["meditions"] = user_info["meditions"]
                break
        
        file_manager.save(database, "database.json")
        print("-Sesión cerrada")
        return



