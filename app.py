import tkinter as tk
from tkinter import messagebox, ttk
from usuario import Usuario  
from datetime import datetime

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Aplicación de Registro y Login")

        self.frame_login = tk.Frame(ventana)
        self.frame_login.pack()

        self.label_usuario = tk.Label(self.frame_login, text="Usuario:")
        self.label_password = tk.Label(self.frame_login, text="Contraseña:")

        self.entry_usuario = tk.Entry(self.frame_login)
        self.entry_password = tk.Entry(self.frame_login, show="*")  # Muestra asteriscos para ocultar la contraseña

        self.btn_login = tk.Button(self.frame_login, text="Iniciar Sesión", command=self.login)
        self.btn_registro = tk.Button(self.frame_login, text="Registrarse", command=self.registro)

        self.label_usuario.pack()
        self.entry_usuario.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_login.pack()
        self.btn_registro.pack()


    def login(self):
        user = self.entry_usuario.get()
        password = self.entry_password.get()

        # Llama a tu función de inicio de sesión desde la clase Usuario
        user_info = Usuario.login_app(user, password)
        
        if user_info == -1:
            tk.messagebox.showerror("Log in", "Contraseña incorrecta.")
            self.entry_usuario.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        elif user_info == -2:
            tk.messagebox.showerror("Log in", "El usuario no existe.")
            self.entry_usuario.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            self.frame_login.pack_forget()  # Oculta el formulario de inicio de sesión
            self.show_menu(user_info)

    def registro(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_password.get()

        # Llama a tu función de registro desde la clase Usuario
        exito = Usuario.register_app(usuario, contrasena)

        if exito:
            tk.messagebox.showinfo("Registro", "Registro exitoso.")
        else:
            tk.messagebox.showerror("Registro", "El usuario ya existe.")
        
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def show_menu(self, user_info):
        # Aquí puedes crear y mostrar un nuevo formulario para el menú de la aplicación
        # Puedes usar self.ventana o crear un nuevo marco (frame) para mostrar las opciones del menú
        # Debes conectar esta parte con tu lógica de la aplicación para registrar medidas y consultar medidas

        self.user_info = user_info

        # Crear un marco para el menu 
        self.frame_menu = tk.Frame(self.ventana)
        self.frame_menu.pack()

        # Crear una etiqueta de Tkinter para mostrar el mensaje de bienvenida
        label_bienvenida = tk.Label(self.frame_menu, text="Bienvenido " + self.user_info["userid"] + "!", font=("Arial Bold", 20))
        label_bienvenida.pack()

        # Botones
        btn_cerrar_sesion = tk.Button(self.frame_menu, text="Cerrar Sesión", command=self.cerrar_sesion)
        btn_introducir_data = tk.Button(self.frame_menu, text="Introducir nueva medicion", command=self.registrar_data)
        btn_consulta = tk.Button(self.frame_menu, text="Consultar mediciones", command=self.consultar)
        
        # Mostrar en el frame en pantalla
        btn_introducir_data.pack()
        btn_consulta.pack()
        btn_cerrar_sesion.pack()

    def cerrar_sesion(self):
        # Eliminar todo el menu
        for widget in self.frame_menu.winfo_children():
            widget.destroy()
        self.frame_menu.destroy()
        self.user_info = None

        self.frame_login.pack()
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def registrar_data(self):
        self.frame_menu.pack_forget()
        # TODO crear un formulario para registrar una nueva medida
        
        

    def consultar(self):
        self.frame_menu.pack_forget()

        self.frame_consulta = tk.Frame(self.ventana)
        self.frame_consulta.pack()

        fechas_ordenadas = sorted(self.user_info["meditions"].keys(), key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
        
        tabla = ttk.Treeview(self.frame_consulta, columns=("Fecha", "Valor"), padding=[-395,0,0,0])
        # Configurar las columnas
        tabla.heading("#1", text="Fecha", anchor=tk.CENTER)
        tabla.heading("#2", text="Valor", anchor=tk.CENTER)

        # Ajustar el ancho de las columnas
        tabla.column("#1", width=100, anchor=tk.CENTER)
        tabla.column("#2", width=50, anchor=tk.CENTER)

        self.llenar_tabla(tabla, fechas_ordenadas)
        btn_cerrar_sesion = tk.Button(self.frame_consulta, text="Cerrar Sesión", command=lambda: self.logout_from(self.frame_consulta))
        btn_go_home = tk.Button(self.frame_consulta, text="Volver al menú", command=lambda: self.menu_from(self.frame_consulta))
        

        tabla.pack()
        btn_cerrar_sesion.pack()
        btn_go_home.pack()


    def logout_from(self, current_place):
        for widget in current_place.winfo_children():
            widget.destroy()
        current_place.destroy()
        self.cerrar_sesion()

    def menu_from(self, current_place):
        for widget in current_place.winfo_children():
            widget.destroy()
        current_place.destroy()
        self.show_menu(self.user_info)


    def llenar_tabla(self, table, fechas_ordenadas):
        for fecha in fechas_ordenadas:
            valor = self.user_info["meditions"][fecha]
            table.insert("", "end", values = (fecha, valor))

  


if __name__ == "__main__":
    #ventana
    ventana = tk.Tk()
    #Creamos el objeto
    app = App(ventana)
    #ejecutas la ventana
    ventana.mainloop()
