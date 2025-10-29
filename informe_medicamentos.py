import pandas as pd
import numpy as np
from importacion import data

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
# region SIMA
#? seleccionamos todos los ingresos por SIMA
origen = data[data['origenMed'] == "SIMA"]

# Revisa que dentro de origen cuantos tienen el nombre de *MUNICIPIOS* en el subcentro de costos
municipios = origen[origen['scc_Nombre'] == "MUNICIPIOS"]
#print(len(municipios))
res_municipios = f"Se encuentran {len(municipios)} registros con subcentro de costo MUNICIPIOS"
#print(res_municipios)

#region Cirugia
cirugia = origen[origen['scc_Nombre'] == "CIRUGIA"]
res_cirugia = f"Se encuentran {len(cirugia)} registros con subcentro de costo CIRUGIA"
#print(res_cirugia)

# Revisa todos los registros que tenga medico *NO DETERMINADO*
no_determinado = origen[origen['MedicoNom'] == "NO DETERMINADO"]
res_no_determinado = f"Se encuentran {len(no_determinado)} registros con medico NO DETERMINADO"
#print(res_no_determinado)

# region MEDICINA GENERAL
#? Creamos el grupo de *MEDICINA GENERAL*
medicina_general =origen[origen['scc_Nombre'] == "MEDICINA GENERAL"]

#Revisamos cuantos medicos generales hay en medicina general
mgral = medicina_general[medicina_general['EspeNom'] == "MEDICINA GENERAL"]
hospitales = medicina_general[medicina_general['EspeNom'] == "Hospitales"]


# Revisamos cuantas enfermeras hay en el grupo de medicina general
enfermeria= medicina_general[medicina_general['EspeNom'] == "ENFERMERIA"]
res_enfer_in_mgral = f"Se encuentran {len(enfermeria)} registros de ENFERMERIA en el subcentro de costo de MEDICINA GENERAL"
#print(res_enfer_in_mgral)



# Por descarte sacamos cuantas especializadas hay en medicina general
espe_in_mgral = len(medicina_general) - (len(mgral) + len(enfermeria) + len(hospitales))
res_espe_in_mgral = f"Se encuentran {espe_in_mgral} registros de MEDICINA ESPECIALIZADA en el subcentro de costo de MEDICINA GENERAL"
#print(res_espe_in_mgral)

#region PYM
# Revisamos cuantas especialidades que no son de promocion y prevencion estan descargadas en este proceso
pym = origen[origen['scc_Nombre'] == "PROMOCION Y PREVENCION"]

especialidades_pym = pym[pym['EspeNom'].isin(["CIRUGIA ONCOLOGICA", "OFTALMOLOGIA", "UROLOGIA", "ANESTESIOLOGIA", "CIRUGIA GENERAL", "CIRUGIA VASCULAR", "FISIATRIA", "MEDICINA URGENCIOLOGIA INTENSIVISTA ", "ORTOPEDIA", "CARDIOLOGIA", 'ENDOCRINOLOGIA', 'MEDICINA FAMILIAR', 'MEDICINA URGENCIOLOGIA INTENSIVISTA', 'NEUROCIRUGIA', 'NEUROLOGIA', 'ONCOLOGIA', 'PSIQUIATRIA', "MEDICINA ESPECIALIZADA"])]
res_pym = f"Se encuentran {len(especialidades_pym)} registros con subcentro de costo PYM y son especialidades que no corresponden a PYM"
#print(res_pym)


# region MEDICINA ESPECIALIZADA
#? Creamos el grupo de *MEDICINA ESPECIALIZADA*
medicina_especializada = origen[origen['scc_Nombre'] == "MEDICINA ESPECIALIZADA"]

# Revisamos en el grupo de medicina especializada cuantos medicos tenemos
med_gral_in_espe = medicina_especializada[medicina_especializada['EspeNom'] == "MEDICINA GENERAL"]
res_mgral_in_esp = f"Se encuentran {len(med_gral_in_espe)} registros de MEDICINA GENERAL en el subcentro de costo de MEDICINA ESPECIALIZADA"
#print(res_mgral_in_esp)



# Revisamos en el grupo de medicina especializada cuantas enfermeras tenemos
enfer_in_espe = medicina_especializada[medicina_especializada['EspeNom'] == "ENFERMERIA"] # aqui contamos todas las de enfermeria 
enfer_in_espe_sin_quimio = enfer_in_espe[enfer_in_espe['MedicoNom'] != "QUIMIOTERAPIA 1 ." ] # les quitamos las de quimioterapia 
res_enfer_in_esp = f"Se encuentran {len(enfer_in_espe_sin_quimio)} registros de ENFERMERIA en el subcentro de costo de MEDICINA ESPECIALIZADA"
#print(res_enfer_in_esp)


# Revisamos en el grupo de medicina especializada cuantas odontologos tenemos
odonto_in_espe = medicina_especializada[medicina_especializada['EspeNom'] == "ODONTOLOGIA"]
res_odon_in_esp = f"Se encuentran {len(odonto_in_espe)} registros de ODONTOLOGIA en el subcentro de costo de MEDICINA ESPECIALIZADA"
# print(res_odon_in_esp)

#region ATENCION DOMICILIARIA
domiciliaria = origen[origen["scc_Nombre"] == "ATENCION DOMICILIARIA"]
res_domiciliaria = f"Se encuentran {len(domiciliaria)} registros de ATENCION DOMICILIARIA"

# region ODONTOLOGIA
#? Creamos el grupo de *ODONTOLOGIA*
odontologia = origen[origen['scc_Nombre'] == "ODONTOLOGIA"]

# Revisamos en el grupo de odontologia cuantas de oftalmologia tenemos
oftal_in_odonto = odontologia[odontologia['EspeNom'] == "OFTALMOLOGIA"]
res_ofta_in_odon = f"Se encuentran {len(oftal_in_odonto)} registros de OFTALMOLOGIA en el subcentro de costo de ODONTOLOGIA"
# print(res_ofta_in_odon)

# Revisamos en el grupo de odontologia cuantas de medicina general tenemos
medgral_in_odonto = odontologia[odontologia['EspeNom'] == "MEDICINA GENERAL"]
res_mgral_in_odon = f"Se encuentran {len(medgral_in_odonto)} registros de MEDICINA GENERAL en el subcentro de costo de ODONTOLOGIA"
# print(res_mgral_in_odon)


# region MEDICOS
#? Revisamos los codigos que se estan utilizando por medico

luis_fdo_caicedo = origen[origen['MedicoCod'] == 3073]
luis_fdo_caicedo2 = origen[origen['MedicoCod'] == 5]

rsta_luis_fdo_caicedo = f"Se utiliza al Dr Luis Fernando Caicedo con codigos 3073 y 5 en {len(luis_fdo_caicedo)+len(luis_fdo_caicedo2)} registros"


maurimelo_maurodri = origen[origen['MedicoCod'] == 3457]

rta_maurimelo_maurodri = f"Se utiliza al Dr Jorge Muaricio Melo Mauricio Rodriguez con el codigo 3457 en {len(maurimelo_maurodri)} registros"


melo_dolypantoja = origen[origen['MedicoCod'] == 4447]
rta_melo_dolypantoja = f"Se utiliza al DR MAURICIO  MELO  DRA DOLY  PANTOJA con el codigo 4447 en {len(melo_dolypantoja)} registros"
   
      
calpa = origen[origen['MedicoCod'] == 1159]
calpa2 = origen[origen['MedicoCod'] == 3087]
rta_calpa = f"Se utiliza al DR ALVARO JOSE CALPA ZAMBRANO con el codigo 1159 Y 3087 {len(calpa) + len(calpa2)} registros"

      
emilio = origen[origen['MedicoCod'] == 742]
emilio2 = origen[origen['MedicoCod'] == 3742]

rta_emilio = f"Se utiliza al DR EMILIO MORENO con el codigo 742 Y 3742 en {len(emilio) + len(emilio2)} registros"

      
      
libardo = origen[origen['MedicoCod'] == 3178]
libardo2 = origen[origen['MedicoCod'] == 2467]
rta_libardo = f"Se utiliza al DR JOSE LIBARDO BENAVIDES TAPIA 3178 Y 2467 en {len(libardo) + len(libardo2)} registros"

sede2 = origen[origen['MedicoCod'] == 5023]

rta_sede2 = f"Se utiliza al SEDE 2 : ELIANA ALEJANDRA DELGADO  MARCILLO con el codigo 5023 en {len(sede2)} registros"

#region BACTERIOLOGIA
bacteriologia = origen[origen['EspeNom'] == "BACTERIOLOGIA"]
rta_bacteriologia = f"Se utiliza BACTERIOLOGIA como especialista formulando medicamentos en {len(bacteriologia)} registros"


#region revision cantidades

#organizar dataframe por producto y fecha

origen = origen.sort_values(by=['COD13', 'fecha'])

#agrupamos por producto
origen["variacion"] = origen.groupby('COD13')["dCantidad"].diff()

estadisticas = origen.groupby('COD13')["dCantidad"].agg(["mean", "std"]).reset_index()

origen = origen.merge(estadisticas, on="COD13", how="left")

origen["es_pico"] = np.where(np.abs(origen["dCantidad"] - origen["mean"]) >2 * origen["std"], True, False)

picos = origen[origen["es_pico"]]

picos = picos[['Mes', 'fecha', 'TipDoc4','DescTipDoc', 'NroMov','COD13', 'Ref', 'Producto', 'dCantidad', 'dValor', "variacion", "mean", "std"]]

"""
Index(['TipMovFiltro', 'FechaDesde', 'FechaHasta', 'Mes', 'fecha', 'TipDoc4',
       'DescTipDoc', 'NroMov', 'SecMov', 'BodegaMov', 'BOD4', 'NombreBod',
       'CentroMov', 'cc_Nombre', 'ScentroMov', 'scc_Nombre', 'MedicoCod',
       'MedicoNom', 'EspeCod', 'EspeNom', 'COD13', 'Ref', 'Producto', 'LinInv',
       'Linea', 'GruInv', 'Grupo', 'CtaInv', 'CtaCruce', 'dCantidad', 'dValor',
       'Veces', 'origenMed', 'IdPaciente', 'NomPaciente'],
      dtype='object')
      
"""

result_data = {
      "Hallazgos": [res_municipios, res_no_determinado, res_domiciliaria, res_pym, res_enfer_in_mgral, res_espe_in_mgral,  res_mgral_in_esp, res_enfer_in_esp, res_odon_in_esp, 
      res_ofta_in_odon, res_mgral_in_odon, res_cirugia, rsta_luis_fdo_caicedo, rta_maurimelo_maurodri, rta_melo_dolypantoja, rta_calpa, rta_emilio, rta_libardo, rta_sede2, 
      rta_bacteriologia]
}

mes = input("Cual es tu mes en revision? ")

hallazgos_medicamentos = pd.DataFrame(result_data)

try:
      hallazgos_medicamentos.to_excel(f"Hallazgos/HALLAZGOS MES DE {mes.upper()} DE 2025.xlsx")
      print("El archivo de hallazgos se exporto satisfactoriamente")
except:
      print("No se pudo exportar el archivo")

try:
      picos.to_excel(f"Hallazgos/analisis_cantidades/ANALISIS CANTIDADES MES DE {mes.upper()} DE 2025.xlsx")
      print("El archivo de analisis se exporto satisfactoriamente")

except:
      print("No se pudo exportar el archivo de analisis de cantidades")