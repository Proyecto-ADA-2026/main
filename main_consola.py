"""Ejecucion alternativa por consola del Proyecto Final ADA.

Esta version no abre ventanas, no mide memoria y no guarda archivos externos.
Todos los resultados se muestran directamente en la terminal.
"""

from proyecto_final import (
    MAX_N,
    crear_matriz,
    multiplicar_matrices,
    analizar_matriz,
    contar_repeticiones,
    frecuencias_a_json_ordenado,
    matriz_a_vector,
    ordenar_ascendente,
    invertir_vector,
    construir_arbol_json_equilibrado,
    buscar_y_contar_en_matriz,
    buscar_en_arbol_json,
    medir_tiempo_promedio,
    arbol_a_ascii,
    contar_nodos_arbol_json,
    altura_arbol_json,
    contar_elementos_representados_arbol,
)


def imprimir_titulo(titulo):
    """Imprime un titulo de seccion en consola."""
    print("\n" + titulo)
    print("=" * len(titulo))


def matriz_a_texto(matriz):
    """Convierte una matriz a texto alineado."""
    texto = ""
    for i in range(len(matriz)):
        fila = matriz[i]
        linea = ""
        for j in range(len(fila)):
            linea += f"{fila[j]:8}"
            if j < len(fila) - 1:
                linea += " "
        texto += linea
        if i < len(matriz) - 1:
            texto += "\n"
    return texto


def lista_a_texto(lista, max_mostrar=80):
    """Convierte una lista a texto y limita la salida si es muy larga."""
    texto = "["
    limite = len(lista)
    recortada = False

    if limite > max_mostrar:
        limite = max_mostrar
        recortada = True

    for i in range(limite):
        texto += str(lista[i])
        if i < limite - 1:
            texto += ", "

    if recortada:
        texto += " ... +" + str(len(lista) - max_mostrar) + " elementos"
    texto += "]"
    return texto


def leer_entero(mensaje):
    """Lee un entero desde la consola."""
    while True:
        texto = input(mensaje)
        try:
            return int(texto)
        except ValueError:
            print("Ingrese un numero entero valido.")


def leer_n():
    """Lee y valida el tamano de la matriz."""
    while True:
        n = leer_entero("Ingrese el tamano n de la matriz (n >= 4): ")
        if n < 4:
            print("Error: n debe ser mayor o igual a 4.")
        elif n > MAX_N:
            print(
                "Error: n supera el limite de " + str(MAX_N) +
                ". Calcular A3 requiere dos multiplicaciones de matrices."
            )
        else:
            return n


def imprimir_analisis(nombre, analisis):
    """Muestra el analisis numerico de una matriz."""
    imprimir_titulo("ANALISIS " + nombre)
    print("Pares              :", analisis["pares"]["cantidad"])
    print("Impares            :", analisis["impares"]["cantidad"])
    print("Primos             :", analisis["primos"]["cantidad"])
    print("Perfectos          :", analisis["perfectos"]["cantidad"])
    print("Cuadrados perfectos:", analisis["cuadrados"]["cantidad"])


def imprimir_repeticiones(nombre, repeticiones):
    """Muestra las frecuencias ordenadas por valor."""
    claves = []
    for clave in repeticiones:
        claves = claves + [clave]
    claves = ordenar_ascendente(claves)

    imprimir_titulo("REPETICIONES " + nombre)
    for i in range(len(claves)):
        clave = claves[i]
        print(str(clave) + ": " + str(repeticiones[clave]))


def construir_arbol_desde_repeticiones(repeticiones):
    """Construye una lista JSON ordenada y un arbol equilibrado."""
    lista_json = frecuencias_a_json_ordenado(repeticiones)
    arbol = construir_arbol_json_equilibrado(lista_json, 0, len(lista_json) - 1)
    return lista_json, arbol


def imprimir_arbol(nombre, arbol, cantidad_nodos):
    """Muestra datos del arbol y su version ASCII si es manejable."""
    imprimir_titulo("ARBOL " + nombre)
    print("Nodos del arbol        :", contar_nodos_arbol_json(arbol))
    print("Altura                 :", altura_arbol_json(arbol))
    print("Elementos representados:", contar_elementos_representados_arbol(arbol))

    if cantidad_nodos <= 63:
        print(arbol_a_ascii(arbol))
    else:
        print("Arbol generado. No se imprime completo porque tiene muchos nodos.")


def imprimir_vectores(A, A3):
    """Muestra vectores ordenados de A y A3."""
    vec_A = matriz_a_vector(A)
    vec_A3 = matriz_a_vector(A3)
    vec_A_asc = ordenar_ascendente(vec_A)
    vec_A3_asc = ordenar_ascendente(vec_A3)
    vec_A_desc = invertir_vector(vec_A_asc)
    vec_A3_desc = invertir_vector(vec_A3_asc)

    imprimir_titulo("VECTORES ORDENADOS")
    print("A ascendente :", lista_a_texto(vec_A_asc))
    print("A descendente:", lista_a_texto(vec_A_desc))
    print("A3 ascendente :", lista_a_texto(vec_A3_asc))
    print("A3 descendente:", lista_a_texto(vec_A3_desc))


def ejecutar_busqueda(A, A3, arbol_A, arbol_A3):
    """Permite comparar busqueda en matriz contra busqueda en arbol."""
    imprimir_titulo("BUSQUEDA COMPARATIVA")
    buscado = leer_entero("Ingrese el numero que desea buscar: ")
    repeticiones = 1000

    res_mat_A, t_mat_A = medir_tiempo_promedio(
        buscar_y_contar_en_matriz, A, buscado, repeticiones
    )
    res_arb_A, t_arb_A = medir_tiempo_promedio(
        buscar_en_arbol_json, arbol_A, buscado, repeticiones
    )
    res_mat_A3, t_mat_A3 = medir_tiempo_promedio(
        buscar_y_contar_en_matriz, A3, buscado, repeticiones
    )
    res_arb_A3, t_arb_A3 = medir_tiempo_promedio(
        buscar_en_arbol_json, arbol_A3, buscado, repeticiones
    )

    print("\nMatriz A")
    print("En matriz:", res_mat_A[0], "| cantidad:", res_mat_A[1], "| tiempo:", t_mat_A, "ns")
    if res_arb_A is None:
        print("En arbol : False | cantidad: 0 | tiempo:", t_arb_A, "ns")
    else:
        print("En arbol : True | cantidad:", res_arb_A["cantidad"], "| tiempo:", t_arb_A, "ns")

    print("\nMatriz A3")
    print("En matriz:", res_mat_A3[0], "| cantidad:", res_mat_A3[1], "| tiempo:", t_mat_A3, "ns")
    if res_arb_A3 is None:
        print("En arbol : False | cantidad: 0 | tiempo:", t_arb_A3, "ns")
    else:
        print("En arbol : True | cantidad:", res_arb_A3["cantidad"], "| tiempo:", t_arb_A3, "ns")


def main():
    """Punto de entrada de la version por consola."""
    imprimir_titulo("PROYECTO FINAL ADA - VERSION CONSOLA")
    print("Esta version no abre interfaz grafica, no mide memoria y no guarda archivos.")

    n = leer_n()

    imprimir_titulo("GENERACION Y POTENCIAS DE MATRIZ")
    A = crear_matriz(n)
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)

    imprimir_titulo("MATRIZ A")
    print(matriz_a_texto(A))
    imprimir_titulo("MATRIZ A2")
    print(matriz_a_texto(A2))
    imprimir_titulo("MATRIZ A3")
    print(matriz_a_texto(A3))

    imprimir_analisis("MATRIZ A", analizar_matriz(A))
    imprimir_analisis("MATRIZ A3", analizar_matriz(A3))

    rep_A = contar_repeticiones(A)
    rep_A3 = contar_repeticiones(A3)
    imprimir_repeticiones("MATRIZ A", rep_A)
    imprimir_repeticiones("MATRIZ A3", rep_A3)

    imprimir_vectores(A, A3)

    lista_A, arbol_A = construir_arbol_desde_repeticiones(rep_A)
    lista_A3, arbol_A3 = construir_arbol_desde_repeticiones(rep_A3)
    imprimir_arbol("A", arbol_A, len(lista_A))
    imprimir_arbol("A3", arbol_A3, len(lista_A3))

    ejecutar_busqueda(A, A3, arbol_A, arbol_A3)

    imprimir_titulo("FIN")
    print("Ejecucion finalizada correctamente.")


if __name__ == "__main__":
    main()
