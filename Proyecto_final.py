import random
import time
import css

# Solicita un tamaño válido para la matriz.
def tamañoMatriz_n(): 
    while True:
        try:
            n = int(input("Ingrese el tamaño de la matriz debe ser mayor o igual a 4: "))
            if n >= 4:
                return n
            print("Error: n debe ser mayor o igual a 4")
        except ValueError:
            print("Error: debe ingresar un número entero")

# Crea una matriz cuadrada con valores aleatorios entre 0 y 9.
def crear_matriz(n):
    matriz = []  # Guarda todas las filas de la matriz.
    for i in range(n):  # Recorre cada fila.
        fila = []  # Crea una fila vacía.
        for j in range(n):  # Recorre cada columna.
            fila.append(random.randint(0, 9))  # Agrega un número aleatorio.
        matriz.append(fila)  # Inserta la fila en la matriz.
    return matriz


# Muestra la matriz en formato de tabla.
def mostrar_matriz(matriz):
    for fila in matriz:  # Recorre cada fila.
        for valor in fila:  # Recorre cada valor de la fila.
            print(valor, end="\t") 
        print()

# Multiplica dos matrices cuadradas del mismo tamaño.
def multiplicar_matrices(x, y):
    n = len(x)  # Toma el tamaño de la matriz.
    contador = []  # Guarda la matriz resultado.
    for i in range(n):  # Recorre las filas del resultado.
        fila_contador = []  # Crea una fila vacía para el resultado.
        for j in range(n):  # Recorre las columnas del resultado.
            suma = 0  # Acumula el valor de cada celda.
            for k in range(n):  # Hace el producto punto de fila por columna.
                suma = suma + x[i][k] * y[k][j]
            fila_contador.append(suma)
        contador.append(fila_contador)
    return contador

#Calcular matriz A3 
def calcular_A3(A):
    # Calcula A3 = A * A * A.
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)
    return A3

#Números primos
def es_primo(numero):
    # Verifica si un número solo tiene dos divisores.
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor = divisor + 1
    return True

#numeros perfectos
def es_perfecto(numero):
    # Verifica si la suma de sus divisores propios da el mismo número.
    if numero <= 0:
        return False
    suma_divisores = 0
    for divisor in range(1, numero):
        if numero % divisor == 0:
            suma_divisores = suma_divisores + divisor
    return suma_divisores == numero

# cuadrados perfectos
def es_cuadrado_perfecto(numero):
    # Verifica si el número es resultado de elevar otro al cuadrado.
    if numero < 0:
        return False
    raiz = 0
    while raiz * raiz <= numero:
        if raiz * raiz == numero:
            return True
        raiz = raiz + 1
    return False

#Analizar la matriz para contar pares, impares, primos, perfectos y cuadrados perfectos.
def analizar_matriz(matriz):

    pares = []  # Guarda números pares.
    impares = []  # Guarda números impares.
    primos = []  # Guarda números primos.
    perfectos = []  # Guarda números perfectos.
    cuadrados = []  # Guarda cuadrados perfectos.
    for fila in matriz:
        for valor in fila:
            if valor % 2 == 0:
                pares.append(valor)
            else:
                impares.append(valor)
            if es_primo(valor):
                primos.append(valor)
            if es_perfecto(valor):
                perfectos.append(valor)
            if es_cuadrado_perfecto(valor):
                cuadrados.append(valor)
    return {
        "pares": {
            "cantidad": len(pares),
            "valores": pares
        },
        "impares": {
            "cantidad": len(impares),
            "valores": impares
        },
        "primos": {
            "cantidad": len(primos),
            "valores": primos
        },
        "perfectos": {
            "cantidad": len(perfectos),
            "valores": perfectos
        },
        "cuadrados": {
            "cantidad": len(cuadrados),
            "valores": cuadrados
        }
    }


# Contar repeticiones cada número en la matriz y guardarlas en un diccionario.
def contar_repeticiones(matriz):
    frecuencias = {}  # Guarda cuántas veces aparece cada valor.
    for fila in matriz:
        for valor in fila:
            if valor in frecuencias:
                frecuencias[valor] = frecuencias[valor] + 1
            else:
                frecuencias[valor] = 1
    return frecuencias

# mostrar repeticiones de cada número en la matriz.
def mostrar_repeticiones(frecuencias):

    for valor in frecuencias:
        print(valor, "aparece", frecuencias[valor], "veces")

# Pasa la matriz a un vector (lista) con todos los elementos.
def matriz_a_vector(matriz):
    vector = []  # Reúne todos los elementos en una sola lista.
    for fila in matriz:
        for valor in fila:
            vector.append(valor)
    return vector

# insertar sort ascendente para ordenar el vector de menor a mayor.
def insertion_sort_ascendente(vector):
    # Ordena de menor a mayor usando inserción.
    for i in range(1, len(vector)):
        actual = vector[i]
        j = i - 1
        while j >= 0 and vector[j] > actual:
            vector[j + 1] = vector[j]
            j = j - 1
        vector[j + 1] = actual
    return vector

# Ordena de mayor a menor usando inserción.
def insertion_sort_descendente(vector):
    for i in range(1, len(vector)):
        actual = vector[i]
        j = i - 1
        while j >= 0 and vector[j] < actual:
            vector[j + 1] = vector[j]
            j = j - 1
        vector[j + 1] = actual
    return vector

#nodo arbol binario de búsqueda equilibrado
class Nodo:
    def __init__(self, valor):
        self.valor = valor  # Dato guardado en el nodo.
        self.izquierda = None  # Hijo izquierdo.
        self.derecha = None  # Hijo derecho.

#construir un árbol binario de búsqueda equilibrado a partir de un vector ordenado.
def construir_arbol_equilibrado(vector, inicio, fin):
    # Toma el elemento central como raíz y divide el resto.
    if inicio > fin:
        return None
    mitad = (inicio + fin) // 2
    raiz = Nodo(vector[mitad])
    raiz.izquierda = construir_arbol_equilibrado(
        vector,
        inicio,
        mitad - 1
    )
    raiz.derecha = construir_arbol_equilibrado(
        vector,
        mitad + 1,
        fin
    )
    return raiz

#mostrar el árbol en orden (izquierda, raíz, derecha).
def mostrar_inorden(raiz):
    # Recorre el árbol de izquierda a derecha.
    if raiz is not None:
        mostrar_inorden(raiz.izquierda)
        print(raiz.valor, end=" ")
        mostrar_inorden(raiz.derecha)


# buscar un valor en el árbol binario de búsqueda aprovechando su orden.
def buscar_en_arbol(raiz, buscado):

    # Aprovecha el orden del árbol para buscar más rápido.
    if raiz is None:
        return False
    if buscado == raiz.valor:
        return True
    if buscado < raiz.valor:
        return buscar_en_arbol(
            raiz.izquierda,
            buscado
        )
    return buscar_en_arbol(
        raiz.derecha,
        buscado
    )

# buscar un valor en la matriz recorriéndola completamente.
def buscar_en_matriz(matriz, buscado):

    # Recorre toda la matriz hasta encontrar el valor.
    for fila in matriz:
        for valor in fila:
            if valor == buscado:
                return True
    return False

# Medir el tiempo que tarda una función de búsqueda en encontrar un valor, en nanosegundos.
def medir_tiempo(funcion, estructura, buscado):
    # Mide cuánto tarda una búsqueda en nanosegundos.
    inicio = time.perf_counter_ns()
    encontrado = funcion(
        estructura,
        buscado
    )

    fin = time.perf_counter_ns()
    tiempo = fin - inicio
    return encontrado, tiempo

# Función principal que ejecuta todo el programa.
def main():

    css.activar_colores()

    # Pide el tamaño, crea la matriz y calcula A3.
    numero = tamañoMatriz_n()
    A = crear_matriz(numero)
    css.titulo("MATRIZ A", css.Color.CYAN)
    css.mostrar_matriz_bonita(A)
    A3 = calcular_A3(A)
    css.titulo("MATRIZ A^3", css.Color.CYAN)
    css.mostrar_matriz_bonita(A3)

    # mostrar análisis de la matriz A y contar repeticiones.
    css.titulo("ANALISIS MATRIZ A", css.Color.VERDE)
    css.mostrar_analisis_bonito(analizar_matriz(A))
    frecuencias_A = contar_repeticiones(A)
    css.titulo("REPETICIONES MATRIZ A", css.Color.AMARILLO)
    css.mostrar_repeticiones_bonitas(frecuencias_A)

    # mostrar análisis de la matriz A3 y contar repeticiones.
    css.titulo("ANALISIS MATRIZ A^3", css.Color.VERDE)
    css.mostrar_analisis_bonito(analizar_matriz(A3))
    frecuencias_A3 = contar_repeticiones(A3)
    css.titulo("REPETICIONES MATRIZ A^3", css.Color.AMARILLO)
    css.mostrar_repeticiones_bonitas(frecuencias_A3)

    # mostrar los vectores A y A3, ordenarlos y mostrar los vectores ordenados.
    vector_A = matriz_a_vector(A)
    vector_A3 = matriz_a_vector(A3)
    css.titulo("VECTOR A", css.Color.CYAN)
    css.mostrar_vector_bonito(vector_A)
    css.titulo("VECTOR A ORDENADO", css.Color.CYAN)
    vector_A_asc = insertion_sort_ascendente(
        vector_A.copy()
    )
    css.mostrar_vector_bonito(vector_A_asc)
    css.titulo("VECTOR A^3", css.Color.CYAN)
    css.mostrar_vector_bonito(vector_A3)
    css.titulo("VECTOR A^3 ORDENADO", css.Color.CYAN)
    vector_A3_asc = insertion_sort_ascendente(
        vector_A3.copy()
    )
    css.mostrar_vector_bonito(vector_A3_asc)

    # construir los árboles binarios de búsqueda equilibrados a partir de los vectores ordenados y mostrar su recorrido inorden.
    arbol_A = construir_arbol_equilibrado(
        vector_A_asc,
        0,
        len(vector_A_asc) - 1
    )
    arbol_A3 = construir_arbol_equilibrado(
        vector_A3_asc,
        0,
        len(vector_A3_asc) - 1
    )
    css.titulo("ARBOL BINARIO DE BUSQUEDA (MATRIZ A)", css.Color.CYAN, 55)
    css.mostrar_arbol_bonito(arbol_A)

    css.titulo("ARBOL BINARIO DE BUSQUEDA (MATRIZ A^3)", css.Color.CYAN, 55)
    css.mostrar_arbol_bonito(arbol_A3)
    print()


   # solicitar al usuario un número a buscar y medir el tiempo que tarda en encontrarlo en la matriz y en el árbol, mostrando los resultados.
    while True:
        try:
            buscado = int(input("\nIngrese el número a buscar: "))
            break
        except ValueError:
            print("Error: debe ingresar un número entero")
    encontrado_matriz, tiempo_matriz = medir_tiempo(
        buscar_en_matriz,
        A,
        buscado
    )
    encontrado_arbol, tiempo_arbol = medir_tiempo(
        buscar_en_arbol,
   
        arbol_A,
        buscado
    )
    css.titulo("RESULTADOS DE BUSQUEDA EN MATRIZ A", css.Color.MAGENTA)
    css.mostrar_resultados_busqueda(
        encontrado_matriz,
        tiempo_matriz,
        encontrado_arbol,
        tiempo_arbol
    )


# ------------------------------------------
# EJECUTAR PROGRAMA
# ------------------------------------------
if __name__ == "__main__":
    main()
