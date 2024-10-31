# Leer los datos desde un archivo CSV
def leer_datos(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    datos = []
    etiquetas = []

    for linea in lineas[1:]:  # Ignorar la cabecera
        elementos = linea.strip().split(',')
        try:
            registro = list(map(float, elementos[2:]))  # Atributos a partir de la columna 2
            etiqueta = 0 if elementos[1] == 'M' else 1  # 'M' -> 0, 'B' -> 1
            datos.append(registro)
            etiquetas.append(etiqueta)
        except ValueError as e:
            print(f"Error al procesar la línea: {linea}. {e}")

    return datos, etiquetas

# Calcular la media de un conjunto de datos
def calcular_media(datos):
    n = len(datos)
    d = len(datos[0])
    media = [0] * d

    for registro in datos:
        for i in range(d):
            media[i] += registro[i] / n

    return media

# Calcular la matriz de dispersión dentro de clases
def matriz_dispersion(datos, media):
    d = len(media)
    S = [[0] * d for _ in range(d)]

    for registro in datos:
        diferencia = [registro[i] - media[i] for i in range(d)]
        for i in range(d):
            for j in range(d):
                S[i][j] += diferencia[i] * diferencia[j]

    return S

# Multiplicar un vector por una matriz
def multiplicar_vector_matriz(vector, matriz):
    return [sum(vector[j] * matriz[j][i] for j in range(len(vector))) for i in range(len(matriz[0]))]

# Función L(x) para un nuevo registro
def L(x, w, b):
    return sum(w[i] * x[i] for i in range(len(x))) + b

# Inversa de matriz usando librería básica
def inversa(matriz):
    import numpy as np
    return np.linalg.inv(matriz).tolist()

# Clasificar un nuevo registro
def clasificar_nuevo_registro(w, b):
    nuevo_registro = list(map(float, input(f"Ingrese los valores para los atributos separados por coma: ").strip().split(',')))
    resultado = "Maligno" if L(nuevo_registro, w, b) > 0 else "Benigno"
    print(f"El nuevo registro ha sido clasificado como: {resultado}")

# Evaluar modelo con datos de prueba
def evaluar_modelo(X_prueba, y_prueba, w, b):
    VP = VN = FP = FN = 0
    for i in range(len(X_prueba)):
        prediccion = L(X_prueba[i], w, b) > 0
        verdadero = y_prueba[i] == 0

        if prediccion and verdadero:
            VP += 1
        elif not prediccion and not verdadero:
            VN += 1
        elif prediccion and not verdadero:
            FP += 1
        else:
            FN += 1

    exactitud = (VP + VN) / (VP + VN + FP + FN)
    precision = VP / (VP + FP) if (VP + FP) != 0 else 0
    sensibilidad = VP / (VP + FN) if (VP + FN) != 0 else 0

    print(f"\nMatriz de Confusión:")
    print(f"VP: {VP}, FP: {FP}")
    print(f"FN: {FN}, VN: {VN}")
    print(f"\nExactitud: {exactitud:.2f}")
    print(f"Precisión: {precision:.2f}")
    print(f"Sensibilidad: {sensibilidad:.2f}")

# Programa principal
def main():
    datos, etiquetas = leer_datos('cancer.csv')

    # Verificar si se cargaron datos correctamente
    print(f"Total de registros: {len(datos)}")
    print(f"Etiquetas: {set(etiquetas)}")  # Debe mostrar {0, 1}

    # Separar datos en entrenamiento (90%) y prueba (10%)
    n_entrenamiento = int(0.9 * len(datos))
    X_entrenamiento = datos[:n_entrenamiento]
    y_entrenamiento = etiquetas[:n_entrenamiento]
    X_prueba = datos[n_entrenamiento:]
    y_prueba = etiquetas[n_entrenamiento:]

    # Verificar cuántos registros de cada clase existen en el conjunto de entrenamiento
    print(f"Clase 0 (Maligno): {y_entrenamiento.count(0)} registros")
    print(f"Clase 1 (Benigno): {y_entrenamiento.count(1)} registros")

    if y_entrenamiento.count(0) == 0 or y_entrenamiento.count(1) == 0:
        print("Error: No hay suficientes datos de ambas clases en el conjunto de entrenamiento.")
        return

    # Calcular las medias de cada clase
    media_maligno = calcular_media([X_entrenamiento[i] for i in range(len(X_entrenamiento)) if y_entrenamiento[i] == 0])
    media_benigno = calcular_media([X_entrenamiento[i] for i in range(len(X_entrenamiento)) if y_entrenamiento[i] == 1])

    # Calcular la matriz de dispersión dentro de clases
    S_w_maligno = matriz_dispersion([X_entrenamiento[i] for i in range(len(X_entrenamiento)) if y_entrenamiento[i] == 0], media_maligno)
    S_w_benigno = matriz_dispersion([X_entrenamiento[i] for i in range(len(X_entrenamiento)) if y_entrenamiento[i] == 1], media_benigno)

    # Sumar las matrices de dispersión
    S_w = [[S_w_maligno[i][j] + S_w_benigno[i][j] for j in range(len(S_w_maligno[0]))] for i in range(len(S_w_maligno))]

    # Calcular el vector de proyección w y el umbral b
    S_w_inv = inversa(S_w)
    w = multiplicar_vector_matriz(media_maligno, S_w_inv)
    b = -0.5 * (sum(w[i] * media_maligno[i] for i in range(len(w))) + sum(w[i] * media_benigno[i] for i in range(len(w))))

    # Clasificar un nuevo registro
    clasificar_nuevo_registro(w, b)

    # Evaluar modelo con datos de prueba
    evaluar_modelo(X_prueba, y_prueba, w, b)

# Ejecutar el programa
if __name__ == '__main__':
    main()
