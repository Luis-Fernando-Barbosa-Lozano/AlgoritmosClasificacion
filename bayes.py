# Leer y preparar los datos
def cargar_datos(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    datos = [linea.strip().split(',') for linea in lineas]
    return datos

# Separar datos en clases y atributos
def separar_datos(datos):
    clases = [fila[0] for fila in datos]
    atributos = [fila[1:] for fila in datos]
    return clases, atributos

# Calcular probabilidades a priori
def calcular_probabilidades_a_priori(clases):
    total = len(clases)
    probabilidades = {}
    for clase in clases:
        if clase not in probabilidades:
            probabilidades[clase] = 0
        probabilidades[clase] += 1
    for clave in probabilidades:
        probabilidades[clave] /= total
    return probabilidades

# Calcular probabilidades condicionales
def calcular_probabilidades_condicionales(clases, atributos):
    probabilidades = {}
    total_por_clase = {clase: clases.count(clase) for clase in set(clases)}

    for clase in set(clases):
        probabilidades[clase] = [{} for _ in range(len(atributos[0]))]

    for i, fila in enumerate(atributos):
        clase_actual = clases[i]
        for j, valor in enumerate(fila):
            if valor not in probabilidades[clase_actual][j]:
                probabilidades[clase_actual][j][valor] = 0
            probabilidades[clase_actual][j][valor] += 1

    for clase, listas in probabilidades.items():
        for i, diccionario in enumerate(listas):
            for valor in diccionario:
                diccionario[valor] /= total_por_clase[clase]

    return probabilidades

# Clasificar un nuevo registro
def clasificar(registro, probabilidades_a_priori, probabilidades_condicionales):
    max_probabilidad = -1
    mejor_clase = None

    for clase in probabilidades_a_priori:
        probabilidad = probabilidades_a_priori[clase]
        for i, valor in enumerate(registro):
            if valor in probabilidades_condicionales[clase][i]:
                probabilidad *= probabilidades_condicionales[clase][i][valor]
            else:
                probabilidad *= 0  # Caso de valor no encontrado

        if probabilidad > max_probabilidad:
            max_probabilidad = probabilidad
            mejor_clase = clase

    return mejor_clase

# Calcular métricas de evaluación
def calcular_métricas(predicciones, reales):
    tp = sum(1 for p, r in zip(predicciones, reales) if p == r == 'p')
    tn = sum(1 for p, r in zip(predicciones, reales) if p == r == 'e')
    fp = sum(1 for p, r in zip(predicciones, reales) if p == 'p' and r == 'e')
    fn = sum(1 for p, r in zip(predicciones, reales) if p == 'e' and r == 'p')

    exactitud = (tp + tn) / len(reales)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    sensibilidad = tp / (tp + fn) if (tp + fn) > 0 else 0

    return exactitud, precision, sensibilidad

# Programa principal
def main():
    ruta_archivo = "agaricus-lepiota.data"
    datos = cargar_datos(ruta_archivo)
    clases, atributos = separar_datos(datos)

    # Dividir datos en entrenamiento y prueba (manual)
    punto_corte = int(len(datos) * 0.8)
    clases_entrenamiento = clases[:punto_corte]
    atributos_entrenamiento = atributos[:punto_corte]
    clases_prueba = clases[punto_corte:]
    atributos_prueba = atributos[punto_corte:]

    # Entrenar el modelo
    probabilidades_a_priori = calcular_probabilidades_a_priori(clases_entrenamiento)
    probabilidades_condicionales = calcular_probabilidades_condicionales(clases_entrenamiento, atributos_entrenamiento)

    # Evaluar en datos de prueba
    predicciones = [clasificar(registro, probabilidades_a_priori, probabilidades_condicionales) for registro in
                    atributos_prueba]
    exactitud, precision, sensibilidad = calcular_métricas(predicciones, clases_prueba)

    print(f"Exactitud: {exactitud:.2f}, Precisión: {precision:.2f}, Sensibilidad: {sensibilidad:.2f}")

    # Clasificar un nuevo registro
    nuevo_registro = input("Introduce un nuevo registro con 22 atributos separados por comas: ").split(',')
    resultado = clasificar(nuevo_registro, probabilidades_a_priori, probabilidades_condicionales)
    print(f"El hongo es {'comestible' if resultado == 'e' else 'venenoso'}.")

if __name__ == "__main__":
    main()
