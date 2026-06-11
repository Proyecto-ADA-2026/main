# ==============================================================================
# MEDICION Y ESTIMACION DE MEMORIA
# ==============================================================================
# Este modulo tiene DOS enfoques para medir memoria:
#
#   1. ESTIMACION PROFUNDA con sys.getsizeof():
#      Recorre recursivamente un objeto Python y suma el tamaño de cada parte.
#      Es una ESTIMACION porque Python reutiliza objetos internamente y
#      sys.getsizeof solo mide el contenedor, no el contenido.
#      Por eso se usa tamano_profundo() que baja hasta cada elemento.
#
#   2. MEDICION REAL con tracemalloc:
#      tracemalloc es el modulo oficial de Python para rastrear asignaciones
#      de memoria en tiempo de ejecucion. Mide lo que REALMENTE usa el proceso
#      en bytes, con precision de bloque de asignacion.
#      get_traced_memory() retorna (actual, pico) en bytes.
# ==============================================================================

import sys          # sys.getsizeof(obj): retorna bytes que ocupa el objeto en memoria.
import tracemalloc  # Modulo estandar para rastrear uso de memoria con start/stop.


def tamano_profundo(objeto, vistos=None):
    """Calcula el tamaño de memoria de un objeto y TODOS sus contenidos internos.

    PROBLEMA con sys.getsizeof(): solo mide la 'carcasa' del objeto, no lo que
    contiene. Por ejemplo, sys.getsizeof([1,2,3]) retorna el tamaño de la lista
    pero NO el tamaño de los enteros 1, 2, 3 almacenados dentro.

    SOLUCION: recursion profunda que suma el tamaño de cada elemento contenido.

    PROTECCION CONTRA CICLOS: se usa 'vistos' (conjunto de ids) para no entrar
    en un ciclo infinito si dos objetos se referencian mutuamente.
    id(objeto) es el identificador unico en memoria de un objeto Python.
    """
    if vistos is None:
        vistos = set()              # Inicializa el conjunto de ids visitados en la primera llamada.

    obj_id = id(objeto)             # Identificador unico del objeto en memoria (su direccion).
    if obj_id in vistos:
        return 0                    # Ya se proceso este objeto: no lo cuenta de nuevo (evita ciclos).

    vistos.add(obj_id)              # Marca este objeto como visitado.
    tamano = sys.getsizeof(objeto)  # Tamaño del contenedor del objeto (sin sus contenidos).

    if isinstance(objeto, dict):    # Para diccionarios, suma tamaño de claves y valores.
        for clave, valor in objeto.items():
            tamano += tamano_profundo(clave, vistos)  # Suma tamaño de cada clave.
            tamano += tamano_profundo(valor, vistos)  # Suma tamaño de cada valor.
    elif isinstance(objeto, (list, tuple, set)): # Para secuencias, suma tamaño de cada elemento.
        for elemento in objeto:
            tamano += tamano_profundo(elemento, vistos)
    elif hasattr(objeto, "__dict__"): # Para objetos con atributos (clases), suma su diccionario interno.
        tamano += tamano_profundo(objeto.__dict__, vistos) # __dict__ contiene todos los atributos.

    return tamano                   # Tamaño total aproximado del objeto y todos sus contenidos.


def bytes_a_kb_mb(bytes_valor):
    """Convierte un valor en bytes a su equivalente en KB y MB.

    Retorna una tupla de tres valores para facilitar la presentacion en distintas
    unidades segun lo que sea mas legible (bytes para valores chicos, MB para grandes).
    """
    kb = bytes_valor / 1024         # 1 KB = 1024 bytes.
    mb = kb / 1024                  # 1 MB = 1024 KB = 1048576 bytes.
    return bytes_valor, kb, mb      # Tupla: (bytes, kilobytes, megabytes).


def estimar_memoria_estructuras(A=None, A2=None, A3=None, vector=None,
                                frecuencias=None, arbol=None):
    """Estima la memoria de las estructuras principales del programa con tamano_profundo().

    PARAMETROS OPCIONALES: cada estructura puede ser None si no se genero.
    Los parametros 'vector', 'frecuencias' y 'arbol' pueden ser:
      - Un objeto simple: se guarda bajo un nombre generico.
      - Un dict {nombre: objeto}: se guarda cada estructura con su propio nombre.
        Esto permite distinguir entre el vector de A y el de A3, por ejemplo.

    Retorna un diccionario {nombre_estructura: bytes_estimados} con un campo
    adicional "Total estimado estructuras" que suma todos los valores.
    """
    memoria = {}                    # Diccionario resultado: nombre -> bytes.

    if A is not None:
        memoria["Matriz A"] = tamano_profundo(A)    # Tamaño de la matriz A original.

    if A2 is not None:
        memoria["Matriz A2"] = tamano_profundo(A2)  # Tamaño de la matriz intermedia A^2.

    if A3 is not None:
        memoria["Matriz A3"] = tamano_profundo(A3)  # Tamaño de la matriz A^3.

    if vector is not None:
        if isinstance(vector, dict):                # Si es un dict, cada clave es un nombre de vector.
            for nombre in vector:
                memoria["Vector " + str(nombre)] = tamano_profundo(vector[nombre])
        else:                                       # Si es un objeto simple, nombre generico.
            memoria["Vector"] = tamano_profundo(vector)

    if frecuencias is not None:
        if isinstance(frecuencias, dict) and ("A" in frecuencias or "A3" in frecuencias):
            for nombre in frecuencias:              # Dict con claves "A" y "A3".
                memoria["Frecuencias " + str(nombre)] = tamano_profundo(frecuencias[nombre])
        else:
            memoria["Frecuencias"] = tamano_profundo(frecuencias)

    if arbol is not None:
        if isinstance(arbol, dict):                 # Dict con los dos arboles (A y A3).
            for nombre in arbol:
                memoria["Arbol " + str(nombre)] = tamano_profundo(arbol[nombre])
        else:
            memoria["Arbol binario"] = tamano_profundo(arbol)

    total = 0                       # Acumula la suma de todos los tamaños individuales.
    for nombre in memoria:
        total += memoria[nombre]
    memoria["Total estimado estructuras"] = total   # Agrega el total como campo final del dict.

    return memoria


def imprimir_reporte_memoria(memoria):
    """Imprime en consola el reporte de memoria estimada en formato tabla.

    Se usa principalmente para pruebas desde la terminal, no desde la interfaz.
    """
    print("MEMORIA DETALLADA")
    print("-----------------")

    for nombre, bytes_valor in memoria.items():      # Itera sobre cada estructura y su tamaño.
        bytes_total, kb, mb = bytes_a_kb_mb(bytes_valor)
        print(f"{nombre:30}: {bytes_total} bytes | {kb:.2f} KB | {mb:.4f} MB")


def reporte_memoria_a_texto(memoria):
    """Convierte el dict de memoria estimada a un string multilinea para la interfaz.

    Alternativa a imprimir_reporte_memoria() que devuelve texto en lugar de imprimirlo,
    para poder mostrarlo en el widget Text de la interfaz grafica.
    """
    texto = "Estimacion detallada por estructura:\n"
    for nombre, bytes_valor in memoria.items():
        bytes_total, kb, mb = bytes_a_kb_mb(bytes_valor)
        texto += "- " + str(nombre) + ": "
        texto += str(bytes_total) + " bytes | "
        texto += f"{kb:.2f} KB | {mb:.4f} MB\n"  # Formato con 2 decimales para KB y 4 para MB.
    return texto


def iniciar_medicion_memoria():
    """Inicia el rastreo de asignaciones de memoria con tracemalloc.

    COMO FUNCIONA tracemalloc:
      Al llamar start(), Python comienza a registrar cada malloc (asignacion de
      memoria) que ocurre. Se puede consultar con get_traced_memory() cuanta
      memoria se ha asignado desde que se llamo start().
    Se debe llamar ANTES de crear las estructuras que se quiere medir.
    """
    tracemalloc.start()             # Activa el rastreador de memoria de Python.


def obtener_memoria_actual_y_pico():
    """Retorna la memoria actual usada y el pico maximo desde que se inicio tracemalloc.

    RETORNO: tupla (actual, pico) en bytes.
      - actual: memoria asignada y aun no liberada en este momento.
      - pico: la mayor cantidad de memoria simultaneamente asignada desde start().

    El pico es util para saber el maximo consumo durante el calculo de A3,
    aunque luego se libere parte de esa memoria.
    """
    actual, pico = tracemalloc.get_traced_memory() # Consulta el estado actual del rastreador.
    return actual, pico             # Ambos valores en bytes.


def detener_medicion_memoria():
    """Detiene el rastreador de memoria y libera los recursos de tracemalloc.

    Se debe llamar despues de obtener_memoria_actual_y_pico() para no
    consumir memoria adicional rastreando operaciones posteriores.
    """
    tracemalloc.stop()              # Desactiva el rastreador y libera su memoria interna.


def estimar_memoria_matriz(n):
    """Estima la memoria de una matriz n x n con formula simple.

    FORMULA: n * n * 28 bytes.
    - n*n: cantidad total de elementos.
    - 28 bytes: tamaño aproximado de un entero Python de un digito en memoria.
      (Los enteros Python no son simples int de 4 bytes; tienen overhead de objeto).
    Esta es una estimacion rapida de compatibilidad para cuando no se tiene
    la matriz real construida todavia.
    """
    return n * n * 28               # Estimacion: cada entero Python ocupa ~28 bytes.
