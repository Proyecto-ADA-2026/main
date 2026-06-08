# ==============================================================================
# MEDICION Y ESTIMACION DE MEMORIA
# ==============================================================================
# Este modulo concentra la medicion real con tracemalloc y la estimacion
# profunda de las principales estructuras generadas por el proyecto.
# ==============================================================================

import sys
import tracemalloc


def tamano_profundo(objeto, vistos=None):
    """Calcula el tamano aproximado de un objeto y sus contenidos internos."""
    if vistos is None:
        vistos = set()

    obj_id = id(objeto)
    if obj_id in vistos:
        return 0

    vistos.add(obj_id)
    tamano = sys.getsizeof(objeto)

    if isinstance(objeto, dict):
        for clave, valor in objeto.items():
            tamano += tamano_profundo(clave, vistos)
            tamano += tamano_profundo(valor, vistos)
    elif isinstance(objeto, (list, tuple, set)):
        for elemento in objeto:
            tamano += tamano_profundo(elemento, vistos)
    elif hasattr(objeto, "__dict__"):
        tamano += tamano_profundo(objeto.__dict__, vistos)

    return tamano


def bytes_a_kb_mb(bytes_valor):
    """Convierte bytes a una tupla con bytes, KB y MB."""
    kb = bytes_valor / 1024
    mb = kb / 1024
    return bytes_valor, kb, mb


def estimar_memoria_estructuras(A=None, A2=None, A3=None, vector=None,
                                frecuencias=None, arbol=None):
    """Estima memoria profunda de las estructuras principales del programa."""
    memoria = {}

    if A is not None:
        memoria["Matriz A"] = tamano_profundo(A)

    if A2 is not None:
        memoria["Matriz A2"] = tamano_profundo(A2)

    if A3 is not None:
        memoria["Matriz A3"] = tamano_profundo(A3)

    if vector is not None:
        if isinstance(vector, dict):
            for nombre in vector:
                memoria["Vector " + str(nombre)] = tamano_profundo(vector[nombre])
        else:
            memoria["Vector"] = tamano_profundo(vector)

    if frecuencias is not None:
        if isinstance(frecuencias, dict) and ("A" in frecuencias or "A3" in frecuencias):
            for nombre in frecuencias:
                memoria["Frecuencias " + str(nombre)] = tamano_profundo(frecuencias[nombre])
        else:
            memoria["Frecuencias"] = tamano_profundo(frecuencias)

    if arbol is not None:
        if isinstance(arbol, dict):
            for nombre in arbol:
                memoria["Arbol " + str(nombre)] = tamano_profundo(arbol[nombre])
        else:
            memoria["Arbol binario"] = tamano_profundo(arbol)

    total = 0
    for nombre in memoria:
        total += memoria[nombre]
    memoria["Total estimado estructuras"] = total

    return memoria


def imprimir_reporte_memoria(memoria):
    """Imprime en consola un reporte legible de memoria estimada."""
    print("MEMORIA DETALLADA")
    print("-----------------")

    for nombre, bytes_valor in memoria.items():
        bytes_total, kb, mb = bytes_a_kb_mb(bytes_valor)
        print(f"{nombre:30}: {bytes_total} bytes | {kb:.2f} KB | {mb:.4f} MB")


def reporte_memoria_a_texto(memoria):
    """Convierte el reporte de memoria estimada a texto para la interfaz."""
    texto = "Estimacion detallada por estructura:\n"
    for nombre, bytes_valor in memoria.items():
        bytes_total, kb, mb = bytes_a_kb_mb(bytes_valor)
        texto += "- " + str(nombre) + ": "
        texto += str(bytes_total) + " bytes | "
        texto += f"{kb:.2f} KB | {mb:.4f} MB\n"
    return texto


def iniciar_medicion_memoria():
    """Inicia el rastreo de uso de memoria utilizando tracemalloc."""
    tracemalloc.start()


def obtener_memoria_actual_y_pico():
    """Retorna memoria actual y pico maximo desde tracemalloc."""
    actual, pico = tracemalloc.get_traced_memory()
    return actual, pico


def detener_medicion_memoria():
    """Detiene el rastreador de memoria de tracemalloc."""
    tracemalloc.stop()


def estimar_memoria_matriz(n):
    """Mantiene compatibilidad con la estimacion simple de una matriz n x n."""
    return n * n * 28
