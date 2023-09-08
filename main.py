from usuario import Usuario
import tkinter as tk

end1 = False

while not end1:
    #Tipo de operación
    operacion = int(input("-Introduzca la operación a llevar a cabo (0 es salir, 1 es registrarse y 2 es iniciar sesión): "))
    
    if operacion ==0:
        end1 = True

    elif operacion == 1:
        #llamar a función que pida al usuario su nombre y contraseña, esta chequeará que ni el nombre ni la contraseña están en el json 
        #si no están se añaden al json de autenticación, si están avisará al usuario y volverá a elegir una operación
        Usuario.register()
    
    elif operacion == 2:
        #llamar a la función que pida al usuario su nombre, contraseña, si no coinciden con las del json, se devolverá al usuario a la 
        #selección de operación
        # En caso de que sí coincida, se le abrirá al usuario un nuevo menú que le permita salir de la aplicación, o elegir una de las
        # siguientes funciones: registrar medida (meterá su usuario, dato de medida y día) o consultar medida (meterá el usuario y se mostrarán
        # todas sus mediciones)
        end2 = False
        user_info = Usuario.login()

        # login da error si no se encuentra el usuario en el json o la contraseña no coincide
        if not user_info:
            continue
        
        while not end2:
            operacion2 = int(input("-Introduzca la operación a llevar a cabo (0 es cerrar la aplicación, 1 es hacer logout, 2 es introducir medida y 3 es consultar medidas): "))
            if operacion2 == 0:
                end1 = True
                end2 = True
            elif operacion2 == 1: 
                end2 = True
            elif operacion2 == 2:
                Usuario.new_medition(user_info)
            elif operacion2 == 3:
                print(user_info["meditions"])


