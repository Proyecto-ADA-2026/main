# ===============================================================================
# LOGICA DEL PROYECTO - ALGORITMOS Y ESTRUCTURAS DE DATOS
# ===============================================================================
# Este archivo contiene los algoritmos necesarios para el analisis de matrices,
# conteo de frecuencias, ordenamientos y construccion/busqueda en arboles BST.
# ===============================================================================

import random
import time
import tracemalloc


def unir_con_delimitador(lista, delimitador):
    """Une una lista de elementos en un solo string usando un delimitador manual."""
    resultado = ""
    for i in range(len(lista)):
        resultado += str(lista[i])
        if i < len(lista) - 1:
            resultado += delimitador
    return resultado


def crear_matriz(n):
    """Genera una matriz de tamaño n x n con valores aleatorios entre 0 y 9 sin usar .append()."""
    matriz = []
    for _ in range(n):
        fila = []
        for _ in range(n):
            valor = random.randint(0, 9)
            fila = fila + [valor]
        matriz = matriz + [fila]
    return matriz


def guardar_matriz_directo_txt(n, nombre_archivo="matriz.txt"):
    """Genera una matriz fila por fila y la escribe en un archivo TXT sin guardarla completa en memoria."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("Matriz generada de tamaño " + str(n) + " x " + str(n) + "\n")
        linea_separadora = ""
        for _ in range(60):
            linea_separadora += "="
        archivo.write(linea_separadora + "\n\n")
        for i in range(n):
            fila = []
            for j in range(n):
                valor = random.randint(0, 9)
                fila = fila + [str(valor)]
            linea_texto = ""
            for k in range(len(fila)):
                formateado = ""
                num_str = fila[k]
                espacios = 10 - len(num_str)
                formateado += num_str
                for _ in range(espacios):
                    formateado += " "
                linea_texto += formateado
                if k < len(fila) - 1:
                   linea_texto += "   "
            archivo.write(linea_texto + "\n")
            if i % 100 == 0:
                print("Generando fila " + str(i) + " de " + str(n) + "...")
    print("Matriz guardada correctamente en " + str(nombre_archivo))


def multiplicar_matrices(x, y):
    """Realiza la multiplicacion de dos matrices n x n sin usar librerias externas ni .append()."""
    n = len(x)
    y_transpuesta = []
    for j in range(n):
        columna = []
        for i in range(n):
            columna = columna + [y[i][j]]
        y_transpuesta = y_transpuesta + [columna]
    resultado = []
    for i in range(n):
        fila_resultado = []
        for j in range(n):
            columna_y = y_transpuesta[j]
            suma = 0
            for k in range(n):
                suma += x[i][k] * columna_y[k]
            fila_resultado = fila_resultado + [suma]
        resultado = resultado + [fila_resultado]
    return resultado


def guardar_A3_directo_txt(matriz_A, nombre_archivo="matriz_A3.txt"):
    """Calcula A3 = A * A * A y escribe el resultado directo en TXT fila por fila sin .append() ni .join()."""
    n = len(matriz_A)
    A2 = multiplicar_matrices(matriz_A, matriz_A)
    A3 = multiplicar_matrices(A2, matriz_A)
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("Matriz A³ de tamaño " + str(n) + " x " + str(n) + "\n")
        linea_separadora = ""
        for _ in range(60):
            linea_separadora += "="
        archivo.write(linea_separadora + "\n\n")
        for i in range(len(A3)):
            fila = A3[i]
            linea_texto = ""
            for k in range(len(fila)):
                num_str = str(fila[k])
                espacios = 10 - len(num_str)
                formateado = num_str
                for _ in range(espacios):
                    formateado += " "
                linea_texto += formateado
                if k < len(fila) - 1:
                    linea_texto += "   "
            archivo.write(linea_texto + "\n")
            if i % 100 == 0:
                print("Guardando fila " + str(i) + " de " + str(n) + "...")
    print("Matriz A³ guardada correctamente en " + str(nombre_archivo))
    return A3


def calcular_A3(A):
    """Calcula la potencia de la matriz A al cubo (A3 = A2 * A)."""
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)
    return A3


def estimar_memoria_matriz(n):
    """Realiza una estimacion teorica del tamaño en bytes que ocupa la matriz A en memoria."""
    return n * n * 28


def iniciar_medicion_memoria():
    """Inicia el rastreo de uso de memoria utilizando el modulo tracemalloc."""
    tracemalloc.start()


def obtener_memoria_actual_y_pico():
    """Retorna el uso de memoria RAM actual y el pico maximo alcanzado durante el rastreo."""
    actual, pico = tracemalloc.get_traced_memory()
    return actual, pico


def detener_medicion_memoria():
    """Detiene el rastreador de memoria de tracemalloc y libera recursos."""
    tracemalloc.stop()


def es_primo(numero):
    """Determina si un numero entero es primo utilizando un bucle basico."""
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def es_perfecto(numero):
    """Determina si un numero entero es perfecto (la suma de sus divisores propios es igual a el)."""
    if numero <= 1:
        return False
    suma_divisores = 1
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            suma_divisores += divisor
            otro_divisor = numero // divisor
            if otro_divisor != divisor:
                suma_divisores += otro_divisor
        divisor += 1
    return suma_divisores == numero


def es_cuadrado_perfecto(numero):
    """Comprueba si un numero es un cuadrado perfecto mediante una busqueda binaria simple."""
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
    """Analiza y clasifica todos los elementos de una matriz sin usar .append()."""
    pares = []
    impares = []
    primos = []
    perfectos = []
    cuadrados = []
    cache = {}
    for i in range(len(matriz)):
        fila = matriz[i]
        for j in range(len(fila)):
            valor = fila[j]
            if valor in cache:
                datos = cache[valor]
            else:
                datos = {
                    "par": valor % 2 == 0,
                    "primo": es_primo(valor),
                    "perfecto": es_perfecto(valor),
                    "cuadrado": es_cuadrado_perfecto(valor)
                }
                cache[valor] = datos
            if datos["par"]:
                pares = pares + [valor]
            else:
                impares = impares + [valor]
            if datos["primo"]:
                primos = primos + [valor]
            if datos["perfecto"]:
                perfectos = perfectos + [valor]
            if datos["cuadrado"]:
                cuadrados = cuadrados + [valor]
    return {
        "pares": {"cantidad": len(pares), "valores": pares},
        "impares": {"cantidad": len(impares), "valores": impares},
        "primos": {"cantidad": len(primos), "valores": primos},
        "perfectos": {"cantidad": len(perfectos), "valores": perfectos},
        "cuadrados": {"cantidad": len(cuadrados), "valores": cuadrados}
    }


def contar_repeticiones(matriz):
    """Cuenta cuantas veces aparece cada valor en la matriz, guardandolo en un diccionario."""
    frecuencias = {}
    for i in range(len(matriz)):
        fila = matriz[i]
        for j in range(len(fila)):
            valor = fila[j]
            if valor in frecuencias:
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1
    return frecuencias


def buscar_y_contar_en_matriz(matriz, buscado):
    """Realiza una busqueda secuencial en la matriz para determinar si existe y cuantas veces se repite."""
    encontrado = False
    cantidad = 0
    for i in range(len(matriz)):
        fila = matriz[i]
        for j in range(len(fila)):
            valor = fila[j]
            if valor == buscado:
                encontrado = True
                cantidad += 1
    return encontrado, cantidad


def frecuencias_a_json_ordenado(frecuencias):
    """Convierte el diccionario de frecuencias en una lista ordenada por valor sin usar .append()."""
    claves = []
    for clave in frecuencias:
        claves = claves + [clave]
    claves_ordenadas = ordenar_ascendente(claves)
    lista_json = []
    for i in range(len(claves_ordenadas)):
        clave = claves_ordenadas[i]
        dato = {
            "valor": clave,
            "cantidad": frecuencias[clave]
        }
        lista_json = lista_json + [dato]
    return lista_json


def frecuencias_a_tuplas_ordenadas(frecuencias):
    """Convierte el diccionario de frecuencias en una lista de tuplas ordenada sin usar .append()."""
    claves = []
    for clave in frecuencias:
        claves = claves + [clave]
    claves_ordenadas = ordenar_ascendente(claves)
    tuplas = []
    for i in range(len(claves_ordenadas)):
        clave = claves_ordenadas[i]
        tuplas = tuplas + [(clave, frecuencias[clave])]
    return tuplas


def matriz_a_vector(matriz):
    """Aplana una matriz n x n en un vector unidimensional sin usar .append()."""
    vector = []
    for i in range(len(matriz)):
        fila = matriz[i]
        for j in range(len(fila)):
            vector = vector + [fila[j]]
    return vector


def insertion_sort_ascendente(vector):
    """Ordena un vector de menor a mayor usando el algoritmo de ordenamiento por insercion."""
    for i in range(1, len(vector)):
        actual = vector[i]
        j = i - 1
        while j >= 0 and vector[j] > actual:
            vector[j + 1] = vector[j]
            j -= 1
        vector[j + 1] = actual
    return vector


def invertir_vector(vector):
    """Invierte el orden de un vector sin usar metodos incorporados ni .append()."""
    invertido = []
    for i in range(len(vector) - 1, -1, -1):
        invertido = invertido + [vector[i]]
    return invertido


def merge_sort_ascendente(vector):
    """Ordena un vector usando division y conquista (Merge Sort) sin usar .append()."""
    if len(vector) <= 1:
        return vector
    medio = len(vector) // 2
    izquierda = merge_sort_ascendente(vector[:medio])
    derecha = merge_sort_ascendente(vector[medio:])
    resultado = []
    i = 0
    j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado = resultado + [izquierda[i]]
            i += 1
        else:
            resultado = resultado + [derecha[j]]
            j += 1
    while i < len(izquierda):
        resultado = resultado + [izquierda[i]]
        i += 1
    while j < len(derecha):
        resultado = resultado + [derecha[j]]
        j += 1
    return resultado


def ordenar_ascendente(vector):
    """Elige el mejor algoritmo de ordenamiento segun el tamano de los datos."""
    if len(vector) <= 64:
        return insertion_sort_ascendente(vector)
    return merge_sort_ascendente(vector)


# ===============================================================================
# CLASES DE NODOS PARA ARBOLES BINARIOS DE BUSQUEDA
# ===============================================================================

class NodoJSON:
    """Clase que representa un nodo con estructura compatible con formato JSON."""

    def __init__(self, valor, cantidad):
        self.dato = {
            "valor": valor,
            "cantidad": cantidad
        }
        self.izquierda = None
        self.derecha = None


class NodoFrecuencia:
    """Clase que representa un nodo en formato de tupla simple."""

    def __init__(self, valor, cantidad):
        self.dato = (valor, cantidad)
        self.izquierda = None
        self.derecha = None


class Nodo:
    """Clase que representa un nodo basico que guarda un unico valor."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


# ===============================================================================
# ALGORITMOS DE CONSTRUCCION DE ARBOLES EQUILIBRADOS (BST)
# ===============================================================================


def construir_arbol_json_equilibrado(lista_json, inicio, fin):
    """Construye un arbol binario equilibrado desde una lista JSON ordenada."""
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
    """Construye un arbol equilibrado utilizando tuplas ordenadas de valores y frecuencias."""
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
    """Construye un BST equilibrado basico a partir de un vector plano de enteros ordenados."""
    if inicio > fin:
        return None
    mitad = (inicio + fin) // 2
    raiz = Nodo(vector[mitad])
    raiz.izquierda = construir_arbol_equilibrado(vector, inicio, mitad - 1)
    raiz.derecha = construir_arbol_equilibrado(vector, mitad + 1, fin)
    return raiz


# ===============================================================================
# ALGORITMOS DE BUSQUEDA Y OPERACIONES EN ARBOLES
# ===============================================================================


def buscar_en_arbol(raiz, buscado):
    """Busca un valor de forma binaria en un arbol binario basico."""
    if raiz is None:
        return False
    if hasattr(raiz, 'valor'):
        valor_nodo = raiz.valor
    else:
        valor_nodo = raiz.dato[0]
    if buscado == valor_nodo:
        return True
    if buscado < valor_nodo:
        return buscar_en_arbol(raiz.izquierda, buscado)
    return buscar_en_arbol(raiz.derecha, buscado)


def buscar_en_arbol_json(raiz, buscado):
    """Busca un numero de forma binaria en un arbol de estructura compatible JSON."""
    if raiz is None:
        return None
    valor_nodo = raiz.dato["valor"]
    if buscado == valor_nodo:
        return raiz.dato
    if buscado < valor_nodo:
        return buscar_en_arbol_json(raiz.izquierda, buscado)
    return buscar_en_arbol_json(raiz.derecha, buscado)


def contar_nodos_arbol_json(raiz):
    """Cuenta todos los nodos del arbol JSON recursivamente."""
    if raiz is None:
        return 0
    return 1 + contar_nodos_arbol_json(raiz.izquierda) + contar_nodos_arbol_json(raiz.derecha)


def altura_arbol_json(raiz):
    """Calcula la altura maxima del arbol compatible JSON."""
    if raiz is None:
        return 0
    altura_izquierda = altura_arbol_json(raiz.izquierda)
    altura_derecha = altura_arbol_json(raiz.derecha)
    if altura_izquierda > altura_derecha:
        return altura_izquierda + 1
    return altura_derecha + 1


def recorrido_inorden_json(raiz):
    """Retorna una lista con la estructura de recorrido inorden sin usar .append()."""
    if raiz is None:
        return []
    izq = recorrido_inorden_json(raiz.izquierda)
    der = recorrido_inorden_json(raiz.derecha)
    return izq + [raiz.dato] + der


def buscar_en_arbol_frecuencias(raiz, buscado):
    """Busca binariamente en un arbol construido con nodos de tuplas de frecuencia."""
    if raiz is None:
        return None
    valor_nodo = raiz.dato[0]
    if buscado == valor_nodo:
        return raiz.dato
    if buscado < valor_nodo:
        return buscar_en_arbol_frecuencias(raiz.izquierda, buscado)
    return buscar_en_arbol_frecuencias(raiz.derecha, buscado)


def contar_nodos_arbol_frecuencias(raiz):
    """Cuenta el numero total de nodos de frecuencias."""
    if raiz is None:
        return 0
    return 1 + contar_nodos_arbol_frecuencias(raiz.izquierda) + contar_nodos_arbol_frecuencias(raiz.derecha)


def altura_arbol(raiz):
    """Calcula la altura maxima de un arbol binario basico."""
    if raiz is None:
        return 0
    altura_izq = altura_arbol(raiz.izquierda)
    altura_der = altura_arbol(raiz.derecha)
    if altura_izq >= altura_der:
        return 1 + altura_izq
    return 1 + altura_der


def recorrido_inorden_frecuencias(raiz):
    """Retorna una lista plana de recorrido inorden sin usar .append() ni .extend()."""
    if raiz is None:
        return []
    izq = recorrido_inorden_frecuencias(raiz.izquierda)
    der = recorrido_inorden_frecuencias(raiz.derecha)
    return izq + [raiz.dato] + der


def buscar_en_matriz(matriz, buscado):
    """Busca de forma directa si un valor entero existe dentro de la matriz."""
    for i in range(len(matriz)):
        fila = matriz[i]
        for j in range(len(fila)):
            if fila[j] == buscado:
                return True
    return False


def medir_tiempo(funcion, estructura, buscado):
    """Mide el tiempo transcurrido en nanosegundos al ejecutar una busqueda."""
    inicio = time.perf_counter_ns()
    encontrado = funcion(estructura, buscado)
    fin = time.perf_counter_ns()
    return encontrado, fin - inicio


# ===============================================================================
# DIBUJO DEL ARBOL EN TEXTO (REPRESENTACION ASCII Y DOT DE GRAPHVIZ)
# ===============================================================================


def arbol_a_ascii(raiz):
    """Genera un dibujo ASCII del arbol binario con ramas visuales sin .append() ni .join()."""
    if raiz is None:
        return "Árbol vacío"

    def display_aux(nodo):
        if nodo.izquierda is None and nodo.derecha is None:
            if hasattr(nodo, 'dato'):
                linea = str(nodo.dato["valor"])
            else:
                linea = str(nodo.valor)
            ancho = len(linea)
            alto = 1
            centro = ancho // 2
            return [linea], ancho, alto, centro

        if nodo.derecha is None:
            lineas, ancho, alto, centro = display_aux(nodo.izquierda)
            if hasattr(nodo, 'dato'):
                valor = str(nodo.dato["valor"])
            else:
                valor = str(nodo.valor)
            ancho_valor = len(valor)
            primera = ""
            for _ in range(centro + 1):
                primera += " "
            for _ in range(ancho - centro - 1):
                primera += "_"
            primera += valor
            segunda = ""
            for _ in range(centro):
                segunda += " "
            segunda += "/"
            for _ in range(ancho - centro - 1 + ancho_valor):
                segunda += " "
            lineas_movidas = []
            for idx in range(len(lineas)):
                linea_aux = lineas[idx]
                relleno = ""
                for _ in range(ancho_valor):
                    relleno += " "
                lineas_movidas = lineas_movidas + [linea_aux + relleno]
            return [primera, segunda] + lineas_movidas, ancho + ancho_valor, alto + 2, ancho_valor // 2

        if nodo.izquierda is None:
            lineas, ancho, alto, centro = display_aux(nodo.derecha)
            if hasattr(nodo, 'dato'):
                valor = str(nodo.dato["valor"])
            else:
                valor = str(nodo.valor)
            ancho_valor = len(valor)
            primera = valor
            for _ in range(centro):
                primera += "_"
            for _ in range(ancho - centro):
                primera += " "
            segunda = ""
            for _ in range(ancho_valor + centro):
                segunda += " "
            segunda += "\\"
            for _ in range(ancho - centro - 1):
                segunda += " "
            lineas_movidas = []
            for idx in range(len(lineas)):
                linea_aux = lineas[idx]
                relleno = ""
                for _ in range(ancho_valor):
                    relleno += " "
                lineas_movidas = lineas_movidas + [relleno + linea_aux]
            return [primera, segunda] + lineas_movidas, ancho + ancho_valor, alto + 2, ancho_valor // 2

        izquierda, ancho_izq, alto_izq, centro_izq = display_aux(nodo.izquierda)
        derecha, ancho_der, alto_der, centro_der = display_aux(nodo.derecha)
        if hasattr(nodo, 'dato'):
            valor = str(nodo.dato["valor"])
        else:
            valor = str(nodo.valor)
        ancho_valor = len(valor)
        primera = ""
        for _ in range(centro_izq + 1):
            primera += " "
        for _ in range(ancho_izq - centro_izq - 1):
            primera += "_"
        primera += valor
        for _ in range(centro_der):
            primera += "_"
        for _ in range(ancho_der - centro_der):
            primera += " "
        segunda = ""
        for _ in range(centro_izq):
            segunda += " "
        segunda += "/"
        for _ in range(ancho_izq - centro_izq - 1 + ancho_valor + centro_der):
            segunda += " "
        segunda += "\\"
        for _ in range(ancho_der - centro_der - 1):
            segunda += " "
        if alto_izq < alto_der:
            diferencia = alto_der - alto_izq
            for _ in range(diferencia):
                relleno_izq = ""
                for _ in range(ancho_izq):
                    relleno_izq += " "
                izquierda = izquierda + [relleno_izq]
        elif alto_der < alto_izq:
            diferencia = alto_izq - alto_der
            for _ in range(diferencia):
                relleno_der = ""
                for _ in range(ancho_der):
                    relleno_der += " "
                derecha = derecha + [relleno_der]
        lineas = [primera, segunda]
        for idx in range(len(izquierda)):
            linea_izq = izquierda[idx]
            linea_der = derecha[idx]
            relleno_central = ""
            for _ in range(ancho_valor):
                relleno_central += " "
            lineas = lineas + [linea_izq + relleno_central + linea_der]
        return lineas, ancho_izq + ancho_valor + ancho_der, max(alto_izq, alto_der) + 2, ancho_izq + ancho_valor // 2

    lineas, _, _, _ = display_aux(raiz)
    if not lineas:
        return "Árbol vacío"
    ancho_maximo = 0
    for i in range(len(lineas)):
        l = len(lineas[i])
        if l > ancho_maximo:
            ancho_maximo = l
    lineas_centradas = []
    for i in range(len(lineas)):
        linea = lineas[i]
        ancho_actual = len(linea)
        faltante = (ancho_maximo + 8) - ancho_actual
        mitad_izq = faltante // 2
        mitad_der = faltante - mitad_izq
        espacio_izq = ""
        for _ in range(mitad_izq):
            espacio_izq += " "
        espacio_der = ""
        for _ in range(mitad_der):
            espacio_der += " "
        linea_centrada = espacio_izq + linea + espacio_der
        lineas_centradas = lineas_centradas + [linea_centrada]
    return unir_con_delimitador(lineas_centradas, "\n")


def exportar_arbol_dot(raiz, nombre_grafo="Arbol"):
    """Exporta el arbol a formato DOT de Graphviz para renderizar grafos, sin usar .append() ni .join()."""
    lineas = []
    lineas = lineas + ["digraph " + str(nombre_grafo) + " {"]
    lineas = lineas + ["    node [shape=circle];"]
    contador = [0]

    def recorrer(nodo):
        nonlocal lineas
        if nodo is None:
            return None
        id_actual = contador[0]
        contador[0] += 1
        if hasattr(nodo, 'dato'):
            if isinstance(nodo.dato, dict):
                label = str(nodo.dato['valor']) + " | cant: " + str(nodo.dato['cantidad'])
            else:
                label = str(nodo.dato[0]) + " | cant: " + str(nodo.dato[1])
        else:
            label = str(nodo.valor)
        lineas = lineas + ["    nodo" + str(id_actual) + " [label=\"" + label + "\"];"]
        id_izq = recorrer(nodo.izquierda)
        if id_izq is not None:
            lineas = lineas + ["    nodo" + str(id_actual) + " -> nodo" + str(id_izq) + ";"]
        id_der = recorrer(nodo.derecha)
        if id_der is not None:
            lineas = lineas + ["    nodo" + str(id_actual) + " -> nodo" + str(id_der) + ";"]
        return id_actual

    recorrer(raiz)
    lineas = lineas + ["}"]
    return unir_con_delimitador(lineas, "\n")
