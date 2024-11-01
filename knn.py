import random

#Generamos base de datos
peliculas = ["Inception", "Actividad Paranormal", "Titanic", "Rápidos y Furiosos", "Forrest Gump"]
generos = ["Terror", "Acción", "Drama", "Romance", "Comedia"]

def generar_base_datos(num_registros=500):
    base_datos = []
    for _ in range(num_registros):
        registro = {
            "Inception": random.randint(1, 10),
            "Actividad Paranormal": random.randint(1, 10),
            "Titanic": random.randint(1, 10),
            "Rápidos y Furiosos": random.randint(1, 10),
            "Forrest Gump": random.randint(1, 10),
            "GeneroFavorito": random.choice(generos)
        }
        base_datos.append(registro)
    return base_datos

base_datos = generar_base_datos()

for i in range(5):
    print(base_datos[i])

usuario = {
    "Inception": int(input("Califica Inception (1-10): ")),
    "Actividad Paranormal": int(input("Califica Actividad Paranormal (1-10): ")),
    "Titanic": int(input("Califica Titanic (1-10): ")),
    "Rápidos y Furiosos": int(input("Califica Rápidos y Furiosos (1-10): ")),
    "Forrest Gump": int(input("Califica Forrest Gump (1-10): "))
}
k = int(input("¿Cuántos vecinos cercanos deseas considerar (valor de K)? "))

#Calculamos los K vecinos más cercanos
def calcular_distancia(registro, usuario):
    distancia = 0
    for pelicula in peliculas:
        distancia += (registro[pelicula] - usuario[pelicula]) ** 2
    return distancia ** 0.5

# Ordenamos los registros de la base de datos por cercanía al usuario
base_datos_ordenada = sorted(base_datos, key=lambda registro: calcular_distancia(registro, usuario))

# Seleccionamos los K vecinos más cercanos
vecinos_cercanos = base_datos_ordenada[:k]

print(f"\nLos {k} vecinos más cercanos son:")
for vecino in vecinos_cercanos:
    print(vecino)

#Recomendamos películas al usuario
recomendaciones = {
    "Terror": "Actividad Paranormal",
    "Acción": "Rápidos y Furiosos",
    "Drama": "Titanic",
    "Romance": "Forrest Gump",
    "Comedia": "Inception"
}

#Contamos los géneros de los vecinos cercanos
conteo_generos = {}
for vecino in vecinos_cercanos:
    genero = vecino["GeneroFavorito"]
    conteo_generos[genero] = conteo_generos.get(genero, 0) + 1

# Generar recomendaciones
sugerencias = sorted(conteo_generos, key=conteo_generos.get, reverse=True)
print("\nTe recomendamos que veas las siguientes películas:")
for genero in sugerencias[:k]:  # Limitar a K recomendaciones
    print("-", recomendaciones[genero])
