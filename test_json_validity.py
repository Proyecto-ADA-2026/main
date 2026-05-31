import json

try:
    with open("resultados/arbol_A.json") as f:
        arbol_A = json.load(f)
    print("✓ arbol_A.json es JSON válido")
    print(f"  - Raíz: valor={arbol_A['valor']}, cantidad={arbol_A['cantidad']}")
    print(f"  - Estructura: izquierda={'sí' if arbol_A['izquierda'] else 'no'}, derecha={'sí' if arbol_A['derecha'] else 'no'}")
except Exception as e:
    print(f"✗ Error en arbol_A.json: {e}")

try:
    with open("resultados/arbol_A3.json") as f:
        arbol_A3 = json.load(f)
    print("✓ arbol_A3.json es JSON válido")
    print(f"  - Raíz: valor={arbol_A3['valor']}, cantidad={arbol_A3['cantidad']}")
    print(f"  - Estructura: izquierda={'sí' if arbol_A3['izquierda'] else 'no'}, derecha={'sí' if arbol_A3['derecha'] else 'no'}")
except Exception as e:
    print(f"✗ Error en arbol_A3.json: {e}")
