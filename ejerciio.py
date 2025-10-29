# # Ejemplo de condicional
# numero = 10

# # Guardar el resultado de la condicional en una variable
# es_mayor = numero > 5

# # Utilizar el resultado guardado
# if es_mayor:
#     print("El número es mayor que 5")
# else:
#     print("El número es menor o igual que 5")
    
    
# carlos = 0
# carlos2 = 0

# es_mayor2 = carlos > 0 and carlos2 >0

# if es_mayor2:
#     print("cumple")
# else: 
#     print("")
    
    
from importacion import data

origen = data[data['origenMed'] == "SIMA"]

sede2 = origen[origen['MedicoCod'] == 5023]

if len(sede2)>0:
      rta_sede2 = f"Se utiliza en la SEDE 2 : ELIANA ALEJANDRA DELGADO  MARCILLO con el codigo 5023 en {len(sede2)} registros"
      
print(rta_sede2)