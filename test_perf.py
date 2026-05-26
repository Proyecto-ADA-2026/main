import time
import random
from interfaz_grafica import (
    crear_matriz,
    calcular_A3,
    matriz_a_vector,
    ordenar_ascendente,
    construir_arbol_equilibrado,
    buscar_en_matriz,
    buscar_en_arbol,
)


def medir_accion(nombre, func, *args):
    t0 = time.perf_counter_ns()
    res = func(*args)
    t1 = time.perf_counter_ns()
    print(f"{nombre}: {t1-t0} ns")
    return res, t1 - t0


for n in (8, 200):
    print("\n=== Prueba n=", n, "===")

    # Generar matriz
    A, t_gen = medir_accion("Generar matriz A", crear_matriz, n)

    # Calcular A3
    A3, t_a3 = medir_accion("Calcular A3", calcular_A3, A)

    # Vectorizar
    vector_A, t_vecA = medir_accion("Vectorizar A", matriz_a_vector, A)
    vector_A3, t_vecA3 = medir_accion("Vectorizar A3", matriz_a_vector, A3)

    # Ordenar (ascendente)
    vA_copy = list(vector_A)
    vA_ord, t_ordA = medir_accion("Ordenar vector A (custom)", ordenar_ascendente, vA_copy)
    vA3_copy = list(vector_A3)
    vA3_ord, t_ordA3 = medir_accion("Ordenar vector A3 (custom)", ordenar_ascendente, vA3_copy)

    # Construir árbol equilibrado
    t0 = time.perf_counter_ns()
    arbolA = construir_arbol_equilibrado(vA_ord, 0, len(vA_ord)-1)
    t1 = time.perf_counter_ns()
    t_buildA = t1 - t0
    print(f"Construir árbol A: {t_buildA} ns")

    t0 = time.perf_counter_ns()
    arbolA3 = construir_arbol_equilibrado(vA3_ord, 0, len(vA3_ord)-1)
    t1 = time.perf_counter_ns()
    t_buildA3 = t1 - t0
    print(f"Construir árbol A3: {t_buildA3} ns")

    # Seleccionar un valor a buscar (toma uno existente si es posible)
    buscado = None
    if vector_A:
        buscado = random.choice(vector_A)
    else:
        buscado = 0

    print(f"Valor a buscar: {buscado}")

    # Buscar en matriz y árbol
    _, t_bus_mat = medir_accion("Buscar en matriz A", buscar_en_matriz, A, buscado)
    _, t_bus_ar = medir_accion("Buscar en árbol A", buscar_en_arbol, arbolA, buscado)

    _, t_bus_mat3 = medir_accion("Buscar en matriz A3", buscar_en_matriz, A3, buscado)
    _, t_bus_ar3 = medir_accion("Buscar en árbol A3", buscar_en_arbol, arbolA3, buscado)

    print("Resumen tiempos (ns): gen, A3, vec, ord, buildA, buildA3, b_mat, b_ar, b_mat3, b_ar3")
    print(t_gen, t_a3, t_vecA, t_ordA, t_buildA, t_buildA3, t_bus_mat, t_bus_ar, t_bus_mat3, t_bus_ar3)

print('\nPruebas completadas.')
