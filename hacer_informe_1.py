import pandas as pd

mes = input("ingrese el mes: ").upper()
consumo = pd.read_excel(f"Arreglados/CONSUMO PACIENTES DEL MES DE {mes} DE 2025.xlsx", sheet_name="Sheet1")
entradas = pd.read_excel("entradas/901S055-InformeConsumos-SEP2025.xlsx", sheet_name="Es")
cruce_cc = pd.read_excel("otros_informes/para_cruzar_6.xlsx")

#dejando solo 6135JU
consumo = consumo.loc[consumo["CtaCruce"].isin([6135050100,6135050200,6135100000, 6135150000,6135050300,6135400000,6135450000,6135300000, 6135350000,6135200000,6135250000,6135050400])]

entradas = entradas.loc[entradas["CtaCruce"].isin([6135050100,6135050200,6135100000, 6135150000,6135050300,6135400000,6135450000,6135300000, 6135350000,6135200000,6135250000,6135050400])]

#arreglando negativos
consumo["dValor"] = consumo["dValor"].abs().astype(float).round(2)
consumo["dCantidad"] = consumo["dCantidad"].abs().astype(float).round(2)

medicamentos_consumos = consumo.loc[(consumo["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))& (consumo['origenMed'] == "SIMA")]
medicamentos_entradas = entradas.loc[entradas["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"])]

#print(f"numero de registros para medicamentos_consumos: {len(medicamentos_consumos)}")
pasto_medicamentos = medicamentos_consumos.loc[medicamentos_consumos['TipDoc4'] != "S014"]
#print(f"numero de registros para pasto_medicamentos: {len(pasto_medicamentos)}")
mpios_medicamentos = medicamentos_consumos.loc[medicamentos_consumos['TipDoc4'] == "S014"]
#print(f"numero de registros para mpios_medicamentos: {len(mpios_medicamentos)}")

#region Tablas consumo medicamentos
para_td1 = pasto_medicamentos[~pasto_medicamentos["scc_Nombre"].isin(["APOYO DIAGNOSTICO", "MEDICINA ESPECIALIZADA", "APOYO TERAPEUTICO"])]
td1 = para_td1.pivot_table(values="dValor", index="scc_Nombre", aggfunc="sum").reset_index()

para_td2 = pasto_medicamentos[pasto_medicamentos["scc_Nombre"].isin(["APOYO DIAGNOSTICO", "MEDICINA ESPECIALIZADA", "APOYO TERAPEUTICO"])]
td2 = para_td2.pivot_table(values="dValor", index="EspeNom", aggfunc="sum").reset_index()
td2.columns = ["scc_Nombre", "dValor"]

td3 = mpios_medicamentos.pivot_table(values="dValor", index='NombreBod', aggfunc="sum").reset_index()
td3.columns = ["scc_Nombre", "dValor"]

para_td4 = consumo.loc[(consumo["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))& (consumo['origenMed'] == "SIIGO")]
td4 = para_td4.pivot_table(values="dValor", index='MedicoNom', aggfunc="sum").reset_index()
td4.columns = ["scc_Nombre", "dValor"]

total_consumo_medicamentos = pd.concat([td1, td2, td3, td4], axis=0, ignore_index=True)

#agregar cruce cc

para_distr_medica = pd.merge(total_consumo_medicamentos, cruce_cc, left_on="scc_Nombre", right_on="CENTRO DE COSTO", how="left")

valor_nulos = para_distr_medica[para_distr_medica["CORRECCION"].isnull()]
#print(valor_nulos)

DISTRIBUIR_NULOS = valor_nulos.dValor.sum()

para_distribucion = para_distr_medica[para_distr_medica["CORRECCION"].notnull()]
TOTAL_DISTRIBUCION = para_distribucion.dValor.sum()
para_distribucion["distribuido"] = para_distribucion.dValor + ((para_distribucion["dValor"] * DISTRIBUIR_NULOS ) / TOTAL_DISTRIBUCION)

#total consumo de medicamentos
td_distribucion = para_distribucion.pivot_table(values="distribuido", index="CORRECCION", aggfunc="sum").reset_index()


#region Entrada Medicamentos
para_t1_entradas_med = medicamentos_entradas.loc[~medicamentos_entradas["scc.Nombre"].isin(["MEDICINA ESPECIALIZADA", "PASTO"]) ]
t1_entradas_med = para_t1_entradas_med.pivot_table(values="DValor", index="scc.Nombre", aggfunc="sum").reset_index()

para_t2_entradas_med = medicamentos_entradas.loc[medicamentos_entradas["scc.Nombre"].isin(["MEDICINA ESPECIALIZADA", "PASTO"]) ]
t2_entradas_med = para_t2_entradas_med.pivot_table(values="DValor", index="EspeNom", aggfunc="sum").reset_index()
t2_entradas_med.columns = ["scc.Nombre", "DValor"]

entradas_medicamentos = pd.concat([t1_entradas_med, t2_entradas_med], axis=0, ignore_index=True)
entradas_medicamentos = pd.pivot_table(entradas_medicamentos, values="DValor", index="scc.Nombre", aggfunc="sum").reset_index()

#agregar cruce cc
para_distr_entradas = pd.merge(entradas_medicamentos, cruce_cc, left_on="scc.Nombre", right_on="CENTRO DE COSTO", how="left")

#region Total Medicamentos
medicamentos = pd.merge(td_distribucion, para_distr_entradas, on="CORRECCION", how="left")
medicamentos["DValor"] = medicamentos["DValor"].fillna(0)
medicamentos["Total"] = medicamentos["distribuido"] - medicamentos["DValor"]

#print(medicamentos.distribuido.sum())
#print(medicamentos.DValor.sum())

#print(medicamentos)

td_total = medicamentos.pivot_table(values="Total", index="CORRECCION", aggfunc="sum").reset_index()

print(td_total)
print(f"El total de consumo de medicamentos es {td_distribucion.distribuido.sum()}")
print(f"El total de entradas de medicamentos es {entradas_medicamentos.DValor.sum()}")
print(f"El total de medicamentos deberia ser  {td_distribucion.distribuido.sum() - entradas_medicamentos.DValor.sum()}")

print(f"este es valor que esta dando el {td_total.Total.sum()}")

#region dispositivos medicos

dispositivos_consumo = consumo.loc[(~consumo["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))& (consumo['origenMed'] == "SIMA")]

print(dispositivos_consumo.dValor.sum())


dispositivos_entradas = entradas.loc[~entradas["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"])]

pasto_dispositivos = dispositivos_consumo.loc[dispositivos_consumo['TipDoc4'] != "S014"]
mpios_dispositivos = dispositivos_consumo.loc[dispositivos_consumo['TipDoc4'] == "S014"]

print(pasto_dispositivos.dValor.sum() + mpios_dispositivos.dValor.sum())

para_td1_dispositivos = pasto_dispositivos[~pasto_dispositivos["scc_Nombre"].isin(["APOYO DIAGNOSTICO", "MEDICINA ESPECIALIZADA", "APOYO TERAPEUTICO"])]
td1_dispositivos = para_td1_dispositivos.pivot_table(values="dValor", index="scc_Nombre", aggfunc="sum").reset_index()
td1_dispositivos.columns = ["scc_Nombre", "dValor"]

para_td2_dispositivos = pasto_dispositivos[pasto_dispositivos["scc_Nombre"].isin(["APOYO DIAGNOSTICO", "MEDICINA ESPECIALIZADA", "APOYO TERAPEUTICO"])]
td2_dispositivos = para_td2_dispositivos.pivot_table(values="dValor", index="EspeNom", aggfunc="sum").reset_index()
td2_dispositivos.columns = ["scc_Nombre", "dValor"]


para_td3_dispositivos = mpios_dispositivos.pivot_table(values="dValor", index='NombreBod', aggfunc="sum").reset_index()
td3_dispositivos = para_td3_dispositivos.pivot_table(values="dValor", index='NombreBod', aggfunc="sum").reset_index()
td3_dispositivos.columns = ["scc_Nombre", "dValor"]

print(td1_dispositivos.dValor.sum() + td2_dispositivos.dValor.sum() + td3_dispositivos.dValor.sum())

total_dispositivos = pd.concat([td1_dispositivos, td2_dispositivos, td3_dispositivos], axis=0, ignore_index=True)

print(total_dispositivos.dValor.sum()) #hasta aqui esta bien 🆗

para_distr_dispositivos = pd.merge(total_dispositivos, cruce_cc, left_on="scc_Nombre", right_on="CENTRO DE COSTO", how="left")

para_distr_dispositivos = pd.pivot_table(para_distr_dispositivos, values="dValor", index="CORRECCION", aggfunc="sum").reset_index()
para_distr_dispositivos.columns = ["CORRECCION", "dValor"]

print(para_distr_dispositivos.dValor.sum()) #hasta aqui esta bien 🆗


#entrada de dispositivos medicos
print("-------- ahora revisamos entradas -------------")
print(dispositivos_entradas.DValor.sum())
para_entrada_dispo = dispositivos_entradas.loc[~dispositivos_entradas['scc.Nombre'].isin(["MEDICINA ESPECIALIZADA", "PASTO"]) ]
para_entrada_dispo2 = dispositivos_entradas.loc[dispositivos_entradas['scc.Nombre'].isin(["MEDICINA ESPECIALIZADA", "PASTO"]) ]

td1_entrada_dispo = para_entrada_dispo.pivot_table(values="DValor", index="scc.Nombre", aggfunc="sum").reset_index()
td2_entrada_dispo = para_entrada_dispo2.pivot_table(values="DValor", index="EspeNom", aggfunc="sum").reset_index()
td2_entrada_dispo.columns = ["scc.Nombre", "DValor"]

entrada_dispositivos = pd.concat([td1_entrada_dispo, td2_entrada_dispo], axis=0, ignore_index=True)

print(entrada_dispositivos)

print(entrada_dispositivos.DValor.sum())

entrada_dispositivos.DValor = entrada_dispositivos.DValor.fillna(0)
entrada_dispositivos = pd.merge(entrada_dispositivos, cruce_cc, left_on="scc.Nombre", right_on="CENTRO DE COSTO", how="left")

entrada_dispositivos = pd.pivot_table(entrada_dispositivos, values="DValor", index="CORRECCION", aggfunc="sum").reset_index().fillna(0)
entrada_dispositivos.columns = ["CORRECCION", "DValor"]

print(entrada_dispositivos.DValor.sum())

#region total dispositivos medicos
dispositivos_formulados = pd.merge(para_distr_dispositivos, entrada_dispositivos, on="CORRECCION",how="left")
dispositivos_formulados["DValor"] = dispositivos_formulados["DValor"].fillna(0)
dispositivos_formulados["Total"] = dispositivos_formulados["dValor"] - dispositivos_formulados["DValor"]

total_dispositivos_formulados = dispositivos_formulados.pivot_table(values="Total", index="CORRECCION", aggfunc="sum").reset_index()

#region dispositivos de consumo

dispositivos_de_consumo = consumo.loc[(~consumo["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))& (consumo['origenMed'] == "SIIGO") & (~consumo['BOD4'].isin([3,9901,9902,9903,9904]))].copy()

dispositivos_de_consumo["dValor"] = dispositivos_de_consumo["dValor"].astype(int)
total_dis_de_consumo = pd.pivot_table(dispositivos_de_consumo, values="dValor", index="MedicoNom", aggfunc="sum").reset_index()
total_dis_de_consumo.columns = ["MedicoNom", "dValor"]



#region insumos
insumos = consumo.loc[(~consumo["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"])) & (consumo['origenMed'] == "SIIGO") & (consumo['BOD4'].isin([3,9901,9902,9903,9904]))].copy()

insumos["dValor"] = insumos["dValor"].astype(int)
total_insumos = pd.pivot_table(insumos, values="dValor", index="MedicoNom", aggfunc="sum").reset_index()
total_insumos.columns = ["MedicoNom", "dValor"]

verificacion = pd.pivot_table(consumo, values="dValor", index='CtaCruce', aggfunc="sum").reset_index()
verificacion_entradas = pd.pivot_table(entradas, values="DValor", index='CtaCruce', aggfunc="sum").reset_index()

try:    
    with pd.ExcelWriter(f"informes de consumo/Informe de Consumos {mes.capitalize()} de 2025.xlsx") as writer:
        td_total.to_excel(writer, sheet_name="Consumo Medicamentos", index=False)
        total_dispositivos_formulados.to_excel(writer, sheet_name="Dispositivos Medicos", index=False)
        total_dis_de_consumo.to_excel(writer, sheet_name="Dispositivos de Consumo", index=False)
        total_insumos.to_excel(writer, sheet_name="Insumos", index=False)
        verificacion.to_excel(writer, sheet_name="Verificacion Consumos", index=False)
        verificacion_entradas.to_excel(writer, sheet_name="Verificacion Entradas", index=False)
        print("SE REALIZO LA EXPORTACION ADECUADAMENTE")
except Exception as e:
    print(e)
    print("NO SE REALIZO LA EXPORTACION ADECUADAMENTE")