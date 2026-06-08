import time
import random
from proyecto_final import (
    crear_matriz,
    calcular_A3,
    contar_repeticiones,
    frecuencias_a_json_ordenado,
    construir_arbol_json_equilibrado,
    buscar_y_contar_en_matriz,
    buscar_en_arbol_json,
)


def medir_accion(nombre, func, *args):
    t0 = time.perf_counter_ns()
    res = func(*args)
    t1 = time.perf_counter_ns()
    print(f"{nombre}: {t1-t0} ns")
    return res, t1 - t0


for n in (4, 8, 20, 21, 200):
    print("\n=== Prueba n=", n, "===")

    # Generar matriz
    A, t_gen = medir_accion("Generar matriz A", crear_matriz, n)

    # Calcular A3
    A3, t_a3 = medir_accion("Calcular A3", calcular_A3, A)

    # Contar frecuencias y ordenarlas como JSON
    rep_A, t_repA = medir_accion("Contar repeticiones A", contar_repeticiones, A)
    rep_A3, t_repA3 = medir_accion("Contar repeticiones A3", contar_repeticiones, A3)
    lista_A, t_jsonA = medir_accion("Crear lista JSON A", frecuencias_a_json_ordenado, rep_A)
    lista_A3, t_jsonA3 = medir_accion("Crear lista JSON A3", frecuencias_a_json_ordenado, rep_A3)

    # Construir arbol JSON equilibrado
    t0 = time.perf_counter_ns()
    arbolA = construir_arbol_json_equilibrado(lista_A, 0, len(lista_A)-1)
    t1 = time.perf_counter_ns()
    t_buildA = t1 - t0
    print(f"Construir arbol JSON A: {t_buildA} ns")

    t0 = time.perf_counter_ns()
    arbolA3 = construir_arbol_json_equilibrado(lista_A3, 0, len(lista_A3)-1)
    t1 = time.perf_counter_ns()
    t_buildA3 = t1 - t0
    print(f"Construir arbol JSON A3: {t_buildA3} ns")

    # Seleccionar un valor a buscar (toma uno existente si es posible)
    buscado = 0
    if len(A) > 0 and len(A[0]) > 0:
        fila_azar = random.randint(0, len(A) - 1)
        columna_azar = random.randint(0, len(A[fila_azar]) - 1)
        buscado = A[fila_azar][columna_azar]

    print(f"Valor a buscar: {buscado}")

    # Buscar en matriz y árbol
    _, t_bus_mat = medir_accion("Buscar en matriz A", buscar_y_contar_en_matriz, A, buscado)
    _, t_bus_ar = medir_accion("Buscar en arbol JSON A", buscar_en_arbol_json, arbolA, buscado)

    _, t_bus_mat3 = medir_accion("Buscar en matriz A3", buscar_y_contar_en_matriz, A3, buscado)
    _, t_bus_ar3 = medir_accion("Buscar en arbol JSON A3", buscar_en_arbol_json, arbolA3, buscado)

    print("Resumen tiempos (ns): gen, A3, rep, json, buildA, buildA3, b_mat, b_ar, b_mat3, b_ar3")
    print(t_gen, t_a3, t_repA, t_jsonA, t_buildA, t_buildA3, t_bus_mat, t_bus_ar, t_bus_mat3, t_bus_ar3)

print('\nPruebas completadas.')
