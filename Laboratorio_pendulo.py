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
