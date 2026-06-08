#!/usr/bin/env python3
"""
Script de prueba para validar que los árboles se exportan como JSON correctamente
sin Graphviz.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from proyecto_final import (
    crear_matriz,
    calcular_A3,
    analizar_matriz,
    contar_repeticiones,
    frecuencias_a_json_ordenado,
    construir_arbol_json_equilibrado,
)
from gestor_txt import arbol_a_json_texto

def test_json_export():
    """Prueba la generación y exportación de árboles en JSON."""
    
    print("=" * 60)
    print("PRUEBA: Generación y Exportación JSON de Árboles")
    print("=" * 60)
    
    n = 4
    print(f"\n1. Generando matriz A de tamaño {n}x{n}...")
    A = crear_matriz(n)
    print("   ✓ Matriz A generada")
    
    print(f"\n2. Calculando A³...")
    A3 = calcular_A3(A)
    print("   ✓ A³ calculada")
    
    print(f"\n3. Analizando matrices...")
    analisis_A = analizar_matriz(A)
    analisis_A3 = analizar_matriz(A3)
    print("   ✓ Análisis completado")
    
    print(f"\n4. Contando repeticiones...")
    rep_A = contar_repeticiones(A)
    rep_A3 = contar_repeticiones(A3)
    print("   ✓ Repeticiones contadas")
    
    print(f"\n5. Generando listas JSON...")
    lista_json_A = frecuencias_a_json_ordenado(rep_A)
    lista_json_A3 = frecuencias_a_json_ordenado(rep_A3)
    print(f"   ✓ Lista A: {len(lista_json_A)} elementos únicos")
    print(f"   ✓ Lista A³: {len(lista_json_A3)} elementos únicos")
    
    print(f"\n6. Construyendo árboles equilibrados...")
    arbol_A = construir_arbol_json_equilibrado(lista_json_A, 0, len(lista_json_A) - 1)
    arbol_A3 = construir_arbol_json_equilibrado(lista_json_A3, 0, len(lista_json_A3) - 1)
    print("   ✓ Árboles construidos")
    
    print(f"\n7. Exportando árboles a JSON...")
    json_A = arbol_a_json_texto(arbol_A)
    json_A3 = arbol_a_json_texto(arbol_A3)
    print("   ✓ Árboles convertidos a JSON")
    
    print(f"\n8. Guardando archivos JSON...")
    resultados_dir = ROOT / "resultados"
    resultados_dir.mkdir(exist_ok=True)
    with open(resultados_dir / "arbol_A.json", "w", encoding="utf-8") as f:
        f.write(json_A)
    with open(resultados_dir / "arbol_A3.json", "w", encoding="utf-8") as f:
        f.write(json_A3)
    print("   ✓ resultados/arbol_A.json guardado")
    print("   ✓ resultados/arbol_A3.json guardado")
    
    print(f"\n9. Verificando que NO se generaron archivos .dot o .png...")
    dot_exists = os.path.exists(str(ROOT / "resultados" / "arbol_A.dot"))
    png_exists = os.path.exists(str(ROOT / "resultados" / "arbol_A.png"))
    if not dot_exists and not png_exists:
        print("   ✓ Correcto: No se generaron .dot ni .png")
    else:
        print("   ✗ ERROR: Se encontraron archivos .dot o .png")
        return False
    
    print(f"\n10. Mostrando fragmentos de JSON generado...")
    print("\n   --- arbol_A.json (primeros 200 caracteres) ---")
    print("   " + json_A[:200].replace("\n", "\n   "))
    print("\n   --- arbol_A3.json (primeros 200 caracteres) ---")
    print("   " + json_A3[:200].replace("\n", "\n   "))
    
    print("\n" + "=" * 60)
    print("✓ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_json_export()
    sys.exit(0 if success else 1)
