"""
proyecto_final.py
Lógica algorítmica / backend del proyecto (sin GUI).
Contiene todos los algoritmos y estructuras de datos del taller.
"""

import random
import time


# =========================================================
# LÓGICA / ALGORITMOS
# =========================================================


def crear_matriz(n):
    matriz = []
    for _ in range(n):
        fila = []
        for _ in range(n):
            # Cada elemento es un número aleatorio entre 0 y 9
            fila.append(random.randint(0, 9))
        matriz.append(fila)
    return matriz


def multiplicar_matrices(x, y):
    """Multiplicación de matrices sin librerías externas.
    Optimiza el acceso recordando las columnas de y.
    """
    n = len(x)

    # Transponer y para leer columnas como filas y mejorar el acceso en el bucle.
    y_transpuesta = []
    for j in range(n):
        columna = []
        for i in range(n):
            columna.append(y[i][j])
        y_transpuesta.append(columna)

    resultado = []
    for i in range(n):
        fila_resultado = []
        for columna_y in y_transpuesta:
            suma = 0
            for a, b in zip(x[i], columna_y):
                suma += a * b
            fila_resultado.append(suma)
        resultado.append(fila_resultado)

    return resultado


def calcular_A3(A):
    # A² = A * A, luego A³ = A² * A
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)
    return A3


def es_primo(numero):
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        # Si es divisible por cualquier divisor menor que sqrt(numero), no es primo
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def es_perfecto(numero):
    # Optimizado: solo recorremos divisores hasta la raíz cuadrada
    if numero <= 1:
        return False

    suma_divisores = 1
    divisor = 2

    while divisor * divisor <= numero:
        if numero % divisor == 0:
            suma_divisores += divisor

            otro_divisor = numero // divisor
            if otro_divisor != divisor:
                # Sumar el divisor complementario si no es el mismo
                suma_divisores += otro_divisor

        divisor += 1

    return suma_divisores == numero


def es_cuadrado_perfecto(numero):
    # Optimizado con búsqueda binaria sobre el rango de posibles raíces
    if numero < 0:
        return False

    if numero == 0 or numero == 1:
        return True

    izquierda = 1
    derecha = numero

    while izquierda <= derecha:
        mitad = (izquierda + derecha) // 2
        cuadrado = mitad * mitad

        if cuadrado == numero:
            return True

        if cuadrado < numero:
            izquierda = mitad + 1
        else:
            derecha = mitad - 1

    return False


def analizar_matriz(matriz):
    pares = []
    impares = []
    primos = []
    perfectos = []
    cuadrados = []

    cache = {}

    def analizar_valor(valor, cache):
        if valor in cache:
            return cache[valor]

        # Calcular propiedades una sola vez por valor repetido
        resultado = {
            "par": valor % 2 == 0,
            "primo": es_primo(valor),
            "perfecto": es_perfecto(valor),
            "cuadrado": es_cuadrado_perfecto(valor),
        }

        cache[valor] = resultado
        return resultado

    for fila in matriz:
        for valor in fila:
            datos = analizar_valor(valor, cache)

            if datos["par"]:
                pares.append(valor)
            else:
                impares.append(valor)

            if datos["primo"]:
                primos.append(valor)

            if datos["perfecto"]:
                perfectos.append(valor)

            if datos["cuadrado"]:
                cuadrados.append(valor)

    return {
        "pares": {"cantidad": len(pares), "valores": pares},
        "impares": {"cantidad": len(impares), "valores": impares},
        "primos": {"cantidad": len(primos), "valores": primos},
        "perfectos": {"cantidad": len(perfectos), "valores": perfectos},
        "cuadrados": {"cantidad": len(cuadrados), "valores": cuadrados},
    }


def contar_repeticiones(matriz):
    frecuencias = {}
    for fila in matriz:
        for valor in fila:
            # Incrementar el conteo para cada aparición
            frecuencias[valor] = frecuencias.get(valor, 0) + 1
    return frecuencias


def matriz_a_vector(matriz):
    vector = []
    for fila in matriz:
        for valor in fila:
            # Aplanar la matriz en un vector fila a fila
            vector.append(valor)
    return vector


def insertion_sort_ascendente(vector):
    for i in range(1, len(vector)):
        actual = vector[i]
        j = i - 1
        while j >= 0 and vector[j] > actual:
            vector[j + 1] = vector[j]
            j -= 1
        vector[j + 1] = actual
    return vector


def merge_sort_ascendente(vector):
    if len(vector) <= 1:
        return vector

    medio = len(vector) // 2
    izquierda = merge_sort_ascendente(vector[:medio])
    derecha = merge_sort_ascendente(vector[medio:])

    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


def ordenar_ascendente(vector):
    # Elegir inserción para vectores pequeños y merge sort para los grandes
    if len(vector) <= 64:
        return insertion_sort_ascendente(vector)
    return merge_sort_ascendente(vector)


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


def construir_arbol_equilibrado(vector, inicio, fin):
    if inicio > fin:
        return None

    mitad = (inicio + fin) // 2
    raiz = Nodo(vector[mitad])
    raiz.izquierda = construir_arbol_equilibrado(vector, inicio, mitad - 1)
    raiz.derecha = construir_arbol_equilibrado(vector, mitad + 1, fin)
    return raiz


def buscar_en_arbol(raiz, buscado):
    if raiz is None:
        return False
    if buscado == raiz.valor:
        return True
    if buscado < raiz.valor:
        return buscar_en_arbol(raiz.izquierda, buscado)
    return buscar_en_arbol(raiz.derecha, buscado)


def buscar_en_matriz(matriz, buscado):
    for fila in matriz:
        for valor in fila:
            if valor == buscado:
                return True
    return False


def medir_tiempo(funcion, estructura, buscado):
    # Mide el tiempo en nanosegundos que tarda la búsqueda
    inicio = time.perf_counter_ns()
    encontrado = funcion(estructura, buscado)
    fin = time.perf_counter_ns()
    return encontrado, fin - inicio


# =========================================================
# DIBUJO DEL ÁRBOL EN TEXTO
# =========================================================


def arbol_a_ascii(raiz):
    # Convierte un árbol en una representación ASCII legible
    if raiz is None:
        return "Árbol vacío"

    def display_aux(nodo):
        if nodo.izquierda is None and nodo.derecha is None:
            linea = str(nodo.valor)
            ancho = len(linea)
            alto = 1
            centro = ancho // 2
            return [linea], ancho, alto, centro

        if nodo.derecha is None:
            lineas, ancho, alto, centro = display_aux(nodo.izquierda)
            valor = str(nodo.valor)
            ancho_valor = len(valor)

            primera = (
                " " * (centro + 1)
                + "_" * (ancho - centro - 1)
                + valor
            )

            segunda = (
                " " * centro
                + "/"
                + " " * (ancho - centro - 1 + ancho_valor)
            )

            lineas_movidas = [linea + " " * ancho_valor for linea in lineas]

            return (
                [primera, segunda] + lineas_movidas,
                ancho + ancho_valor,
                alto + 2,
                ancho_valor // 2
            )

        if nodo.izquierda is None:
            lineas, ancho, alto, centro = display_aux(nodo.derecha)
            valor = str(nodo.valor)
            ancho_valor = len(valor)

            primera = (
                valor
                + "_" * centro
                + " " * (ancho - centro)
            )

            segunda = (
                " " * (ancho_valor + centro)
                + "\\"
                + " " * (ancho - centro - 1)
            )

            lineas_movidas = [" " * ancho_valor + linea for linea in lineas]

            return (
                [primera, segunda] + lineas_movidas,
                ancho + ancho_valor,
                alto + 2,
                ancho_valor // 2
            )

        izquierda, ancho_izq, alto_izq, centro_izq = display_aux(nodo.izquierda)
        derecha, ancho_der, alto_der, centro_der = display_aux(nodo.derecha)

        valor = str(nodo.valor)
        ancho_valor = len(valor)

        primera = (
            " " * (centro_izq + 1)
            + "_" * (ancho_izq - centro_izq - 1)
            + valor
            + "_" * centro_der
            + " " * (ancho_der - centro_der)
        )

        segunda = (
            " " * centro_izq
            + "/"
            + " " * (ancho_izq - centro_izq - 1 + ancho_valor + centro_der)
            + "\\"
            + " " * (ancho_der - centro_der - 1)
        )

        if alto_izq < alto_der:
            izquierda += [" " * ancho_izq] * (alto_der - alto_izq)
        elif alto_der < alto_izq:
            derecha += [" " * ancho_der] * (alto_izq - alto_der)

        lineas = [primera, segunda]
        for linea_izq, linea_der in zip(izquierda, derecha):
            lineas.append(linea_izq + " " * ancho_valor + linea_der)

        return (
            lineas,
            ancho_izq + ancho_valor + ancho_der,
            max(alto_izq, alto_der) + 2,
            ancho_izq + ancho_valor // 2
        )

    lineas, _, _, _ = display_aux(raiz)
    if not lineas:
        return "Árbol vacío"

    ancho_maximo = max(len(linea) for linea in lineas)
    lineas_centradas = []
    for linea in lineas:
        lineas_centradas.append(linea.center(ancho_maximo + 8))
    return "\n".join(lineas_centradas)
