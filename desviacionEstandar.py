import math
import csv

#Iniciamos la obtencion de datos de un archivo en formato csv
ruta_archivo = "C:\\Users\\iroba\\Downloads\\diabetes.csv"

# Abremos el archivo CSV y cargamos los datos en una lista de diccionarios
with open(ruta_archivo, mode='r') as archivo:
    contenido = csv.DictReader(archivo)
    dataset = [fila for fila in contenido]   # >>> Guardamos los datos en una lista de listas iterando fila por fila


#Guardamos los datos de la columna que nos interesa analizar (en este caso: col 08 >>> Edad)
datos_originales = [float(fila["Age"]) for fila in dataset]

#Obtenemos el promedio de los datos
promedio = sum(datos_originales) / len(datos_originales)

#Obtenemos la varianza
def varianza(numeros):
    sumVar: float = 0
    for i in numeros:
        sumVar += (i - promedio) ** 2
    var = sumVar / (len(numeros) - 1)
    return var

desv_estandar = math.sqrt(varianza(datos_originales))
print(f"La Desviación Estandar de los datos es: {desv_estandar:.2f}")

#Pedimos el valor de 'k' al usuario
#Convertimos la entrada del usuario a float para que coinsida con el resto de nuestros calculos
k = float(input("Ingrese el valor de 'k' para calcular el teorema de Chebyshev>>> "))

#Calculamos el porcentaje torico de valores en 'k' desviaciones
def teoric_prob(k):
    return 100 * (1 - (1 / k**2))

# Calculamos cuantos valores se encuentran dentro de 'k' desviaciones estandar
def k_desviaciones(datos, k, prom, desv_esta):
    conteo = sum(1 for i in datos if abs(i - prom) <= k * desv_esta)
    return 100 * (conteo / len(datos))

proporcion_real = k_desviaciones(datos_originales, k, promedio, desv_estandar)
print(f"La proporción real de datos dentro de {k:.0f} desviaciones estándar de la media es: {proporcion_real:.2f}%")

probabilidad_teorica = teoric_prob(k)
print(f"Según el Teorema de Chebyshev, al menos el {(probabilidad_teorica):.2f}% de los datos deberían estar dentro de {k:.0f} desviaciones estándar.")
