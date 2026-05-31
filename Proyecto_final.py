"""
proyecto_final.py
Lógica algorítmica / backend del proyecto (sin GUI).
Contiene todos los algoritmos y estructuras de datos del taller.
"""

import random
import time
import tracemalloc
import json


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


def guardar_A3_directo_txt(matriz_A, nombre_archivo="matriz_A3.txt"):
    """Calcula A³ = A² × A y guarda el resultado directamente en TXT.
    
    Recibe matriz_A en memoria, calcula A³, y lo guarda fila por fila.
    Útil para matrices grandes.
    """
    n = len(matriz_A)
    
    # Calcular A² = A × A
    A2 = multiplicar_matrices(matriz_A, matriz_A)
    
    # Calcular A³ = A² × A
    A3 = multiplicar_matrices(A2, matriz_A)
    
    # Guardar A³ fila por fila
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"Matriz A³ de tamaño {n} x {n}\n")
        archivo.write("=" * 60 + "\n\n")
        
        for i, fila in enumerate(A3):
            archivo.write("   ".join(f"{v:10}" for v in fila) + "\n")
            
            # Mostrar progreso cada 100 filas
            if i % 100 == 0:
                print(f"Guardando fila {i} de {n}...")
    
    print(f"Matriz A³ guardada correctamente en {nombre_archivo}")
    return A3


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
            for k in range(n):
                suma += x[i][k] * columna_y[k]
            fila_resultado.append(suma)
        resultado.append(fila_resultado)

    return resultado


def calcular_A3(A):
    # A² = A * A, luego A³ = A² * A
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)
    return A3


def estimar_memoria_matriz(n):
    # Estimación aproximada de memoria usada por la matriz A.
    # Se usa 28 bytes por entero como valor de referencia simple para Python,
    # sin contar la sobrecarga completa de listas y objetos adicionales.
    return n * n * 28


def iniciar_medicion_memoria():
    tracemalloc.start()


def obtener_memoria_actual_y_pico():
    actual, pico = tracemalloc.get_traced_memory()
    return actual, pico


def detener_medicion_memoria():
    tracemalloc.stop()


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
            if valor in frecuencias:
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1
    return frecuencias


def buscar_y_contar_en_matriz(matriz, buscado):
    encontrado = False
    cantidad = 0
    for fila in matriz:
        for valor in fila:
            if valor == buscado:
                encontrado = True
                cantidad += 1
    return encontrado, cantidad

def frecuencias_a_json_ordenado(frecuencias):
    claves = []
    for clave in frecuencias:
        claves.append(clave)

    claves_ordenadas = ordenar_ascendente(list(claves))

    lista_json = []
    for clave in claves_ordenadas:
        dato = {
            "valor": clave,
            "cantidad": frecuencias[clave]
        }
        lista_json.append(dato)

    return lista_json


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


def invertir_vector(vector):
    invertido = []
    for i in range(len(vector) - 1, -1, -1):
        invertido.append(vector[i])
    return invertido


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

    while i < len(izquierda):
        resultado.append(izquierda[i])
        i += 1

    while j < len(derecha):
        resultado.append(derecha[j])
        j += 1
    return resultado


def ordenar_ascendente(vector):
    # Elegir inserción para vectores pequeños y merge sort para los grandes
    if len(vector) <= 64:
        return insertion_sort_ascendente(vector)
    return merge_sort_ascendente(vector)


class NodoJSON:
    def __init__(self, valor, cantidad):
        self.dato = {
            "valor": valor,
            "cantidad": cantidad,
        }
        self.izquierda = None
        self.derecha = None


# ======================================================================
# ALGORITMOS DE CONSTRUCCIÓN DE ÁRBOLES EQUILIBRADOS (JSON BST)
# ======================================================================

def construir_arbol_json_equilibrado(lista_json, inicio, fin):
    # Construye un árbol binario de búsqueda equilibrado desde una lista JSON ordenada.
    # La lista JSON ya está ordenada por valor.
    # Se toma el elemento central como raíz.
    # La mitad izquierda forma el subárbol izquierdo.
    # La mitad derecha forma el subárbol derecho.
    # Este proceso se repite recursivamente.
    # Así el árbol queda equilibrado o lo más equilibrado posible.
    if inicio > fin:
        return None

    mitad = (inicio + fin) // 2
    valor = lista_json[mitad]["valor"]
    cantidad = lista_json[mitad]["cantidad"]

    raiz = NodoJSON(valor, cantidad)
    raiz.izquierda = construir_arbol_json_equilibrado(lista_json, inicio, mitad - 1)
    raiz.derecha = construir_arbol_json_equilibrado(lista_json, mitad + 1, fin)

    return raiz


def buscar_en_arbol_json(raiz, buscado):
    if raiz is None:
        return None

    valor_nodo = raiz.dato["valor"]
    if buscado == valor_nodo:
        return raiz.dato
    if buscado < valor_nodo:
        return buscar_en_arbol_json(raiz.izquierda, buscado)
    return buscar_en_arbol_json(raiz.derecha, buscado)


def contar_nodos_arbol_json(raiz):
    if raiz is None:
        return 0
    return 1 + contar_nodos_arbol_json(raiz.izquierda) + contar_nodos_arbol_json(raiz.derecha)


def altura_arbol_json(raiz):
    if raiz is None:
        return 0

    altura_izquierda = altura_arbol_json(raiz.izquierda)
    altura_derecha = altura_arbol_json(raiz.derecha)

    if altura_izquierda > altura_derecha:
        return altura_izquierda + 1

    return altura_derecha + 1


def recorrido_inorden_json(raiz):
    resultado = []

    def recorrer(nodo):
        if nodo is not None:
            recorrer(nodo.izquierda)
            resultado.append(nodo.dato)
            recorrer(nodo.derecha)

    recorrer(raiz)
    return resultado


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


# ==============================================================================
# DIBUJO DEL ÁRBOL EN TEXTO (REPRESENTACIÓN ASCII)
# ==============================================================================

def arbol_a_ascii(raiz):
    # Convierte un árbol en una representación ASCII legible
    if raiz is None:
        return "Árbol vacío"

    def display_aux(nodo):
        if nodo.izquierda is None and nodo.derecha is None:
            linea = str(nodo.dato if hasattr(nodo, 'dato') else nodo.valor)
            ancho = len(linea)
            alto = 1
            centro = ancho // 2
            return [linea], ancho, alto, centro

        if nodo.derecha is None:
            lineas, ancho, alto, centro = display_aux(nodo.izquierda)
            valor = str(nodo.dato if hasattr(nodo, 'dato') else nodo.valor)
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
            valor = str(nodo.dato if hasattr(nodo, 'dato') else nodo.valor)
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

        valor = str(nodo.dato if hasattr(nodo, 'dato') else nodo.valor)
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

    lineas, _, _, _ = display_aux(raiz)                        # Llama a la función recursiva.
    if not lineas:                                             # Si no devolvió líneas.
        return "Árbol vacío"                                   # Retorna texto indicando vacío.
    ancho_maximo = 0                                           # Inicializa el ancho máximo de línea en 0.
    for i in range(len(lineas)):                               # Itera sobre todas las líneas.
        l = len(lineas[i])                                     # Mide la longitud de la línea actual.
        if l > ancho_maximo:                                   # Si es mayor que el máximo actual.
            ancho_maximo = l                                   # Actualiza el ancho máximo.
    lineas_centradas = []                                      # Prepara la lista de líneas que serán centradas.
    for i in range(len(lineas)):                               # Recorre cada línea.
        linea = lineas[i]                                      # Obtiene la línea actual.
        ancho_actual = len(linea)                              # Mide su longitud.
        faltante = (ancho_maximo + 8) - ancho_actual           # Calcula el espacio faltante para centrar con margen de 8.
        mitad_izq = faltante // 2                              # Espacios para el lado izquierdo.
        mitad_der = faltante - mitad_izq                       # Espacios para el lado derecho.
        espacio_izq = ""                                       # Prepara texto izquierdo.
        for _ in range(mitad_izq):                             # Genera los espacios izquierdos.
            espacio_izq += " "                                 # Agrega espacio.
        espacio_der = ""                                       # Prepara texto derecho.
        for _ in range(mitad_der):                             # Genera los espacios derechos.
            espacio_der += " "                                 # Agrega espacio.
        linea_centrada = espacio_izq + linea + espacio_der     # Arma la línea final centrada.
        lineas_centradas = lineas_centradas + [linea_centrada] # Agrega a la lista final de líneas centradas sin .append().
    return "\n".join(lineas_centradas)                          # Une las líneas usando saltos de línea.


def arbol_json_a_lista(raiz):
    """
    Convierte el árbol binario de búsqueda equilibrado a una lista JSON plana.

    Cada nodo se representa como:
    {
        "id": identificador del nodo,
        "valor": valor almacenado,
        "cantidad": frecuencia del valor,
        "izquierda": id del hijo izquierdo o None,
        "derecha": id del hijo derecho o None
    }

    Esta representación permite ver la estructura del árbol sin Graphviz.
    """
    nodos = []
    contador = [0]

    def recorrer(nodo):
        if nodo is None:
            return None

        id_actual = contador[0]
        contador[0] += 1

        registro = {
            "id": id_actual,
            "valor": nodo.dato["valor"],
            "cantidad": nodo.dato["cantidad"],
            "izquierda": None,
            "derecha": None,
        }

        nodos.append(registro)

        id_izquierda = recorrer(nodo.izquierda)
        id_derecha = recorrer(nodo.derecha)

        registro["izquierda"] = id_izquierda
        registro["derecha"] = id_derecha

        return id_actual

    recorrer(raiz)
    return nodos


def arbol_a_json_texto(raiz):
    """
    Convierte el árbol a texto JSON plano por nodos.
    """
    lista_nodos = arbol_json_a_lista(raiz)
    return json.dumps(lista_nodos, indent=4, ensure_ascii=False)



