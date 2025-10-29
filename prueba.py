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


#traer datos de la tabla de consumos
try:
    data = supabase.table("consumos").select("*").execute()
    df = pd.DataFrame(data.data)
    print("la consulta se realizo satisfactoriamente")
except Exception as e:
    print(e)
    print("NO SE REALIZO LA CONSULTA ADECUADAMENTE")

print(df.head(5))
