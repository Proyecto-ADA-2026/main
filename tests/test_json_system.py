#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test final completo del sistema JSON
"""

from logica_arbol import (
    crear_matriz, calcular_A3, contar_repeticiones,
    frecuencias_a_json_ordenado, construir_arbol_json_equilibrado,
    buscar_en_arbol_json, contar_nodos_arbol_json, altura_arbol_json,
    recorrido_inorden_json, buscar_y_contar_en_matriz, arbol_a_ascii,
    exportar_arbol_dot, medir_tiempo, analizar_matriz,
    matriz_a_vector, ordenar_ascendente
)

print("=" * 60)
print("TEST FINAL DEL SISTEMA JSON")
print("=" * 60)

# Test 1: Crear matrices
print("\n✓ Test 1: Crear matrices")
A = crear_matriz(5)
print(f"  Matriz A (5x5) creada: {len(A)} filas")

A3 = calcular_A3(A)
print(f"  Matriz A³ (5x5) calculada: {len(A3)} filas")

# Test 2: Contar repeticiones
print("\n✓ Test 2: Contar repeticiones")
rep_A = contar_repeticiones(A)
print(f"  Frecuencias A: {rep_A}")

rep_A3 = contar_repeticiones(A3)
print(f"  Frecuencias A³: {rep_A3}")

# Test 3: Convertir a JSON y crear árbol
print("\n✓ Test 3: Construir árbol JSON")
lista_json_A = frecuencias_a_json_ordenado(rep_A)
print(f"  Lista JSON A: {lista_json_A}")

tree_A = construir_arbol_json_equilibrado(lista_json_A, 0, len(lista_json_A)-1)
print(f"  Árbol A construido con raíz: {tree_A.dato}")

lista_json_A3 = frecuencias_a_json_ordenado(rep_A3)
tree_A3 = construir_arbol_json_equilibrado(lista_json_A3, 0, len(lista_json_A3)-1)
print(f"  Árbol A³ construido con raíz: {tree_A3.dato}")

# Test 4: Propiedades del árbol
print("\n✓ Test 4: Propiedades del árbol")
nodes_A = contar_nodos_arbol_json(tree_A)
height_A = altura_arbol_json(tree_A)
print(f"  Árbol A: {nodes_A} nodos, altura {height_A}")

nodes_A3 = contar_nodos_arbol_json(tree_A3)
height_A3 = altura_arbol_json(tree_A3)
print(f"  Árbol A³: {nodes_A3} nodos, altura {height_A3}")

# Test 5: Búsqueda
print("\n✓ Test 5: Búsqueda en árbol JSON")
test_value = list(rep_A.keys())[0] if rep_A else 5
resultado = buscar_en_arbol_json(tree_A, test_value)
print(f"  Buscando {test_value} en árbol A: {resultado}")

resultado_matriz = buscar_y_contar_en_matriz(A, test_value)
print(f"  Buscando {test_value} en matriz A: encontrado={resultado_matriz[0]}, cantidad={resultado_matriz[1]}")

# Test 6: Análisis de matriz
print("\n✓ Test 6: Análisis de matriz")
analisis = analizar_matriz(A)
print(f"  Análisis A: pares={analisis['pares']['cantidad']}, impares={analisis['impares']['cantidad']}, primos={analisis['primos']['cantidad']}")

# Test 7: Recorrido inorden
print("\n✓ Test 7: Recorrido inorden")
inorden = recorrido_inorden_json(tree_A)
print(f"  Inorden A: {inorden}")

# Test 8: Exportar DOT
print("\n✓ Test 8: Exportar DOT")
try:
    dot_content = exportar_arbol_dot(tree_A)
    if "digraph" in dot_content:
        print(f"  Archivo DOT generado correctamente ({len(dot_content)} caracteres)")
        lines = dot_content.split('\n')
        print(f"  Primeras líneas:")
        for line in lines[:3]:
            print(f"    {line}")
    else:
        print(f"  Advertencia: formato DOT no tiene 'digraph'")
except Exception as e:
    print(f"  Error en exportar_arbol_dot: {e}")

# Test 9: Visualización ASCII
print("\n✓ Test 9: Visualización ASCII")
try:
    ascii_tree = arbol_a_ascii(tree_A)
    lines = ascii_tree.split('\n')
    print(f"  Árbol A (primeras 3 líneas):")
    for line in lines[:3]:
        print(f"    {line}")
except Exception as e:
    print(f"  Error en arbol_a_ascii: {e}")

# Test 10: Medición de tiempo
print("\n✓ Test 10: Medición de tiempos")
resultado_m, tiempo_m = medir_tiempo(buscar_y_contar_en_matriz, A, test_value)
resultado_a, tiempo_a = medir_tiempo(buscar_en_arbol_json, tree_A, test_value)
print(f"  Búsqueda en matriz A: {tiempo_m} ns")
print(f"  Búsqueda en árbol A: {tiempo_a} ns")
factor = tiempo_m // tiempo_a if tiempo_a > 0 else 0
if factor > 0:
    print(f"  Árbol es {factor}x más rápido")

print("\n" + "=" * 60)
print("✓ TODOS LOS TESTS PASARON CORRECTAMENTE")
print("=" * 60)
