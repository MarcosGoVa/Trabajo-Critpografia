import json
class FileManager:
    #Cargamos la base de datos en database, si hay un error se trata mandando una excepción
    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name,"r", encoding="utf-8", newline="") as file:
                database = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("No se ha encontrado el archivo database.json")
        except json.decoder.JSONDecodeError:
            database = []
        
        file.close() #TODO ¿Es necesario?

        return database
    
    @classmethod
    def save(cls, content, file_name):
        try:
            with open(file_name,"w", encoding="utf-8", newline="") as file:
                json.dump(content, file, indent=2)
        except FileNotFoundError:
            raise FileNotFoundError("No se ha encontrado el archivo database.json")
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError("El archivo database.json está corrupto")
