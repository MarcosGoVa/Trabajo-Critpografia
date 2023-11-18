import tkinter as tk
import pickle
import os
import matplotlib.pyplot as plt
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from usuario import Usuario  
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from sistema import Sistema
from tkinter import filedialog


class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Aplicación de Registro y Login")
        self.ventana.state("zoomed")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.frame_login = tk.Frame(ventana)
        self.frame_login.pack()

        self.label_usuario = tk.Label(self.frame_login, text="Usuario:")
        self.label_password = tk.Label(self.frame_login, text="Contraseña:")

        self.entry_usuario = tk.Entry(self.frame_login)
        self.entry_password = tk.Entry(self.frame_login, show="*")  # Muestra asteriscos para ocultar la contraseña

        self.btn_login = tk.Button(self.frame_login, text="Iniciar Sesión", command=self.login)
        self.btn_registro = tk.Button(self.frame_login, text="Registrarse", command=self.registro)


        self.btn_check_signature = tk.Button(self.frame_login, text="Comprobar informe", command=lambda: self.comprobar_informe_acceso())

        self.label_usuario.pack()
        self.entry_usuario.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_login.pack()
        self.btn_registro.pack()
        self.btn_check_signature.pack()

    def comprobar_informe_acceso(self):
        self.frame_login.pack_forget()
        
        self.frame_comprobar_informe = tk.Frame(self.ventana)
        self.frame_comprobar_informe.pack()
        # Crear un botón para seleccionar el archivo
        self.file_firma = None
        self.file_mensaje = None
        
        self.btn_subir_firma = tk.Button(self.frame_comprobar_informe, text="Subir firma", command=lambda: self.load_file(1))
        self.btn_subir_firma.pack(pady=20)

        self.btn_subir_mensaje = tk.Button(self.frame_comprobar_informe, text="Subir mensaje", command=lambda: self.load_file(2))
        self.btn_subir_mensaje.pack(pady=20)

        btn_verificar_informe = tk.Button(self.frame_comprobar_informe, text="Verificar Informe", command=lambda: self.verificar_informe())
        btn_verificar_informe.pack(pady=20)

        btn_volver_a_inicio = tk.Button(self.frame_comprobar_informe, text="Volver ", command=lambda: self.volver_a_inicio(self.frame_comprobar_informe))
        btn_volver_a_inicio.pack(pady=15)

        #Usuario.comprobar_informe_usuario()

    
    def verificar_informe(self):
        if (self.file_firma and self.file_mensaje):
            if Usuario.comprobar_informe_usuario(self.file_firma,self.file_mensaje) == True:
                tk.messagebox.showinfo("Éxito", "Informe verificado correctamente")
            else:
                tk.messagebox.showerror("Error", "El informe no es válido")
        else:
            tk.messagebox.showerror("Error", "Falta por subir algún archivo")

    def load_file(self, tipo_documento):
        file_path = filedialog.askopenfilename()
        if file_path:
            if tipo_documento == 1:
                with open(file_path, 'rb') as file:
                    self.file_firma = file.read()
                print(f"Firma cargado: {file_path}")
                self.btn_subir_firma.configure(bg="green")
            elif tipo_documento == 2:
                with open(file_path, 'rb') as file:
                    self.file_mensaje = file.read()
                print(f"Mensaje cargado: {file_path}")
                self.btn_subir_mensaje.configure(bg="green")



    def volver_a_inicio(self, current_place):
        for widget in current_place.winfo_children():
            widget.destroy()
        current_place.destroy()
        self.frame_login.pack()


    def login(self):
        user = self.entry_usuario.get()
        password = self.entry_password.get()

        # Llama a tu función de inicio de sesión desde la clase Usuario
        self.user_info = Usuario.login_app(user, password)
        
        if self.user_info == -1:
            tk.messagebox.showerror("Log in", "Contraseña o usuario incorrectos.")
            self.entry_usuario.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        elif self.user_info == -2:
            tk.messagebox.showerror("Log in", "Contraseña o usuario incorrectos.")
            self.entry_usuario.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            self.frame_login.pack_forget()  # Oculta el formulario de inicio de sesión
            self.show_menu()

    def registro(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_password.get()

        # Llama a tu función de registro desde la clase Usuario
        registro_feedback = Usuario.register_app(usuario, contrasena)

        if registro_feedback == -1:
            tk.messagebox.showerror("Registro", """La contraseña no es válida. Requerimientos de contraseña: 
                                    \n- Longitud: 8-32 caracteres.
                                    \n- Al menos 1 mayúscula.
                                    \n- Al menos 1 minúscula.
                                    \n- Al menos 1 carácter especial: ~!@#$%^*()_-+={}[]|:;?
                                    \n- Al menos 1 número. """)
        elif registro_feedback == -2:
            tk.messagebox.showerror("Registro", """El nombre de usuario no es válido. Requerimientos de nombre de usuario: 
                                    \n- Longitud: 4-32 caracteres. 
                                    \n- Solo letras (mayúsculas o minúsculas), números y guiones bajos.""")
        elif registro_feedback == -3:
            tk.messagebox.showerror("Registro", "El usuario ya existe.")
        else:
            tk.messagebox.showinfo("Registro", "Usuario registrado correctamente.")
        
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def show_menu(self):
        # Crear un marco para el menu 
        self.frame_menu = tk.Frame(self.ventana)
        self.frame_menu.pack()

        # Crear una etiqueta de Tkinter para mostrar el mensaje de bienvenida
        label_bienvenida = tk.Label(self.frame_menu, text="Bienvenido " + self.user_info["userid"] + "!", font=("Arial Bold", 20))
        label_bienvenida.pack()

        # Botones
        btn_cerrar_sesion = tk.Button(self.frame_menu, text="Cerrar Sesión", command=lambda: self.logout_from(self.frame_menu))
        btn_introducir_data = tk.Button(self.frame_menu, text="Introducir nueva medicion", command=self.introducir_data)
        btn_consulta = tk.Button(self.frame_menu, text="Consultar mediciones", command=self.consultar)

        btn_pedir_informe = tk.Button(self.frame_menu, text="Pedir_informe", command=lambda: self.pedir_informe(self.user_info))
        
        # Mostrar en el frame en pantalla
        btn_introducir_data.pack()
        btn_consulta.pack()
        btn_cerrar_sesion.pack()
        btn_pedir_informe.pack()

    def pedir_informe(self,user_info):
        Usuario.solicitar_informe_usuario(user_info)

    def cerrar_sesion(self):
        # Eliminar todo el menu
        for widget in self.frame_menu.winfo_children():
            widget.destroy()
        self.frame_menu.destroy()
        
        


    def introducir_data(self):
        self.frame_menu.pack_forget()
        
        self.frame_registrar = tk.Frame(self.ventana)
        self.frame_registrar.pack()

        self.cal = None

        self.label_new_day = tk.Label(self.frame_registrar, text="Día:")
        self.label_new_medition = tk.Label(self.frame_registrar, text="Nivel de azúcar:")

        self.entry_new_day = tk.Entry(self.frame_registrar)
        # Mostrar el calendario al hacer click en el campo de entrada
        self.entry_new_day.bind("<FocusIn>", self.mostrar_calendario)
        self.entry_new_medition = tk.Entry(self.frame_registrar)

        self.btn_new_registration = tk.Button(self.frame_registrar, text="Introducir", command=self.exit_registrar_data)

        self.label_new_day.pack()
        self.entry_new_day.pack()
        self.label_new_medition.pack()
        self.entry_new_medition.pack()
        self.btn_new_registration.pack()

    def mostrar_calendario(self, event):
        if self.cal:
            return

        fecha_actual = datetime.now().date()

        self.cal = Calendar(self.frame_registrar, selectmode="day", date_pattern="dd/mm/yyyy",
         year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
        self.cal.pack()

        # Configurar la acción al seleccionar una fecha en el calendario
        self.cal.bind("<<CalendarSelected>>", self.actualizar_entry_day)
    
    def actualizar_entry_day(self, event):
        fecha_seleccionada = self.cal.get_date()
        self.entry_new_day.delete(0, tk.END)
        self.entry_new_day.insert(0, fecha_seleccionada)

        
    def exit_registrar_data(self):
        new_day = self.entry_new_day.get()
        new_medition = self.entry_new_medition.get()
        if len(new_day) != 0 and len(new_medition) != 0:
            error = Usuario.new_medition_app(self.user_info,new_day,new_medition)
            if error == -1:
                tk.messagebox.showerror("Registro", "La fecha no es válida.\n Formato: DD/MM/YYYY")
            elif error == -2:
                tk.messagebox.showerror("Registro", "La medición no es válida.\n Debe ser un número entre 0 y 1000")
            else:
                tk.messagebox.showinfo("Registro", "Medición guardada correctamente.")
                self.menu_from(self.frame_registrar)
        else:
            tk.messagebox.showerror("Registro", "Por favor, rellene todos los campos.")
    

    def consultar(self):
        self.frame_menu.pack_forget()

        self.frame_consulta = tk.Frame(self.ventana)
        self.frame_consulta.pack()

        # TABLA
        fechas_ordenadas = sorted(self.user_info["meditions"].keys(), key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
        self.tabla = ttk.Treeview(self.frame_consulta, columns=("Fecha", "Valor"), padding=[-395,0,0,0])
        # Configurar las columnas
        self.tabla.heading("#1", text="Fecha", anchor=tk.CENTER)
        self.tabla.heading("#2", text="Valor", anchor=tk.CENTER)
        # Ajustar el ancho de las columnas
        self.tabla.column("#1", width=100, anchor=tk.CENTER)
        self.tabla.column("#2", width=50, anchor=tk.CENTER)
        # Llenar la tabla con los datos
        self.llenar_tabla(self.tabla, fechas_ordenadas)

        # BOTONES
        btn_cerrar_sesion = tk.Button(self.frame_consulta, text="Cerrar Sesión", command=lambda: self.logout_from(self.frame_consulta))
        btn_go_home = tk.Button(self.frame_consulta, text="Volver al menú", command=lambda: self.menu_from(self.frame_consulta))
        btn_mostrar_grafico = tk.Button(self.frame_consulta, text="Mostrar Gráfico", command=lambda: self.mostrar_grafico())

        self.tabla.pack()
        btn_mostrar_grafico.pack()
        btn_go_home.pack()
        btn_cerrar_sesion.pack()
        

    def mostrar_grafico(self):
        for widget in self.frame_consulta.winfo_children():
            widget.destroy()
        self.frame_consulta.destroy()

        fechas_ordenadas, medidas_ordenadas = self.sort_meditions()

        self.create_graph(fechas_ordenadas, medidas_ordenadas)

        # BOTONES
        self.graph_buttons(fechas_ordenadas, medidas_ordenadas)

    def graph_buttons(self, fechas_ordenadas, medidas_ordenadas):
        btn_cerrar_sesion = tk.Button(self.frame_graph, text="Cerrar Sesión", command=lambda: self.logout_from(self.frame_graph))
        btn_go_home = tk.Button(self.frame_graph, text="Volver al menú", command=lambda: self.menu_from(self.frame_graph))
        btn_last_year = tk.Button(self.frame_graph, text="Último año", command=lambda: self.graph_last_year(fechas_ordenadas,medidas_ordenadas))
        btn_last_6_months = tk.Button(self.frame_graph, text="Últimos 6 meses", command=lambda: self.graph_last_6_months(fechas_ordenadas,medidas_ordenadas))
        btn_last_month = tk.Button(self.frame_graph, text="Último mes", command=lambda: self.graph_last_month(fechas_ordenadas,medidas_ordenadas))
        btn_last_week = tk.Button(self.frame_graph, text="Última semana", command=lambda: self.graph_last_week(fechas_ordenadas,medidas_ordenadas))


        btn_last_year.pack()
        btn_last_6_months.pack()
        btn_last_month.pack()
        btn_last_week.pack()
        btn_cerrar_sesion.pack()
        btn_go_home.pack()

    def sort_meditions(self):
        medition_days = self.user_info["meditions"].keys()

        fechas_ordenadas = sorted(medition_days, key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
        medidas_ordenadas = []
        for fecha in fechas_ordenadas:
            medidas_ordenadas.append(self.user_info["meditions"][fecha])
        self.frame_graph = tk.Frame(self.ventana)
        self.frame_graph.pack()
        return fechas_ordenadas,medidas_ordenadas

    def logout_from(self, current_place):
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        for widget in current_place.winfo_children():
            widget.destroy()
        
        if self.user_info:
            Usuario.log_out_app(self.user_info)
            self.user_info = None

        current_place.destroy()

        self.frame_login.pack()

    def menu_from(self, current_place):
        for widget in current_place.winfo_children():
            widget.destroy()
        current_place.destroy()
        self.show_menu()


    def llenar_tabla(self, table, fechas_ordenadas):
        for fecha in fechas_ordenadas:
            valor = self.user_info["meditions"][fecha]
            table.insert("", "end", values = (fecha, valor))

    def graph_last_year(self,days,values):
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
        fecha_actual = datetime.now()
        last_year = {}
        for i in range(len(days)):
            dias_diferencia = (fecha_actual - datetime.strptime(days[i], "%d/%m/%Y")).days
            if dias_diferencia <= 365 and dias_diferencia > 0:
                last_year[days[i]] = values[i]

        self.create_graph(last_year.keys(), last_year.values())
        self.graph_buttons(days, values)
        

    def graph_last_6_months(self,days,values):
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
        fecha_actual = datetime.now()
        last_year = {}
        for i in range(len(days)):
            dias_diferencia = (fecha_actual - datetime.strptime(days[i], "%d/%m/%Y")).days
            if dias_diferencia <= 6*31 and dias_diferencia > 0:
                last_year[days[i]] = values[i]

        self.create_graph(last_year.keys(), last_year.values())
        self.graph_buttons(days, values)
        
  
    def graph_last_month(self,days,values):
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
        fecha_actual = datetime.now()
        last_year = {}
        for i in range(len(days)):
            dias_diferencia = (fecha_actual - datetime.strptime(days[i], "%d/%m/%Y")).days
            if dias_diferencia <= 31 and dias_diferencia > 0:
                last_year[days[i]] = values[i]

        self.create_graph(last_year.keys(), last_year.values())
        self.graph_buttons(days, values)
        
  

    def graph_last_week(self,days,values):
        for widget in self.frame_graph.winfo_children():
            widget.destroy()
        fecha_actual = datetime.now()
        last_year = {}
        for i in range(len(days)):
            dias_diferencia = (fecha_actual - datetime.strptime(days[i], "%d/%m/%Y")).days
            if dias_diferencia <= 7 and dias_diferencia > 0:
                last_year[days[i]] = values[i]

        self.create_graph(last_year.keys(), last_year.values())
        self.graph_buttons(days, values)
        
  

    def create_graph(self,days, values):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(days, values, marker='o', linestyle='-', color='r')
        ax.set_title('Azúcar en sangre gr/ml.')
        ax.set_xlabel('Fechas')
        ax.set_ylabel('gr/ml')

        # Rotar las etiquetas del eje x para una mejor visualización
        plt.xticks(rotation=30)

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_graph)
        self.canvas.get_tk_widget().pack()

    def cerrar_ventana(self):
        self.logout_from(self.ventana)
        exit()




            
if __name__ == "__main__":
    #ventana
    ventana = tk.Tk()
    #Creamos el objeto
    app = App(ventana)
    #ejecutas la ventana
    ventana.mainloop()
