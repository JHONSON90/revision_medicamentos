import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import math



load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

print("Conectado a supabase")

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "Arreglados", "CONSUMO PACIENTES DEL MES DE JUNIO DE 2025.xlsx")

try:
    data = pd.read_excel(file_path)
    print("la importacion se realizo satisfactoriamente")
except Exception as e:
    print(e)
    print("NO SE REALIZO LA IMPORTACION ADECUADAMENTE")


#eliminar dos primeras columnas
data = data.iloc[:, 2:]
#reemplazar valores nulos por 0
data["IdPaciente"] = data["IdPaciente"].fillna(0).astype(int)
data["NomPaciente"] = data["NomPaciente"].fillna("0")
data["Ref"] = data["Ref"].fillna(0)

data["dValor"] = data["dValor"].astype(int)
data["dCantidad"] = data["dCantidad"].astype(int)


#extraer dos ultimos digitos de columna mes

#data["fecha"] = pd.to_datetime(data["fecha"], format='%Y%m')
data["NUMERO MES"] = 6 #data["fecha"].dt.month
data["AÑO"] = 2025 #data["fecha"].dt.year

data["fecha"] = data["fecha"].astype(int)

data["AÑO"] = data["AÑO"].astype(int)
print(data.info())



data_to_insert = data.to_dict(orient="records")

BATCH_SIZE = 1000
N_BATCHES = math.ceil(len(data) / BATCH_SIZE)

for i in range(N_BATCHES):
    start_idx = i * BATCH_SIZE
    end_idx = min((i + 1) * BATCH_SIZE, len(data))
    batch_df = data.iloc[start_idx:end_idx]

    try:
        records_to_insert = batch_df.to_dict(orient="records")
        response = supabase.table("consumos").insert(records_to_insert).execute()
        if response.data:
            print(f"Batch {i+1}/{N_BATCHES} insertado exitosamente ({len(records_to_insert)} filas).")
        else:
            print(f"Error en el lote {i+1}/{N_BATCHES}: {response.error}")
    except Exception as e:
        print(f"Error inesperado al insertar el lote {i+1}/{N_BATCHES}: {e}")
        # Puedes añadir aquí una lógica para reintentar o registrar el error
        break # Detener si un lote falla o continuar al siguiente

print("\nProceso de inserción por lotes finalizado.")

# try:
#     response = supabase.table("consumos").insert(data_to_insert).execute()
#     print("la insercion se realizo satisfactoriamente")
# except Exception as e:
#     print(e)
#     print("NO SE REALIZO LA INSERCION ADECUADAMENTE")


