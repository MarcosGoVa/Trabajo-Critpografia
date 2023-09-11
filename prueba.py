from datetime import datetime

fecha_actual = datetime.now()
print(fecha_actual)

meditions = {
      "12/08/2004": 333,
      "09/03/2025": 140,
      "13/09/2023": 121,
      "12/09/2023": 150,
      "25/09/2023": 123,
      "29/09/2023": 555,
      "09/09/2021": 600,
      "28/08/2023": 43,
      "07/09/2023": 98 
}



for fecha, valor in meditions.items():
    dias_diferencia = (fecha_actual - datetime.strptime(fecha, "%d/%m/%Y")).days
    if dias_diferencia <= 365 and dias_diferencia >= 0:
        ultimo_ano[fecha] = valor
