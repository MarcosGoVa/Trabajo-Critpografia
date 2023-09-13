import json
from file_manager import FileManager
from data.password import Password
from data.username import Username
from data.sugar import Sugar
from data.date import Date



class Usuario:
    def __init__(self,nombre,contraseña):
        self.nombre = nombre
        self.contraseña =  contraseña

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
        
        #Buscamos si el usuario ya está registrado
        for i in database:
            if i["userid"] == user:
                print("-El usuario ya está registrado")
                return -3
        

        #Si no está registrado, lo registramos
        database.append({"userid":user,"password":password,"meditions":{}})
        
        # Guardamos los cambios
        file_manager.save(database,"database.json")
        
        return 0


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
    
    @classmethod
    def login_app(cls, user, password):
        file_manager = FileManager()
        
        database = file_manager.load("database.json")

        #Buscamos si el usuario ya está registrado
        for user_info in database:
            if user_info["userid"] == user:
                if user_info["password"] == password:
                    print("-Bienvenido al sistema ", user_info["userid"])
                    return user_info
                print("-Contraseña incorrecta")
                return -1
        
        print("-El usuario no está registrado")
        return -2
    
    
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



