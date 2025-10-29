import pandas as pd
from importacion import data
import numpy as np


df = pd.DataFrame(data)

#quitar saltos de linea 
df["EspeNom"] = df["EspeNom"].astype(str).str.replace(r'[\n\r]', '', regex=True)
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

#vamos a cambiar en todas las celdas que sean de SIMA municipios a medicina general o medicina especializada

# region Municipios
municipios = (df['origenMed'] == "SIMA") & (df['scc_Nombre'] == "MUNICIPIOS") & (df['EspeNom'] == "MEDICINA GENERAL")

df.loc[municipios, 'scc_Nombre'] = "MEDICINA GENERAL"

municipios = (df['origenMed'] == "SIMA") & (df['scc_Nombre'] == "MUNICIPIOS") & (~df['EspeNom'].isin(["MEDICINA GENERAL"]))
df.loc[municipios, 'scc_Nombre'] = "MEDICINA ESPECIALIZADA"

# oftalmologia = (df['origenMed'] == "SIMA") & (df['scc_Nombre'] == "MUNICIPIOS") & (df['EspeNom'] == "OFTALMOLOGIA")

# df.loc[oftalmologia, 'scc_Nombre'] = "MEDICINA ESPECIALIZADA"

#region Atencion domiciliaria
atencion_domiciliaria = (df['origenMed'] == "SIMA") & (df['scc_Nombre'] == "ATENCION DOMICILIARIA")
df.loc[atencion_domiciliaria, 'scc_Nombre'] = "HOSPITALIZACION"

# region Quimioterapia

#pasando enfermeria a terapias oncologicas
terapias_oncologicas_enfermeras = (df['origenMed'] == "SIMA") & (df['MedicoNom'].isin(["GIOVANNA ELIZABETH ACUÑA LOPEZ", "QUIMIOTERAPIA 1 .", "QUIMIOTERAPIA"]))

df.loc[terapias_oncologicas_enfermeras, 'scc_Nombre'] = "APOYO TERAPEUTICO"
df.loc[terapias_oncologicas_enfermeras, 'EspeNom'] = "TERAPIAS ONCOLOGICAS"

# Especializada oncologia
terapia_onco_especialidad = (df['origenMed'] == "SIMA") & (df['EspeNom'] == "ONCOLOGIA")

df.loc[terapia_onco_especialidad, 'scc_Nombre'] = "APOYO TERAPEUTICO"
df.loc[terapia_onco_especialidad, 'EspeNom'] = "TERAPIAS ONCOLOGICAS"

#region Imagenologia
radiologia = (df['origenMed'] == "SIMA") & (df['EspeNom'] == "RADIOLOGIA")
df.loc[radiologia, 'scc_Nombre'] = "APOYO DIAGNOSTICO"

#region Enfermeria
valores_enfermeria = ["MEDICINA ESPECIALIZADA", "MEDICINA GENERAL", "ODONTOLOGIA"]
enfermeria = (df['origenMed'] == "SIMA") & (df['EspeNom'] == "ENFERMERIA") & (df['scc_Nombre'].isin(valores_enfermeria))
df.loc[enfermeria, 'scc_Nombre'] = "PROMOCION Y PREVENCION"

#region Medicina General
med_general = (df['origenMed'] == "SIMA") & (df['EspeNom'] == "MEDICINA GENERAL") & (df['scc_Nombre'].isin(["MEDICINA ESPECIALIZADA", "ODONTOLOGIA"]))
df.loc[med_general, 'scc_Nombre'] = "MEDICINA GENERAL"

# region apoyo terapeutico
apoyo_tera = (df['origenMed'] == "SIMA") & (df['EspeNom'].isin(["NUTRICION", "OPTOMETRIA", "TERAPIA FISICA", "TERAPIA RESPIRATORIA", "TERAPIA OCUPACIONAL"])) & (df['scc_Nombre'].isin(["MEDICINA ESPECIALIZADA","MEDICINA GENERAL", "ODONTOLOGIA", "PROMOCION Y PREVENCION"]))
df.loc[apoyo_tera, 'scc_Nombre'] = "APOYO TERAPEUTICO"


#region odontologia

odontologia = (df['origenMed'] == "SIMA") & (df['EspeNom'] == "ODONTOLOGIA")
df.loc[odontologia, 'scc_Nombre'] = "ODONTOLOGIA"

higiene_oral = (df['origenMed'] == "SIMA") & (df['EspeNom'] == "HIGIENISTA ORAL") 
df.loc[higiene_oral, 'scc_Nombre'] = "ODONTOLOGIA"

#region promocion y prevencion
promocion = (df['origenMed'] == "SIMA") & (df['scc_Nombre'] == "PROMOCION Y PREVENCION") & (~df['EspeNom'].isin(["ENFERMERIA", "Hospitales", "MEDICINA ESPECIALIZADA", "MEDICINA GENERAL", "MEDICINA INTERNA", "GINECOLOGIA"]))
df.loc[promocion, 'scc_Nombre'] = "MEDICINA ESPECIALIZADA"

promocion = (df['origenMed'] == "SIMA") & (df['scc_Nombre'] == "PROMOCION Y PREVENCION") & (df['EspeNom'] == "TERAPIA FISICA")
df.loc[promocion, 'scc_Nombre'] = "APOYO TERAPEUTICO"


#region Especializada
especializada = (df['origenMed'] == "SIMA") & (~df['EspeNom'].isin(["MEDICINA GENERAL", "ODONTOLOGIA"])) & (~df['EspeNom'].isin([ "Hospitales"])) & (df['scc_Nombre'].isin(["MEDICINA GENERAL", "ODONTOLOGIA"]))
df.loc[especializada, 'scc_Nombre'] = "MEDICINA ESPECIALIZADA"

gastroenterologia = (df['origenMed'] == "SIMA") & (df['EspeNom'].isin(["GASTROENTEROLOGIA", "GASTROENTEROLOGIA INTERVENCIONISTA"])) & (df['scc_Nombre'] == "MEDICINA ESPECIALIZADA")
df.loc[gastroenterologia, 'EspeNom'] = "GASTROENTEROLOGIA"

especializada_sin_especificar = (df['origenMed'] == "SIMA") & (df['EspeNom'].isin(["Hospitales", "MEDICINA ESPECIALIZADA", "nan", "BACTERIOLOGIA"])) & (df['scc_Nombre'] == "MEDICINA ESPECIALIZADA")
df.loc[especializada_sin_especificar, 'EspeNom'] = "ESPECIALIZADA SIN ESPECIFICAR"

urgenciologia = (df['origenMed'] == "SIMA") & (df['EspeNom'].isin(["MEDICINA URGENCIOLOGIA INTENSIVISTA ", "MEDICINA URGENCIOLOGIA INTENSIVISTA ", "MEDICINA URGENCIOLOGIA INTENSIVISTA", "MEDICINA URGENCIOLOGIA INTENSIVISTA "])) & (df['scc_Nombre'] == "MEDICINA ESPECIALIZADA")
df.loc[urgenciologia, 'scc_Nombre'] = "UCI ADULTOS"

cirugia  = (df['origenMed'] == "SIMA") & (df['EspeNom'].isin(["CIRUGIA", "CIRUGIA GENERAL"]) & (df['scc_Nombre'] == "MEDICINA ESPECIALIZADA"))
df.loc[cirugia, 'EspeNom'] = "CIRUGIA GENERAL"
df.loc[cirugia, 'scc_Nombre'] = "MEDICINA ESPECIALIZADA"

mes = input("Mes a arreglar? ")
try:
      df.to_excel(f"Arreglados/CONSUMO PACIENTES DEL MES DE {mes.upper()} DE 2025.xlsx")
      print("El archivo se exporto satisfactoriamente")
except:
      print("No se pudo exportar el archivo")