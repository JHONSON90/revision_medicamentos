import pandas as pd

try:
      data = pd.read_excel("Informes_sin_procesar/CONSUMO PACIENTES SEPT 2025.xlsx")
      print("la importacion se realizo satisfactoriamente")
except:
      print("NO SE REALIZO LA IMPORTACION ADECUADAMENTE")