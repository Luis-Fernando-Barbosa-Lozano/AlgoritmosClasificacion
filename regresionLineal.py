import matplotlib.pyplot as plt

def promedio(datos):
    return sum(datos) / len(datos)

def calc_betas(x, y):
    x_promedio = promedio(x)
    y_promedio = promedio(y)

    numerador = sum((x_i - x_promedio) * (y_i - y_promedio) for x_i, y_i in zip(x, y))
    denominador = sum((x_i - x_promedio) ** 2 for x_i in x)

    beta1 = numerador / denominador
    beta0 = y_promedio - beta1 * x_promedio

    return beta0, beta1

def predecir(x, beta0, beta1):
    return [beta0 + beta1 * x_i for x_i in x]

def coeficiente_determinacion(y_real, y_pred):
    y_promedio = promedio(y_real)
    error_cuadratico = sum((y_i - y_promedio) ** 2 for y_i in y_real)
    residuos_cuadraticos = sum((y_real_i - y_pred_i) ** 2 for y_real_i, y_pred_i in zip(y_real, y_pred))

    r2 = 1 - (residuos_cuadraticos / error_cuadratico)
    return r2

def leer_datos_txt(archivo):
    datos = []
    with open(archivo, 'r') as file:
        for linea in file:
            datos.append([float(valor) for valor in linea.strip().split('\t')])
    return datos

def leer_datos_csv(archivo):
    datos = []
    with open(archivo, 'r') as file:
        next(file)  # Salta la línea del encabezado
        for linea in file:
            datos.append([float(valor) for valor in linea.strip().split(',')])
    return datos

def leave_one_out(x, y):
    errores = []  # Almacena los errores en cada iteración

    n = len(x)  # Número de datos

    # Iteramos sobre cada dato (dejando uno fuera en cada ciclo)
    for i in range(n):
        # Dividir en conjunto de entrenamiento y prueba
        x_entrenamiento = [x[j] for j in range(n) if j != i]
        y_entrenamiento = [y[j] for j in range(n) if j != i]
        x_prueba = x[i]
        y_prueba = y[i]

        # Entrenamos el modelo usando los datos de entrenamiento
        beta0, beta1 = calc_betas(x_entrenamiento, y_entrenamiento)

        # Predecimos para el dato que dejamos fuera
        y_pred_prueba = predecir([x_prueba], beta0, beta1)[0]  # Solo un valor

        # Calculamos el error cuadrático para este punto
        error = (y_prueba - y_pred_prueba) ** 2
        errores.append(error)

    # Devolver el error promedio (raíz del error cuadrático medio)
    mse = (sum(errores) / n)
    return mse

archivos_iris = ["iris_setosa.txt", "iris_versicolor.txt", "iris_virginica.txt"]
archivo_forest = "forestfires.csv"

print("Elige el archivo que deseas analizar:")
print("1. Iris Setosa")
print("2. Iris Versicolor")
print("3. Iris Virginica")
print("4. Forest Fires")

opcion = int(input("Ingresa el número del archivo: "))

if opcion in [1, 2, 3]:
    archivo_seleccionado = archivos_iris[opcion - 1]
    datos = leer_datos_txt(archivo_seleccionado)
    atributos = ["Longitud del sépalo", "Ancho del sépalo", "Longitud del pétalo", "Ancho del pétalo"]
elif opcion == 4:
    archivo_seleccionado = archivo_forest
    datos = leer_datos_csv(archivo_forest)
    atributos = ["Temperatura", "Humedad Relativa", "Velocidad del viento", "Cantidad de lluvia", "Área siniestrada"]
else:
    print("Opción inválida.")
    exit()

# Selección de atributos
print("Elige el par de atributos para la regresión lineal:")
for i, atributo in enumerate(atributos, start=1):
    print(f"{i}. {atributo}")

x_index = int(input("¿Qué atributo quieres usar como 'x' (entrada)? Ingresa el número: ")) - 1
y_index = int(input("¿Qué atributo quieres usar como 'y' (salida)? Ingresa el número: ")) - 1

# Extraemos las columnas seleccionadas
x = [fila[x_index] for fila in datos]
y = [fila[y_index] for fila in datos]

print(f"Has elegido {atributos[x_index]} como 'x' y {atributos[y_index]} como 'y'.")

# Cálculo de betas
beta0, beta1 = calc_betas(x, y)
y_pred = predecir(x, beta0, beta1)
r2 = coeficiente_determinacion(y, y_pred)

# Mostrar coeficiente de determinación
print(f"El coeficiente de determinación (R²) es: {r2:.4f}")

rmse = leave_one_out(x, y)
print(f"El MSE usando Leave-One-Out Cross Validation es: {rmse:.4f}")

# Graficar los resultados
plt.scatter(x, y, color='blue', label='Datos reales')
plt.plot(x, y_pred, color='red', label='Regresión lineal')
plt.xlabel(f'{atributos[x_index]}')
plt.ylabel(f'{atributos[y_index]}')
plt.title(f'Regresión lineal - {archivo_seleccionado}')
plt.legend()
plt.show()
