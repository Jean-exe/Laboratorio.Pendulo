# ==============================================================================
# 1. IMPORTACION DE LIBRERIAS ESTANDAR Y VARIABLES GLOBALES
# ==============================================================================
import math        # Constante pi, raiz cuadrada (sqrt) y comparacion flotante (isclose)
import statistics  # Calculo de media (mean) y desviacion estandar muestral (stdev)
import csv         # Lectura y escritura de archivos CSV

# Lista global que almacenara tuplas inmutables de la forma (L, T)
mediciones = []

# Nombre del archivo CSV exigido por la guia
NOMBRE_ARCHIVO = "datos_pendulo.csv"


# ==============================================================================
# 2. FUNCIONES AUXILIARES DE VALIDACION Y CALCULO FISICO
# ==============================================================================

def solicitar_positivo(mensaje):
    """Solicita un numero flotante positivo al usuario, validando errores de entrada."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("Error: El valor debe ser un numero positivo mayor que cero.")
            else:
                return valor
        except ValueError:
            print("Error: Entrada no valida. Por favor, ingrese un numero.")


def calcular_g_individual(longitud, periodo):
    """Calcula la gravedad experimental g = (4 * pi^2 * L) / T^2 para una medicion."""
    return (4 * (math.pi ** 2) * longitud) / (periodo ** 2)


def obtener_lista_g():
    """Genera una lista con los valores de g correspondientes a todas las mediciones."""
    return [calcular_g_individual(L, T) for L, T in mediciones]


# ==============================================================================
# 3. FUNCIONES DE LAS OPCIONES DEL MENU PRINCIPAL
# ==============================================================================

def agregar_medicion():
    """Opcion 1: Solicita L y T, los valida y agrega la tupla (L, T) a mediciones."""
    longitud = solicitar_positivo("Longitud L (m): ")
    periodo = solicitar_positivo("Periodo T (s): ")
    mediciones.append((longitud, periodo))
    print("Medicion agregada correctamente.")


def mostrar_tabla():
    """Opcion 2: Imprime una tabla formateada a 4 decimales con todas las mediciones."""
    if not mediciones:
        print("No hay mediciones registradas.")
        return
    print("\n" + "-" * 54)
    print(f"{'N°':<6} | {'Longitud L (m)':<15} | {'Periodo T (s)':<14} | {'g (m/s^2)':<12}")
    print("-" * 54)
    # Enumerar las mediciones desde 1 y desempaquetar cada tupla (L, T)
    for indice, (L, T) in enumerate(mediciones, start=1):
        g_val = calcular_g_individual(L, T)
        print(f"{indice:<6} | {L:<15.4f} | {T:<14.4f} | {g_val:<12.4f}")
    print("-" * 54)


def calcular_g_promedio():
    """Opcion 3: Calcula media, desviacion estandar muestral e incertidumbre de g."""
    n = len(mediciones)
    if n < 2:
        print("Error: Se requieren al menos 2 mediciones para este calculo.")
        return
    valores_g = obtener_lista_g()
    media_g = statistics.mean(valores_g)          # Promedio aritmetico de g
    desviacion_g = statistics.stdev(valores_g)    # Desviacion estandar muestral (n - 1)
    incertidumbre = desviacion_g / math.sqrt(n)   # Incertidumbre estandar de la media
    print(f"\nNumero de mediciones: {n}")
    print(f"g promedio: {media_g:.4f} m/s^2")
    print(f"Desviacion estandar: {desviacion_g:.4f} m/s^2")
    print(f"Incertidumbre estandar: {incertidumbre:.4f} m/s^2")
    print(f"Resultado: g = {media_g:.4f} +/- {incertidumbre:.4f} m/s^2")


def ajuste_lineal():
    """Opcion 4: Realiza regresion lineal por minimos cuadrados para T^2 = m*L + b."""
    n = len(mediciones)
    if n < 2:
        print("Error: Se requieren al menos 2 mediciones para el ajuste lineal.")
        return
    # Definir X = L y Y = T^2
    valores_x = [L for L, _ in mediciones]
    valores_y = [T ** 2 for _, T in mediciones]
    media_x = statistics.mean(valores_x)
    media_y = statistics.mean(valores_y)
    # Calcular pendiente m e intercepto b por minimos cuadrados
    numerador = sum((x - media_x) * (y - media_y) for x, y in zip(valores_x, valores_y))
    denominador = sum((x - media_x) ** 2 for x in valores_x)
    if math.isclose(denominador, 0.0, abs_tol=1e-12):
        print("Error: No se puede realizar el ajuste porque todas las longitudes L son iguales.")
        return
    pendiente_m = numerador / denominador
    intercepto_b = media_y - (pendiente_m * media_x)
    print(f"\nEcuacion ajustada: T^2 = {pendiente_m:.4f} * L + ({intercepto_b:.4f})")
    # Estimar gravedad a partir de la pendiente m = (4 * pi^2) / g
    if math.isclose(pendiente_m, 0.0, abs_tol=1e-9):
        print("Aviso: La pendiente es practicamente cero; no se puede estimar g.")
    else:
        g_ajuste = (4 * (math.pi ** 2)) / pendiente_m
        print(f"Gravedad estimada por ajuste (g_ajuste): {g_ajuste:.4f} m/s^2")


def detectar_outliers():
    """Opcion 5: Identifica mediciones atipicas usando puntuacion estandar |z| > 2."""
    n = len(mediciones)
    if n < 3:
        print("Error: Se requieren al menos 3 mediciones para detectar outliers.")
        return
    valores_g = obtener_lista_g()
    media_g = statistics.mean(valores_g)
    desviacion_g = statistics.stdev(valores_g)
    if math.isclose(desviacion_g, 0.0, abs_tol=1e-12):
        print("Todas las mediciones tienen el mismo valor de g (desviacion = 0). No hay outliers.")
        return
    outliers_encontrados = []
    # Calcular puntaje z para cada medicion y filtrar aquellas con |z| > 2
    for indice, ((L, T), g_val) in enumerate(zip(mediciones, valores_g), start=1):
        z = (g_val - media_g) / desviacion_g
        if abs(z) > 2:
            outliers_encontrados.append((indice, L, T, g_val, z))
    if not outliers_encontrados:
        print("No se detectaron posibles outliers (ningun valor cumple |z| > 2).")
    else:
        print("\nPosibles outliers detectados (|z| > 2):")
        print("-" * 66)
        print(f"{'N°':<5} | {'L (m)':<10} | {'T (s)':<10} | {'g (m/s^2)':<12} | {'Valor z':<10}")
        print("-" * 66)
        for indice, L, T, g_val, z in outliers_encontrados:
            print(f"{indice:<5} | {L:<10.4f} | {T:<10.4f} | {g_val:<12.4f} | {z:<10.4f}")
        print("-" * 66)


def guardar_csv():
    """Opcion 6: Exporta la lista global mediciones al archivo datos_pendulo.csv."""
    if not mediciones:
        print("No hay datos para guardar en el archivo CSV.")
        return
    try:
        with open(NOMBRE_ARCHIVO, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["L_m", "T_s"])  # Encabezados exigidos
            for L, T in mediciones:
                escritor.writerow([L, T])
        print(f"Se guardaron {len(mediciones)} mediciones en '{NOMBRE_ARCHIVO}'.")
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")


def cargar_csv():
    """Opcion 7: Lee datos_pendulo.csv, valida cada fila y reemplaza mediciones."""
    global mediciones
    nuevas_mediciones = []
    try:
        with open(NOMBRE_ARCHIVO, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            encabezado = next(lector, None)  # Saltar la primera fila de encabezados
            if encabezado is None:
                print("Error: El archivo CSV esta vacio.")
                return
            # Validar formato y valores positivos antes de sobrescribir mediciones
            for numero_fila, fila in enumerate(lector, start=2):
                if len(fila) != 2:
                    raise ValueError(f"Formato incorrecto en la fila {numero_fila}.")
                L = float(fila[0])
                T = float(fila[1])
                if L <= 0 or T <= 0:
                    raise ValueError(f"Valores no positivos en la fila {numero_fila}.")
                nuevas_mediciones.append((L, T))
        if not nuevas_mediciones:
            print("El archivo no contenia mediciones validas.")
            return
        mediciones = nuevas_mediciones
        print(f"Se cargaron {len(mediciones)} mediciones correctamente desde '{NOMBRE_ARCHIVO}'.")
    except FileNotFoundError:
        print(f"Error: El archivo '{NOMBRE_ARCHIVO}' no existe.")
    except ValueError as e:
        print(f"Error de datos en el archivo CSV: {e}")
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")


# ==============================================================================
# 4. INTERFAZ DE MENU Y CICLO PRINCIPAL DE EJECUCION
# ==============================================================================

def mostrar_menu():
    """Imprime las opciones disponibles del laboratorio virtual en consola."""
    print("\n===== LABORATORIO VIRTUAL DEL PENDULO =====")
    print("1. Agregar medicion")
    print("2. Mostrar tabla de datos")
    print("3. Calcular g promedio e incertidumbre")
    print("4. Ajuste lineal T^2 vs L")
    print("5. Detectar posibles outliers")
    print("6. Guardar datos en CSV")
    print("7. Cargar datos desde CSV")
    print("8. Salir")


def main():
    """Controla el flujo principal del programa mediante un bucle infinito."""
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            agregar_medicion()
        elif opcion == "2":
            mostrar_tabla()
        elif opcion == "3":
            calcular_g_promedio()
        elif opcion == "4":
            ajuste_lineal()
        elif opcion == "5":
            detectar_outliers()
        elif opcion == "6":
            guardar_csv()
        elif opcion == "7":
            cargar_csv()
