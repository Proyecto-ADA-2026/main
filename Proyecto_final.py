"""
proyecto_final.py
Lógica algorítmica / backend del proyecto (sin GUI).
Contiene todos los algoritmos y estructuras de datos del taller.
"""

import random
import sys
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


def guardar_matriz_directo_txt(n, nombre_archivo="matriz.txt"):
    """Genera una matriz fila por fila y la escribe en un archivo TXT sin guardarla completa en memoria."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo: # Abre el archivo en modo escritura con codificación UTF-8.
        archivo.write("Matriz generada de tamaño " + str(n) + " x " + str(n) + "\n") # Escribe el encabezado con el tamaño.
        linea_separadora = ""                                  # Inicializa un string vacío para la línea divisoria.
        for _ in range(60):                                    # Itera 60 veces para construir la línea de caracteres.
            linea_separadora += "="                            # Concatena un carácter '=' en cada ciclo.
        archivo.write(linea_separadora + "\n\n")               # Escribe la línea divisoria seguida de dos saltos de línea.
        for i in range(n):                                     # Itera n veces para generar cada una de las filas.
            fila = []                                          # Inicializa la fila de texto como lista vacía.
            for j in range(n):                                 # Itera n veces para rellenar las columnas de la fila actual.
                valor = random.randint(0, 9)                   # Genera un número entero aleatorio entre 0 y 9.
                fila = fila + [str(valor)]                     # Agrega el valor en formato texto a la lista de la fila.
            linea_texto = ""                                   # Inicializa el string que representará la línea de la fila.
            for k in range(len(fila)):                         # Recorre cada elemento de la fila.
                formateado = ""                                # Inicializa el texto formateado.
                num_str = fila[k]                              # Obtiene el string numérico.
                espacios = 10 - len(num_str)                   # Calcula los espacios necesarios para un ancho fijo de 10.
                formateado += num_str                          # Agrega el número al formateado.
                for _ in range(espacios):                      # Agrega los espacios calculados uno por uno.
                    formateado += " "                          # Agrega un espacio en blanco.
                linea_texto += formateado                      # Concatena el elemento formateado a la línea.
                if k < len(fila) - 1:                          # Si no es el último elemento, añade separación adicional.
                   linea_texto += "   "                        # Agrega tres espacios como separador de columna.
            archivo.write(linea_texto + "\n")                  # Escribe la línea formateada en el archivo.
            if i % 100 == 0:                                   # Mide si la fila actual es múltiplo de 100 para dar feedback.
                print("Generando fila " + str(i) + " de " + str(n) + "...") # Muestra en consola el progreso de la generación.
    print("Matriz guardada correctamente en " + str(nombre_archivo)) # Imprime mensaje final en consola al finalizar.


def multiplicar_matrices(x, y):
    """Realiza la multiplicación de dos matrices n x n sin usar librerías externas ni .append()."""
    n = len(x)                                                 # Obtiene la dimensión n de las matrices cuadradas.
    y_transpuesta = []                                         # Inicializa la matriz transpuesta de y como lista vacía.
    for j in range(n):                                         # Itera por cada columna de la matriz y.
        columna = []                                           # Inicializa una lista vacía para almacenar la columna.
        for i in range(n):                                     # Itera por cada fila de la matriz y.
            columna = columna + [y[i][j]]                      # Agrega el elemento de la columna a la lista por concatenación.
        y_transpuesta = y_transpuesta + [columna]              # Agrega la columna transpuesta a la matriz de transpuestas.
    resultado = []                                             # Inicializa la matriz de resultados como lista vacía.
    for i in range(n):                                         # Itera por cada fila de la matriz x.
        fila_resultado = []                                    # Inicializa la fila del resultado de la iteración actual.
        for j in range(n):                                     # Itera por cada columna transpuesta de y (que ahora son filas).
            columna_y = y_transpuesta[j]                       # Obtiene la columna transpuesta correspondiente.
            suma = 0                                           # Inicializa el acumulador de la multiplicación elemento a elemento.
            for k in range(n):                                 # Itera por los elementos de la fila y la columna.
                suma += x[i][k] * columna_y[k]                 # Multiplica los elementos y acumula el resultado en suma.
            fila_resultado = fila_resultado + [suma]           # Agrega la suma acumulada a la fila resultado.
        resultado = resultado + [fila_resultado]               # Agrega la fila completada a la matriz resultado final.
    return resultado                                           # Retorna la matriz de resultados de la multiplicación.


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


def frecuencias_a_tuplas_ordenadas(frecuencias):
    claves = []
    for clave in frecuencias:
        claves.append(clave)

    claves_ordenadas = ordenar_ascendente(list(claves))

    tuplas = []
    for clave in claves_ordenadas:
        tuplas.append((clave, frecuencias[clave]))

    return tuplas


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
        self.dato = {                                          # Inicializa el diccionario de datos del nodo.
            "valor": valor,                                    # Clave 'valor' guarda el identificador del nodo.
            "cantidad": cantidad                               # Clave 'cantidad' guarda la frecuencia del valor.
        }                                                      # Cierra el diccionario de inicialización.
        self.izquierda = None                                  # Puntero al subárbol izquierdo (menores).
        self.derecha = None                                    # Puntero al subárbol derecho (mayores).


class NodoFrecuencia:
    def __init__(self, valor, cantidad):
        self.dato = (valor, cantidad)                          # Guarda la tupla (valor, cantidad).
        self.izquierda = None                                  # Puntero izquierdo inicializado en None.
        self.derecha = None                                    # Puntero derecho inicializado en None.


class Nodo:
    def __init__(self, valor):
        self.valor = valor                                     # Asigna el valor del nodo.
        self.izquierda = None                                  # Puntero al hijo izquierdo.
        self.derecha = None                                    # Puntero al hijo derecho.


# ==============================================================================
# ALGORITMOS DE CONSTRUCCIÓN DE ÁRBOLES EQUILIBRADOS (BST)
# ==============================================================================

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


def construir_arbol_frecuencias_equilibrado(tuplas, inicio, fin):
    if inicio > fin:
        return None

    mitad = (inicio + fin) // 2
    valor = tuplas[mitad][0]
    cantidad = tuplas[mitad][1]

    raiz = NodoFrecuencia(valor, cantidad)
    raiz.izquierda = construir_arbol_frecuencias_equilibrado(tuplas, inicio, mitad - 1)
    raiz.derecha = construir_arbol_frecuencias_equilibrado(tuplas, mitad + 1, fin)
    return raiz


def construir_arbol_equilibrado(vector, inicio, fin):
    # Construye un árbol binario de búsqueda equilibrado a partir de un vector ordenado.
    # Primero se ordena el vector de elementos.
    # Luego se toma el elemento central como raíz.
    # La mitad izquierda forma el subárbol izquierdo.
    # La mitad derecha forma el subárbol derecho.
    # Este proceso se repite recursivamente para cada subvector.
    # De esta forma se evita que el árbol quede como una cadena lineal.
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

    valor_nodo = raiz.valor if hasattr(raiz, 'valor') else raiz.dato[0]

    if buscado == valor_nodo:
        return True
    if buscado < valor_nodo:
        return buscar_en_arbol(raiz.izquierda, buscado)
    return buscar_en_arbol(raiz.derecha, buscado)


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


def buscar_en_arbol_frecuencias(raiz, buscado):
    if raiz is None:
        return None

    valor_nodo = raiz.dato[0]
    if buscado == valor_nodo:
        return raiz.dato
    if buscado < valor_nodo:
        return buscar_en_arbol_frecuencias(raiz.izquierda, buscado)
    return buscar_en_arbol_frecuencias(raiz.derecha, buscado)


def contar_nodos_arbol_frecuencias(raiz):
    if raiz is None:
        return 0
    return 1 + contar_nodos_arbol_frecuencias(raiz.izquierda) + contar_nodos_arbol_frecuencias(raiz.derecha)


def altura_arbol(raiz):
    if raiz is None:
        return 0
    altura_izq = altura_arbol(raiz.izquierda)
    altura_der = altura_arbol(raiz.derecha)
    return 1 + (altura_izq if altura_izq >= altura_der else altura_der)


def recorrido_inorden_frecuencias(raiz):
    resultado = []
    if raiz is not None:
        resultado.extend(recorrido_inorden_frecuencias(raiz.izquierda))
        resultado.append(raiz.dato)
        resultado.extend(recorrido_inorden_frecuencias(raiz.derecha))
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
# DIBUJO DEL ÁRBOL EN TEXTO (REPRESENTACIÓN ASCII Y DOT DE GRAPHVIZ)
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


def arbol_json_a_diccionario(raiz):
    """
    Convierte el árbol JSON equilibrado en un diccionario anidado.

    Cada nodo se representa con la estructura:
        {
            "valor": número,
            "cantidad": frecuencia,
            "izquierda": subárbol izquierdo,
            "derecha": subárbol derecho
        }

    Si el nodo es None, retorna None.

    Relación con el proyecto:
        Permite exportar el árbol en formato JSON sin depender de Graphviz.

    Costo:
        O(u), donde u es la cantidad de valores únicos del árbol.
    """
    if raiz is None:
        return None

    return {
        "valor": raiz.dato["valor"],
        "cantidad": raiz.dato["cantidad"],
        "izquierda": arbol_json_a_diccionario(raiz.izquierda),
        "derecha": arbol_json_a_diccionario(raiz.derecha)
    }


def arbol_a_json_texto(raiz):
    """
    Convierte el árbol JSON equilibrado a texto JSON con formato legible.

    Retorna:
        Una cadena en formato JSON lista para guardarse en un archivo .json.

    Nota:
        La librería json es estándar de Python y solo se usa para exportar
        la estructura; no construye el árbol ni realiza búsquedas.
    """
    diccionario = arbol_json_a_diccionario(raiz)
    return json.dumps(diccionario, indent=4, ensure_ascii=False)



