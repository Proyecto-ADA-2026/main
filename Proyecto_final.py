"""
proyecto_final.py
Lógica algorítmica / backend del proyecto (sin GUI).
Contiene todos los algoritmos y estructuras de datos del taller.
"""

# random permite generar números aleatorios.
# En este proyecto se usa para llenar la matriz A con valores entre 0 y 9.
import random

# sys es una librería estándar útil para estimar tamaños de objetos en memoria si se requiere.
# No reemplaza ningún algoritmo; solo puede apoyar el análisis de memoria.
import sys

# time permite medir tiempos de ejecución.
# En este proyecto se usa para comparar la búsqueda en matriz y la búsqueda en árbol.
import time

# tracemalloc permite medir memoria actual y memoria pico usada por el programa.
# Sirve para justificar restricciones de tamaño y evitar que el sistema colapse.
import tracemalloc


# =========================================================
# LÓGICA / ALGORITMOS
# =========================================================


def crear_matriz(n):
    """
    Crea una matriz cuadrada de tamaño n x n con valores aleatorios entre 0 y 9.
    
    Entrada:
        n: Tamaño de la matriz (número de filas y columnas).
    
    Retorna:
        Una matriz representada como lista de listas, donde cada elemento es
        un número entero aleatorio en el rango [0, 9].
    
    Relación con el proyecto:
        Cumple el punto 1 del enunciado: construir una matriz n x n con valores
        aleatorios y realizar operaciones sobre ella.
    
    Costo:
        O(n²) - recorre n filas y n columnas para llenar cada posición.
    """
    matriz = []
    for _ in range(n):
        fila = []
        for _ in range(n):
            # Cada elemento es un número aleatorio entre 0 y 9
            fila.append(random.randint(0, 9))
        matriz.append(fila)
    return matriz


def guardar_matriz_directo_txt(n, nombre_archivo="matriz.txt"):
    """Genera una matriz n x n fila por fila y la guarda directamente en TXT.
    
    No guarda la matriz completa en memoria. Genera, guarda y descarta cada fila.
    Útil para matrices grandes (n > 100).
    """
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"Matriz generada de tamaño {n} x {n}\n")
        archivo.write("=" * 60 + "\n\n")
        
        for i in range(n):
            fila = []
            for j in range(n):
                valor = random.randint(0, 9)
                fila.append(str(valor))
            
            archivo.write("   ".join(f"{v:10}" for v in fila) + "\n")
            
            # Mostrar progreso cada 100 filas
            if i % 100 == 0:
                print(f"Generando fila {i} de {n}...")
    
    print(f"Matriz guardada correctamente en {nombre_archivo}")


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
    """
    Multiplica dos matrices cuadradas x e y sin usar librerías externas.
    
    Implementación manual que transpone y para optimizar el acceso a columnas,
    evitando búsquedas repetidas en la estructura de datos.
    
    Entrada:
        x: Primera matriz (lista de listas).
        y: Segunda matriz (lista de listas).
    
    Retorna:
        Matriz resultado de la multiplicación x × y.
    
    Relación con el proyecto:
        Utilizado para calcular A² y A³ requeridas en el proyecto.
    
    Costo:
        O(n³) - tres bucles anidados recorren todas las posiciones.
        Este es el cuello de botella del proyecto, justificando el límite MAX_N.
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
    """
    Calcula A³ mediante dos multiplicaciones de matrices: A² = A × A, A³ = A² × A.
    
    Entrada:
        A: Matriz cuadrada de tamaño n x n.
    
    Retorna:
        Matriz A³, donde A³[i][j] = suma de A²[i][k] × A[k][j] para todo k.
    
    Relación con el proyecto:
        Cumple el punto 1 del enunciado sobre calcular A³.
    
    Costo:
        O(n³) + O(n³) = O(n³) - dos multiplicaciones secuenciales.
    """
    # A² = A * A, luego A³ = A² * A
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)
    return A3


def estimar_memoria_matriz(n):
    """
    Estima de forma aproximada la memoria ocupada por una matriz n x n.
    
    Entrada:
    n: tamaño de la matriz.
    
    Retorna:
    Cantidad aproximada de bytes usados por los enteros de la matriz.
    
    Relación con el proyecto:
    Ayuda a justificar límites de tamaño para evitar consumo excesivo de RAM.
    
    Costo:
    O(1), porque solo realiza una operación aritmética.
    """
    # Estimación aproximada de memoria usada por la matriz A.
    # Se usa 28 bytes por entero como valor de referencia simple para Python,
    # sin contar la sobrecarga completa de listas y objetos adicionales.
    return n * n * 28


def iniciar_medicion_memoria():
    """
    Inicia la medición de memoria con tracemalloc.
    
    Entrada:
    No recibe parámetros.
    
    Retorna:
    No retorna valor.
    
    Relación con el proyecto:
    Permite medir memoria durante la generación, análisis y construcción del árbol.
    
    Costo:
    O(1).
    """
    tracemalloc.start()


def obtener_memoria_actual_y_pico():
    """
    Obtiene la memoria actual y la memoria pico registrada por tracemalloc.
    
    Entrada:
    No recibe parámetros.
    
    Retorna:
    Una tupla con memoria actual y memoria pico en bytes.
    
    Relación con el proyecto:
    Permite mostrar cuánta RAM se usa y cuál fue el máximo alcanzado.
    
    Costo:
    O(1).
    """
    actual, pico = tracemalloc.get_traced_memory()
    return actual, pico


def detener_medicion_memoria():
    """
    Detiene la medición de memoria iniciada con tracemalloc.
    
    Entrada:
    No recibe parámetros.
    
    Retorna:
    No retorna valor.
    
    Relación con el proyecto:
    Finaliza el monitoreo de memoria después de generar los resultados.
    
    Costo:
    O(1).
    """
    tracemalloc.stop()


def es_primo(numero):
    """
    Verifica si un número es primo iterando desde 2 hasta sqrt(número).
    
    Entrada:
        numero: Número entero a verificar.
    
    Retorna:
        True si el número es primo, False en caso contrario.
    
    Relación con el proyecto:
        Utilizado en analizar_matriz para contar números primos.
    
    Costo:
        O(√n) - itera hasta la raíz cuadrada del número.
    """
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
    """
    Verifica si un número es perfecto.
    
    Un número perfecto es igual a la suma de sus divisores propios.
    Por ejemplo, 6 es perfecto porque 1 + 2 + 3 = 6.
    
    Entrada:
    numero: entero que se desea verificar.
    
    Retorna:
    True si el número es perfecto, False en caso contrario.
    
    Relación con el proyecto:
    Cumple el punto 2.c del enunciado.
    
    Costo:
    O(√numero), porque revisa divisores hasta la raíz cuadrada.
    """
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
    """
    Verifica si un número es cuadrado perfecto usando búsqueda binaria.
    
    Entrada:
    numero: entero que se desea evaluar.
    
    Retorna:
    True si existe un entero k tal que k² = numero; False en caso contrario.
    
    Relación con el proyecto:
    Cumple el punto 2.d del enunciado.
    
    Costo:
    O(log numero), porque reduce el rango de búsqueda a la mitad.
    """
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
    """
    Analiza una matriz y clasifica sus elementos.
    
    Cuenta y almacena:
    - números pares,
    - números impares,
    - números primos,
    - números perfectos,
    - números cuadrados perfectos.
    
    Entrada:
    matriz: matriz que se desea analizar.
    
    Retorna:
    Diccionario con cantidades y valores encontrados para cada categoría.
    
    Relación con el proyecto:
    Cumple el punto 2 del enunciado para la matriz A y la matriz A³.
    
    Costo:
    Como mínimo O(n²), porque recorre todos los elementos.
    Además depende del costo de evaluar primo, perfecto y cuadrado perfecto.
    """
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
    """
    Cuenta cuántas veces aparece cada valor en la matriz.
    
    Entrada:
    matriz: matriz que se desea recorrer.
    
    Retorna:
    Diccionario donde la clave es el valor y el contenido es su frecuencia.
    
    Relación con el proyecto:
    Cumple el punto 4 del enunciado.
    
    Costo:
    O(n²), porque revisa todos los elementos de la matriz.
    """
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
    """
    Busca un número en la matriz y cuenta cuántas veces aparece.

    Entrada:
        matriz: matriz donde se realizará la búsqueda secuencial.
        buscado: número que se desea encontrar.

    Retorna:
        Tupla (encontrado, cantidad):
            encontrado es True si aparece el número,
            cantidad es cuántas veces aparece.

    Relación con el proyecto:
        Permite comparar la búsqueda secuencial en matriz contra la búsqueda
        en el árbol JSON equilibrado.

    Costo:
        O(n²), porque en el peor caso recorre todas las posiciones de la matriz.
    """
    encontrado = False
    cantidad = 0

    for fila in matriz:
        for valor in fila:
            if valor == buscado:
                encontrado = True
                cantidad += 1

    return encontrado, cantidad

def frecuencias_a_json_ordenado(frecuencias):
    """
    Convierte un diccionario de frecuencias en una lista de diccionarios tipo JSON ordenada.
    
    Cada elemento queda con la forma:
    {"valor": número, "cantidad": frecuencia}
    
    Entrada:
    frecuencias: diccionario generado por contar_repeticiones.
    
    Retorna:
    Lista de diccionarios ordenada ascendentemente por el campo valor.
    
    Relación con el proyecto:
    Prepara los datos para construir el árbol binario de búsqueda equilibrado con nodos JSON.
    
    Costo:
    Depende del ordenamiento aplicado sobre la cantidad de valores únicos.
    """
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
    """
    Convierte un diccionario de frecuencias en una lista de tuplas ordenadas.
    
    Entrada:
    frecuencias: diccionario con valor y cantidad.
    
    Retorna:
    Lista de tuplas (valor, cantidad) ordenadas por valor.
    
    Relación con el proyecto:
    Se conserva como alternativa, aunque la versión principal usa nodos JSON.
    
    Costo:
    Depende del ordenamiento sobre los valores únicos.
    """
    claves = []
    for clave in frecuencias:
        claves.append(clave)

    claves_ordenadas = ordenar_ascendente(list(claves))

    tuplas = []
    for clave in claves_ordenadas:
        tuplas.append((clave, frecuencias[clave]))

    return tuplas


def matriz_a_vector(matriz):
    """
    Convierte una matriz en un vector unidimensional.
    
    Entrada:
    matriz: matriz que se desea aplanar.
    
    Retorna:
    Lista con todos los elementos de la matriz en orden fila por fila.
    
    Relación con el proyecto:
    Cumple el punto 3 del enunciado antes de ordenar los elementos.
    
    Costo:
    O(n²), porque recorre todos los elementos.
    """
    vector = []
    for fila in matriz:
        for valor in fila:
            # Aplanar la matriz en un vector fila a fila
            vector.append(valor)
    return vector


def insertion_sort_ascendente(vector):
    """
    Ordena un vector de forma ascendente usando Insertion Sort.
    
    Entrada:
    vector: lista de números.
    
    Retorna:
    El vector ordenado ascendentemente.
    
    Relación con el proyecto:
    Cumple el punto 3 del enunciado sin usar sorted() ni list.sort().
    
    Costo:
    O(m²) en el peor caso, donde m es la cantidad de elementos del vector.
    """
    for i in range(1, len(vector)):
        actual = vector[i]
        j = i - 1
        while j >= 0 and vector[j] > actual:
            vector[j + 1] = vector[j]
            j -= 1
        vector[j + 1] = actual
    return vector


def invertir_vector(vector):
    """
    Invierte manualmente un vector para obtener orden descendente.
    
    Entrada:
    vector: lista previamente ordenada de forma ascendente.
    
    Retorna:
    Nueva lista con los elementos en orden contrario.
    
    Relación con el proyecto:
    Permite mostrar los elementos en forma descendente sin usar reverse() ni reversed().
    
    Costo:
    O(m), donde m es la cantidad de elementos del vector.
    """
    invertido = []
    for i in range(len(vector) - 1, -1, -1):
        invertido.append(vector[i])
    return invertido


def merge_sort_ascendente(vector):
    """
    Ordena un vector ascendentemente usando Merge Sort.
    
    Entrada:
    vector: lista de números.
    
    Retorna:
    Nueva lista ordenada de menor a mayor.
    
    Relación con el proyecto:
    Cumple el punto 3 usando un algoritmo propio basado en divide y vencerás.
    
    Costo:
    O(m log m), donde m es la cantidad de elementos del vector.
    """
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
    """
    Selecciona el algoritmo de ordenamiento según el tamaño del vector.
    
    Entrada:
    vector: lista de números.
    
    Retorna:
    Vector ordenado ascendentemente.
    
    Relación con el proyecto:
    Evita usar sorted() o list.sort() y mantiene el análisis algorítmico propio.
    
    Costo:
    O(m²) para vectores pequeños con Insertion Sort.
    O(m log m) para vectores grandes con Merge Sort.
    """
    # Elegir inserción para vectores pequeños y merge sort para los grandes
    if len(vector) <= 64:
        return insertion_sort_ascendente(vector)
    return merge_sort_ascendente(vector)


class NodoJSON:
    """
    Representa un nodo del Árbol Binario de Búsqueda Equilibrado con estructura JSON.
    
    Cada nodo almacena:
    dato["valor"]: número presente en la matriz.
    dato["cantidad"]: cantidad de veces que aparece ese número.
    
    Los enlaces izquierda y derecha mantienen la propiedad:
    valores menores van a la izquierda,
    valores mayores van a la derecha.
    """
    def __init__(self, valor, cantidad):
        self.dato = {
            "valor": valor,
            "cantidad": cantidad
        }
        self.izquierda = None
        self.derecha = None


class NodoFrecuencia:
    """
    Representa un nodo alternativo que almacena una tupla (valor, cantidad).
    
    Esta clase se conserva como apoyo, aunque la versión principal del proyecto usa NodoJSON.
    """
    def __init__(self, valor, cantidad):
        self.dato = (valor, cantidad)
        self.izquierda = None
        self.derecha = None


class Nodo:
    """
    Representa un nodo simple de árbol binario.
    
    Guarda únicamente un valor y referencias a los hijos izquierdo y derecho.
    Se conserva para compatibilidad con funciones generales del proyecto.
    """
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


def construir_arbol_json_equilibrado(lista_json, inicio, fin):
    """
    Construye un Árbol Binario de Búsqueda Equilibrado con nodos tipo JSON.
    
    Entrada:
    lista_json: lista ordenada de diccionarios {"valor": x, "cantidad": y}.
    inicio: índice inicial del segmento.
    fin: índice final del segmento.
    
    Retorna:
    Raíz del árbol construido.
    
    Relación con el proyecto:
    Cumple el punto 5 del enunciado usando un árbol equilibrado que maneja repetidos.
    
    Costo:
    O(u), donde u es la cantidad de valores únicos.
    """
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
    """
    Construye un árbol equilibrado usando tuplas (valor, cantidad).
    
    Entrada:
    tuplas: lista ordenada de tuplas.
    inicio: índice inicial.
    fin: índice final.
    
    Retorna:
    Raíz del árbol de frecuencias.
    
    Relación con el proyecto:
    Se mantiene como alternativa a la versión JSON.
    
    Costo:
    O(u), donde u es la cantidad de valores únicos.
    """
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
    """
    Construye un árbol binario equilibrado desde un vector ordenado.
    
    Entrada:
    vector: lista ordenada.
    inicio: índice inicial.
    fin: índice final.
    
    Retorna:
    Raíz del árbol.
    
    Relación con el proyecto:
    Versión general del árbol usando nodos simples.
    
    Costo:
    O(m), donde m es la cantidad de elementos del vector.
    """
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
    """
    Busca un valor en un árbol binario de búsqueda.
    
    Entrada:
    raiz: raíz del árbol.
    buscado: valor que se desea encontrar.
    
    Retorna:
    True si el valor está en el árbol, False en caso contrario.
    
    Relación con el proyecto:
    Implementa la regla: menor izquierda, mayor derecha, igual encontrado.
    
    Costo:
    O(h), donde h es la altura del árbol.
    """
    if raiz is None:
        return False

    valor_nodo = raiz.valor if hasattr(raiz, 'valor') else raiz.dato[0]

    if buscado == valor_nodo:
        return True
    if buscado < valor_nodo:
        return buscar_en_arbol(raiz.izquierda, buscado)
    return buscar_en_arbol(raiz.derecha, buscado)


def buscar_en_arbol_json(raiz, buscado):
    """
    Busca un valor en el árbol JSON equilibrado.
    
    Entrada:
    raiz: raíz del árbol JSON.
    buscado: valor a buscar.
    
    Retorna:
    Diccionario {"valor": buscado, "cantidad": frecuencia} si lo encuentra.
    None si no lo encuentra.
    
    Relación con el proyecto:
    Cumple el punto 5.a al buscar en el árbol y devolver la cantidad de apariciones.
    
    Costo:
    O(log u) si el árbol está equilibrado, donde u es la cantidad de valores únicos.
    """
    if raiz is None:
        return None

    valor_nodo = raiz.dato["valor"]
    if buscado == valor_nodo:
        return raiz.dato
    if buscado < valor_nodo:
        return buscar_en_arbol_json(raiz.izquierda, buscado)
    return buscar_en_arbol_json(raiz.derecha, buscado)


def contar_nodos_arbol_json(raiz):
    """
    Cuenta la cantidad de nodos del árbol JSON.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Número total de nodos.
    
    Relación con el proyecto:
    Permite mostrar cuántos valores únicos tiene el árbol.
    
    Costo:
    O(u), porque visita todos los nodos.
    """
    if raiz is None:
        return 0
    return 1 + contar_nodos_arbol_json(raiz.izquierda) + contar_nodos_arbol_json(raiz.derecha)


def altura_arbol_json(raiz):
    """
    Calcula la altura del árbol JSON.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Altura del árbol.
    
    Relación con el proyecto:
    Ayuda a explicar por qué la búsqueda depende de la altura.
    
    Costo:
    O(u), porque recorre los nodos para calcular la altura.
    """
    if raiz is None:
        return 0

    altura_izquierda = altura_arbol_json(raiz.izquierda)
    altura_derecha = altura_arbol_json(raiz.derecha)

    if altura_izquierda > altura_derecha:
        return altura_izquierda + 1

    return altura_derecha + 1


def recorrido_inorden_json(raiz):
    """
    Realiza recorrido inorden sobre el árbol JSON.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Lista de diccionarios ordenados de menor a mayor por valor.
    
    Relación con el proyecto:
    Demuestra la propiedad del árbol binario de búsqueda.
    
    Costo:
    O(u), porque visita todos los nodos.
    """
    resultado = []

    def recorrer(nodo):
        if nodo is not None:
            recorrer(nodo.izquierda)
            resultado.append(nodo.dato)
            recorrer(nodo.derecha)

    recorrer(raiz)
    return resultado


def buscar_en_arbol_frecuencias(raiz, buscado):
    """
    Busca un valor en el árbol de frecuencias basado en tuplas.
    
    Entrada:
    raiz: raíz del árbol.
    buscado: valor a buscar.
    
    Retorna:
    Tupla (valor, cantidad) si lo encuentra; None en caso contrario.
    
    Relación con el proyecto:
    Se conserva como alternativa a la búsqueda JSON.
    
    Costo:
    O(h), donde h es la altura del árbol.
    """
    if raiz is None:
        return None

    valor_nodo = raiz.dato[0]
    if buscado == valor_nodo:
        return raiz.dato
    if buscado < valor_nodo:
        return buscar_en_arbol_frecuencias(raiz.izquierda, buscado)
    return buscar_en_arbol_frecuencias(raiz.derecha, buscado)


def contar_nodos_arbol_frecuencias(raiz):
    """
    Cuenta nodos en un árbol de frecuencias basado en tuplas.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Cantidad total de nodos.
    
    Costo:
    O(u), porque visita todos los nodos.
    """
    if raiz is None:
        return 0
    return 1 + contar_nodos_arbol_frecuencias(raiz.izquierda) + contar_nodos_arbol_frecuencias(raiz.derecha)


def altura_arbol(raiz):
    """
    Calcula la altura de un árbol binario.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Altura del árbol.
    
    Costo:
    O(u), porque visita todos los nodos.
    """
    if raiz is None:
        return 0
    altura_izq = altura_arbol(raiz.izquierda)
    altura_der = altura_arbol(raiz.derecha)
    return 1 + (altura_izq if altura_izq >= altura_der else altura_der)


def recorrido_inorden_frecuencias(raiz):
    """
    Recorre un árbol de frecuencias en inorden.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Lista de tuplas ordenadas de menor a mayor.
    
    Costo:
    O(u), porque visita todos los nodos.
    """
    resultado = []
    if raiz is not None:
        resultado.extend(recorrido_inorden_frecuencias(raiz.izquierda))
        resultado.append(raiz.dato)
        resultado.extend(recorrido_inorden_frecuencias(raiz.derecha))
    return resultado


def buscar_en_matriz(matriz, buscado):
    """
    Busca un valor en la matriz mediante recorrido secuencial.
    
    Entrada:
    matriz: matriz donde se busca.
    buscado: valor que se desea encontrar.
    
    Retorna:
    True si lo encuentra, False en caso contrario.
    
    Relación con el proyecto:
    Sirve para comparar contra la búsqueda en árbol.
    
    Costo:
    O(n²) en el peor caso.
    """
    for fila in matriz:
        for valor in fila:
            if valor == buscado:
                return True
    return False


def medir_tiempo(funcion, estructura, buscado):
    """
    Mide el tiempo de ejecución de una función de búsqueda.
    
    Entrada:
    funcion: función que se desea medir.
    estructura: matriz o árbol donde se busca.
    buscado: valor buscado.
    
    Retorna:
    Resultado de la función y tiempo consumido en nanosegundos.
    
    Relación con el proyecto:
    Cumple el punto 5.a y 5.b sobre tomar tiempos de ejecución.
    
    Costo:
    Depende de la función recibida.
    """
    # Mide el tiempo en nanosegundos que tarda la búsqueda
    inicio = time.perf_counter_ns()
    encontrado = funcion(estructura, buscado)
    fin = time.perf_counter_ns()
    return encontrado, fin - inicio


# =========================================================
# DIBUJO DEL ÁRBOL EN TEXTO
# =========================================================


def arbol_a_ascii(raiz):
    """
    Convierte un árbol en una representación de texto tipo ASCII.
    
    Entrada:
    raiz: raíz del árbol.
    
    Retorna:
    Cadena de texto con el dibujo del árbol.
    
    Relación con el proyecto:
    Permite visualizar el árbol sin depender de librerías externas.
    
    Costo:
    O(u), porque recorre los nodos para construir la representación.
    """
    # Convierte un árbol en una representación ASCII legible
    if raiz is None:
        return "Árbol vacío"

    def etiqueta_nodo(nodo):
        """
        Devuelve una etiqueta corta para mostrar el nodo.

        Para nodos JSON se muestra valor|cantidad.
        Ejemplo: 5|8 significa valor 5 con 8 apariciones.
        """
        if hasattr(nodo, "dato"):
            if isinstance(nodo.dato, dict):
                return str(nodo.dato["valor"]) + "|" + str(nodo.dato["cantidad"])
            return str(nodo.dato[0]) + "|" + str(nodo.dato[1])
        return str(nodo.valor)

    def display_aux(nodo):
        if nodo.izquierda is None and nodo.derecha is None:
            linea = etiqueta_nodo(nodo)
            ancho = len(linea)
            alto = 1
            centro = ancho // 2
            return [linea], ancho, alto, centro

        if nodo.derecha is None:
            lineas, ancho, alto, centro = display_aux(nodo.izquierda)
            valor = etiqueta_nodo(nodo)
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
            valor = etiqueta_nodo(nodo)
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

        valor = etiqueta_nodo(nodo)
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


def exportar_arbol_dot(raiz, nombre_grafo="Arbol"):
    """
    Exporta el árbol en formato DOT para visualización con Graphviz.
    
    Entrada:
    raiz: raíz del árbol.
    nombre_grafo: nombre del grafo en el archivo DOT.
    
    Retorna:
    Cadena de texto en formato DOT.
    
    Relación con el proyecto:
    Solo apoya la visualización del árbol; no construye ni modifica el árbol.
    
    Costo:
    O(u), porque visita cada nodo una vez.
    """
    lineas = []
    lineas.append(f"digraph {nombre_grafo} {{")
    lineas.append("    node [shape=circle];")

    contador = [0]

    def recorrer(nodo):
        if nodo is None:
            return None

        id_actual = contador[0]
        contador[0] += 1

        if hasattr(nodo, 'dato'):
            if isinstance(nodo.dato, dict):
                # Formato JSON: {"valor": num, "cantidad": freq}
                label = f"{nodo.dato['valor']} | cant: {nodo.dato['cantidad']}"
            else:
                # Formato tupla antiguo: (valor, cantidad)
                label = f"{nodo.dato[0]} | cant: {nodo.dato[1]}"
        else:
            label = str(nodo.valor)

        lineas.append(f'    nodo{id_actual} [label="{label}"];')

        id_izq = recorrer(nodo.izquierda)
        if id_izq is not None:
            lineas.append(f'    nodo{id_actual} -> nodo{id_izq};')

        id_der = recorrer(nodo.derecha)
        if id_der is not None:
            lineas.append(f'    nodo{id_actual} -> nodo{id_der};')

        return id_actual

    recorrer(raiz)

    lineas.append('}')
    return "\n".join(lineas)
