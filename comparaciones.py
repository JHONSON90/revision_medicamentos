import pandas as pd
from importacion import data
import numpy as np
import openpyxl as op

df = pd.DataFrame(data)

print(df.head())
print(df.dtypes)

# region COLUMNAS
"""
Index(['TipMovFiltro', 'FechaDesde', 'FechaHasta', 'Mes', 'fecha', 'TipDoc4',
       'DescTipDoc', 'NroMov', 'SecMov', 'BodegaMov', 'BOD4', 'NombreBod',
       'CentroMov', 'cc_Nombre', 'ScentroMov', 'scc_Nombre', 'MedicoCod',
       'MedicoNom', 'EspeCod', 'EspeNom', 'COD13', 'Ref', 'Producto', 'LinInv',
       'Linea', 'GruInv', 'Grupo', 'CtaInv', 'CtaCruce', 'dCantidad', 'dValor',
       'Veces', 'origenMed', 'IdPaciente', 'NomPaciente'],
      dtype='object')
      
"""

df[["dValor", "dCantidad"]] = df[["dValor", "dCantidad"]].astype("float")

medicamentos1 = pd.pivot_table(df[(df['origenMed'] == "SIMA") & 
                                   (~df['scc_Nombre'].isin(["APOYO DIAGNOSTICO", "MEDICINA ESPECIALIZADA", "APOYO TERAPEUTICO"])) & 
                                   (df["CtaCruce"].isin([6135050100,6135050200,6135150000,6135050300,6135400000,6135300000,6135200000,6135250000])) & 
                                   (df["TipDoc4"] != "S014") & 
                                   (df["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))], 
                             values="dValor", 
                             index="scc_Nombre", 
                             aggfunc="sum")

print(medicamentos1.to_string(float_format='{:.2f}'.format))

medicamentos2 = pd.pivot_table(df[(df['origenMed'] == "SIMA") & 
                                   (df['scc_Nombre'].isin(["APOYO DIAGNOSTICO", "MEDICINA ESPECIALIZADA", "APOYO TERAPEUTICO"])) & 
                                   (df["CtaCruce"].isin([6135050100,6135050200,6135150000,6135050300,6135400000,6135300000,6135200000,6135250000])) & 
                                   (df["TipDoc4"] != "S014") & 
                                   (df["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))], 
                             values="dValor", 
                             index="EspeNom", 
                             aggfunc="sum")

print(medicamentos2.to_string(float_format='{:.2f}'.format))

medicamentos3 = pd.pivot_table(df[(df['origenMed'] == "SIMA") & 
                                   (df["CtaCruce"].isin([6135050100,6135050200,6135150000,6135050300,6135400000,6135300000,6135200000,6135250000])) & 
                                   (df["TipDoc4"] == "S014") & 
                                   (df["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))], 
                             values="dValor", 
                             index="NombreBod", 
                             aggfunc="sum")

print(medicamentos3.to_string(float_format='{:.2f}'.format))