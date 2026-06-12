# ==============================================================================
# LOGICA DEL PROYECTO - ALGORITMOS Y ESTRUCTURAS DE DATOS
# ==============================================================================
# Este archivo contiene los algoritmos necesarios para el analisis de matrices,
# conteo de frecuencias, ordenamientos y construccion/busqueda en arboles BST.
# ==============================================================================

# ==============================================================================
# IMPORTACIONES Y CONFIGURACION INICIAL
# ==============================================================================

import random      # Permite generar los valores aleatorios de la matriz.
import time        # Permite medir tiempos de busqueda en nanosegundos.


# A3 requiere calcular A2 = A*A y luego A3 = A2*A; por eso se limita n.
MAX_N = 50         # Límite máximo permitido para n por el costo de calcular A³.


# ==============================================================================
# FUNCIONES AUXILIARES DE TEXTO
# ==============================================================================


def unir_con_delimitador(lista, delimitador):
    """Une una lista de elementos en un solo string usando un delimitador manual."""
    resultado = ""                              # Acumulador donde se arma el texto final.
    for i in range(len(lista)):                 # Recorre la lista por indice para controlar el ultimo elemento.
        resultado += str(lista[i])              # Convierte cada elemento a texto antes de concatenarlo.
        if i < len(lista) - 1:                  # Evita agregar delimitador despues del ultimo elemento.
            resultado += delimitador
    return resultado                            # Devuelve el texto unido manualmente.


# ==============================================================================
# FUNCIONES PARA MATRICES
# ==============================================================================


def crear_matriz(n):
    """Genera una matriz de tamaño n x n con valores aleatorios entre 0 y 9 sin usar .append()."""
    matriz = []                                 # Lista principal donde se guardan todas las filas.
    for _ in range(n):                          # Recorre la cantidad de filas que debe tener la matriz.
        fila = []                               # Crea una fila nueva para la iteracion actual.
        for _ in range(n):                      # Recorre las columnas de la fila.
            valor = random.randint(0, 9)        # Genera un entero aleatorio dentro del rango pedido.
            fila = fila + [valor]               # Agrega sin .append(), respetando la restriccion academica.
        matriz = matriz + [fila]                # Agrega la fila completa a la matriz.
    return matriz                               # Retorna la matriz n x n.


def guardar_matriz_directo_txt(n, nombre_archivo="matriz.txt"):
    """Genera una matriz fila por fila y la escribe en un archivo TXT sin guardarla completa en memoria."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo: # Abre el archivo destino en modo escritura.
        archivo.write("Matriz generada de tamaño " + str(n) + " x " + str(n) + "\n")
        linea_separadora = ""                  # Acumulador para construir una linea visual de separacion.
        for _ in range(60):                    # Genera 60 caracteres '=' manualmente.
            linea_separadora += "="
        archivo.write(linea_separadora + "\n\n")
        for i in range(n):                     # Genera cada fila sin almacenar la matriz completa.
            fila = []                          # Guarda temporalmente los valores de la fila como texto.
            for j in range(n):                 # Recorre las columnas de la fila actual.
                valor = random.randint(0, 9)   # Genera el valor de la celda.
                fila = fila + [str(valor)]     # Guarda el valor como string para escribirlo.
            linea_texto = ""                   # Acumulador de la fila formateada.
            for k in range(len(fila)):         # Recorre cada valor textual de la fila.
                formateado = ""                # Acumulador de la celda alineada.
                num_str = fila[k]              # Valor de la celda como texto.
                espacios = 10 - len(num_str)   # Calcula espacios para ancho fijo.
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
    n = len(x)                                  # Dimension de las matrices cuadradas.
    y_transpuesta = []                          # Guarda columnas de y como filas para facilitar el acceso.
    for j in range(n):                          # Recorre cada columna de y.
        columna = []                            # Acumulador de una columna transpuesta.
        for i in range(n):                      # Recorre las filas de y.
            columna = columna + [y[i][j]]       # Extrae el elemento de la columna j.
        y_transpuesta = y_transpuesta + [columna] # Agrega la columna convertida en fila.
    resultado = []                              # Matriz final de la multiplicacion.
    for i in range(n):                          # Recorre las filas de x.
        fila_resultado = []                     # Fila i del resultado.
        for j in range(n):                      # Recorre las columnas de y ya transpuestas.
            columna_y = y_transpuesta[j]        # Columna j original de y.
            suma = 0                            # Acumulador del producto punto.
            for k in range(n):                  # Multiplica elemento a elemento fila x columna.
                suma += x[i][k] * columna_y[k]
            fila_resultado = fila_resultado + [suma] # Agrega el valor calculado a la fila.
        resultado = resultado + [fila_resultado] # Agrega la fila completa al resultado.
    return resultado                            # Retorna x * y.


def guardar_A3_directo_txt(matriz_A, nombre_archivo="matriz_A3.txt"):
    """Calcula A3 = A * A * A y escribe el resultado directo en TXT fila por fila sin .append() ni .join()."""
    n = len(matriz_A)                           # Dimension de la matriz A.
    A2 = multiplicar_matrices(matriz_A, matriz_A) # Calcula A al cuadrado.
    A3 = multiplicar_matrices(A2, matriz_A)     # Calcula A al cubo.
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
    A2 = multiplicar_matrices(A, A)             # Primer producto: A2 = A * A.
    A3 = multiplicar_matrices(A2, A)            # Segundo producto: A3 = A2 * A.
    return A3                                   # Retorna la matriz elevada al cubo.


# ==============================================================================
# FUNCIONES DE ANALISIS NUMERICO
# ==============================================================================


def es_primo(numero):
    """Determina si un numero entero es primo utilizando un bucle basico."""
    if numero < 2:                              # Por definicion, 0 y 1 no son primos.
        return False
    divisor = 2                                 # Primer divisor posible.
    while divisor * divisor <= numero:          # Solo revisa hasta la raiz cuadrada.
        if numero % divisor == 0:               # Si divide exacto, no es primo.
            return False
        divisor += 1                            # Prueba el siguiente divisor.
    return True                                 # Si no encontro divisores, es primo.


def es_perfecto(numero):
    """Determina si un numero entero es perfecto (la suma de sus divisores propios es igual a el)."""
    if numero <= 1:                             # Los numeros menores o iguales a 1 no son perfectos.
        return False
    suma_divisores = 1                          # Acumula divisores propios; 1 siempre cuenta.
    divisor = 2                                 # Comienza desde el primer divisor posible despues de 1.
    while divisor * divisor <= numero:          # Recorre hasta la raiz cuadrada.
        if numero % divisor == 0:               # Detecta un divisor exacto.
            suma_divisores += divisor           # Suma el divisor encontrado.
            otro_divisor = numero // divisor    # Calcula el divisor complementario.
            if otro_divisor != divisor:         # Evita duplicar cuando ambos divisores son iguales.
                suma_divisores += otro_divisor
        divisor += 1                            # Avanza al siguiente candidato.
    return suma_divisores == numero             # Es perfecto si la suma coincide con el numero.


def es_cuadrado_perfecto(numero):
    """Comprueba si un numero es un cuadrado perfecto mediante una busqueda binaria simple."""
    if numero < 0:                              # Los negativos no tienen raiz cuadrada entera real.
        return False
    if numero == 0 or numero == 1:              # Casos directos de cuadrados perfectos.
        return True
    izquierda = 1                               # Limite inferior de la busqueda.
    derecha = numero                            # Limite superior de la busqueda.
    while izquierda <= derecha:                 # Mientras el rango sea valido.
        mitad = (izquierda + derecha) // 2      # Punto medio del rango.
        cuadrado = mitad * mitad                # Cuadrado del candidato.
        if cuadrado == numero:                  # Coincidencia exacta.
            return True
        if cuadrado < numero:                   # Si falta crecer, mueve el limite izquierdo.
            izquierda = mitad + 1
        else:
            derecha = mitad - 1                 # Si se paso, reduce el limite derecho.
    return False                                # No hubo raiz exacta.


def analizar_matriz(matriz):
    """Analiza y clasifica todos los elementos de una matriz sin usar .append()."""
    pares = []                                  # Guarda todos los valores pares encontrados.
    impares = []                                # Guarda todos los valores impares encontrados.
    primos = []                                 # Guarda todos los valores primos encontrados.
    perfectos = []                              # Guarda todos los valores perfectos encontrados.
    cuadrados = []                              # Guarda todos los cuadrados perfectos encontrados.
    cache = {}                                  # Evita recalcular propiedades de valores repetidos.
    for i in range(len(matriz)):                # Recorre filas por indice.
        fila = matriz[i]                        # Obtiene la fila actual.
        for j in range(len(fila)):              # Recorre columnas por indice.
            valor = fila[j]                     # Valor ubicado en la celda (i, j).
            if valor in cache:                  # Si ya se analizo este numero, reutiliza el resultado.
                datos = cache[valor]
            else:
                datos = {                       # Calcula las propiedades numericas del valor.
                    "par": valor % 2 == 0,
                    "primo": es_primo(valor),
                    "perfecto": es_perfecto(valor),
                    "cuadrado": es_cuadrado_perfecto(valor)
                }
                cache[valor] = datos            # Guarda el analisis para apariciones futuras.
            if datos["par"]:                    # Clasifica el valor como par o impar.
                pares = pares + [valor]
            else:
                impares = impares + [valor]
            if datos["primo"]:                  # Agrega si cumple la condicion de primo.
                primos = primos + [valor]
            if datos["perfecto"]:               # Agrega si cumple la condicion de perfecto.
                perfectos = perfectos + [valor]
            if datos["cuadrado"]:               # Agrega si es cuadrado perfecto.
                cuadrados = cuadrados + [valor]
    return {                                    # Devuelve cantidades y listas para cada categoria.
        "pares": {"cantidad": len(pares), "valores": pares},
        "impares": {"cantidad": len(impares), "valores": impares},
        "primos": {"cantidad": len(primos), "valores": primos},
        "perfectos": {"cantidad": len(perfectos), "valores": perfectos},
        "cuadrados": {"cantidad": len(cuadrados), "valores": cuadrados}
    }


def contar_repeticiones(matriz):
    """Cuenta cuantas veces aparece cada valor en la matriz, guardandolo en un diccionario."""
    frecuencias = {}                            # Diccionario valor -> cantidad.
    for i in range(len(matriz)):                # Recorre filas.
        fila = matriz[i]
        for j in range(len(fila)):              # Recorre columnas.
            valor = fila[j]                     # Valor actual de la matriz.
            if valor in frecuencias:            # Si ya existe, incrementa su contador.
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1          # Si es nuevo, inicia su frecuencia.
    return frecuencias                          # Retorna la tabla de frecuencias.

 
def buscar_y_contar_en_matriz(matriz, buscado):
    """Realiza una busqueda secuencial en la matriz para determinar si existe y cuantas veces se repite."""
    encontrado = False                          # Bandera que indica si el valor aparece.
    cantidad = 0                                # Contador de apariciones del valor buscado.
    for i in range(len(matriz)):                # Busca fila por fila.
        fila = matriz[i]
        for j in range(len(fila)):              # Revisa cada columna de la fila.
            valor = fila[j]
            if valor == buscado:                # Coincidencia con el numero solicitado.
                encontrado = True
                cantidad += 1                   # Suma una aparicion.
    return encontrado, cantidad                 # Devuelve estado y frecuencia encontrada.


# ==============================================================================
# FUNCIONES DE FRECUENCIAS Y VECTORES
# ==============================================================================


def frecuencias_a_json_ordenado(frecuencias):
    """Convierte el diccionario de frecuencias en una lista ordenada por valor sin usar .append()."""
    claves = []                                  # Guarda las claves del diccionario.
    for clave in frecuencias:                    # Recorre cada valor unico.
        claves = claves + [clave]               
    claves_ordenadas = ordenar_ascendente(claves) # Ordena los valores unicos.
    lista_json = []                              # Lista de nodos en formato valor/cantidad.
    for i in range(len(claves_ordenadas)):       # Recorre valores ordenados.
        clave = claves_ordenadas[i]
        dato = {                                 # Estructura que usara NodoJSON.
            "valor": clave,
            "cantidad": frecuencias[clave]
        }
        lista_json = lista_json + [dato]
    return lista_json                            # Retorna la lista lista para construir el arbol.


def matriz_a_vector(matriz):
    """Aplana una matriz n x n en un vector unidimensional sin usar .append()."""
    vector = []                                  # Acumulador lineal de todos los elementos.
    for i in range(len(matriz)):                 # Recorre filas.
        fila = matriz[i]
        for j in range(len(fila)):               # Recorre columnas.
            vector = vector + [fila[j]]          # Agrega cada valor al vector.
    return vector                                # Retorna matriz aplanada.


# ==============================================================================
# FUNCIONES DE ORDENAMIENTO
# ==============================================================================


def insertion_sort_ascendente(vector):
    """Ordena un vector de menor a mayor usando el algoritmo de ordenamiento por insercion."""
    for i in range(1, len(vector)):              # Toma elementos desde la segunda posicion.
        actual = vector[i]                       # Elemento que se va a insertar en su lugar.
        j = i - 1                                # Compara hacia la izquierda.
        while j >= 0 and vector[j] > actual:     # Desplaza valores mayores.
            vector[j + 1] = vector[j]
            j -= 1
        vector[j + 1] = actual                   # Inserta el valor en la posicion correcta.
    return vector                                # Retorna el mismo vector ordenado.


def invertir_vector(vector):
    """Invierte el orden de un vector sin usar metodos incorporados ni .append()."""
    invertido = []                               # Acumulador del vector en orden contrario.
    for i in range(len(vector) - 1, -1, -1):     # Recorre desde el ultimo hasta el primero.
        invertido = invertido + [vector[i]]      # Agrega cada elemento al nuevo vector.
    return invertido                             # Retorna el vector invertido.


def merge_sort_ascendente(vector):
    """Ordena un vector usando division y conquista (Merge Sort) sin usar .append()."""
    if len(vector) <= 1:                         # Caso base: una lista de 0 o 1 ya esta ordenada.
        return vector
    medio = len(vector) // 2                     # Punto de division.
    izquierda = merge_sort_ascendente(vector[:medio]) # Ordena recursivamente la mitad izquierda.
    derecha = merge_sort_ascendente(vector[medio:])   # Ordena recursivamente la mitad derecha.
    resultado = []                               # Acumulador de la mezcla ordenada.
    i = 0                                        # Indice de la mitad izquierda.
    j = 0                                        # Indice de la mitad derecha.
    while i < len(izquierda) and j < len(derecha): # Mezcla mientras ambas mitades tengan datos.
        if izquierda[i] <= derecha[j]:           # El menor pasa primero al resultado.
            resultado = resultado + [izquierda[i]]
            i += 1
        else:
            resultado = resultado + [derecha[j]]
            j += 1
    while i < len(izquierda):                    # Copia sobrantes de la izquierda.
        resultado = resultado + [izquierda[i]]
        i += 1
    while j < len(derecha):                      # Copia sobrantes de la derecha.
        resultado = resultado + [derecha[j]]
        j += 1
    return resultado                             # Retorna la mezcla ordenada.


def ordenar_ascendente(vector):
    """Elige el mejor algoritmo de ordenamiento segun el tamano de los datos."""
    if len(vector) <= 64:                        # Para entradas pequenas, insertion sort es suficiente.
        return insertion_sort_ascendente(vector)
    return merge_sort_ascendente(vector)         # Para entradas mayores, usa merge sort.


# ==============================================================================
# CLASES DE NODOS PARA ARBOLES BINARIOS DE BUSQUEDA
# ==============================================================================

class NodoJSON:
    """Clase que representa un nodo con estructura compatible con formato JSON."""

    def __init__(self, valor, cantidad):
        self.dato = {                            # Diccionario que se guarda tambien en el JSON.
            "valor": valor,                      # Valor numerico representado por el nodo.
            "cantidad": cantidad                 # Frecuencia del valor dentro de la matriz.
        }
        self.izquierda = None                    # Hijo izquierdo: valores menores.
        self.derecha = None                      # Hijo derecho: valores mayores.


# ==============================================================================
# ARBOLES BINARIOS DE BUSQUEDA EQUILIBRADOS
# ==============================================================================


def construir_arbol_json_equilibrado(lista_json, inicio, fin):
    """Construye un arbol binario equilibrado desde una lista JSON ordenada."""
    if inicio > fin:                             # Caso base: no hay elementos en este rango.
        return None
    mitad = (inicio + fin) // 2                  # El centro mantiene el arbol balanceado.
    valor = lista_json[mitad]["valor"]           # Valor unico que se guardara en el nodo.
    cantidad = lista_json[mitad]["cantidad"]     # Frecuencia asociada a ese valor.
    raiz = NodoJSON(valor, cantidad)             # Crea el nodo raiz del subarbol actual.
    raiz.izquierda = construir_arbol_json_equilibrado(lista_json, inicio, mitad - 1) # Construye menores.
    raiz.derecha = construir_arbol_json_equilibrado(lista_json, mitad + 1, fin)      # Construye mayores.
    return raiz                                  # Retorna la raiz del subarbol.


# ==============================================================================
# ALGORITMOS DE BUSQUEDA Y OPERACIONES EN ARBOLES
# ==============================================================================


def buscar_en_arbol_json(raiz, buscado):
    """Busca un numero de forma binaria en un arbol de estructura compatible JSON."""
    if raiz is None:                             # Caso base: el valor no existe en esta rama.
        return None
    valor_nodo = raiz.dato["valor"]              # Valor que se compara con el buscado.
    if buscado == valor_nodo:                    # Si coincide, retorna valor y cantidad.
        return raiz.dato
    if buscado < valor_nodo:                     # Si es menor, continua por la rama izquierda.
        return buscar_en_arbol_json(raiz.izquierda, buscado)
    return buscar_en_arbol_json(raiz.derecha, buscado) # Si es mayor, continua por la derecha.


def contar_nodos_arbol_json(raiz):
    """Cuenta todos los nodos del arbol JSON recursivamente."""
    if raiz is None:                             # Un subarbol vacio aporta cero nodos.
        return 0
    return 1 + contar_nodos_arbol_json(raiz.izquierda) + contar_nodos_arbol_json(raiz.derecha)


def altura_arbol_json(raiz):
    """Calcula la altura maxima del arbol compatible JSON."""
    if raiz is None:                             # Arbol vacio tiene altura cero.
        return 0
    altura_izquierda = altura_arbol_json(raiz.izquierda) # Altura recursiva de la rama izquierda.
    altura_derecha = altura_arbol_json(raiz.derecha)     # Altura recursiva de la rama derecha.
    if altura_izquierda > altura_derecha:        # Toma la rama mas profunda.
        return altura_izquierda + 1
    return altura_derecha + 1


def recorrido_inorden_json(raiz):
    """Retorna una lista con la estructura de recorrido inorden sin usar .append()."""
    if raiz is None:                             # Subarbol vacio produce lista vacia.
        return []
    izq = recorrido_inorden_json(raiz.izquierda) # Primero visita valores menores.
    der = recorrido_inorden_json(raiz.derecha)   # Luego visita valores mayores.
    return izq + [raiz.dato] + der               # Une izquierda, raiz y derecha.


def contar_elementos_representados_arbol(raiz):
    """Suma las cantidades de todos los nodos del arbol JSON de frecuencias."""
    if raiz is None:                             # Sin nodo no hay elementos representados.
        return 0
    cantidad_actual = raiz.dato["cantidad"]      # Frecuencia guardada en el nodo actual.
    izquierda = contar_elementos_representados_arbol(raiz.izquierda) # Suma la rama izquierda.
    derecha = contar_elementos_representados_arbol(raiz.derecha)     # Suma la rama derecha.
    return cantidad_actual + izquierda + derecha # Total representado por todo el subarbol.


def buscar_en_matriz(matriz, buscado):
    """Busca de forma directa si un valor entero existe dentro de la matriz."""
    for i in range(len(matriz)):                 # Recorre todas las filas.
        fila = matriz[i]
        for j in range(len(fila)):               # Recorre todas las columnas.
            if fila[j] == buscado:               # Retorna al encontrar la primera coincidencia.
                return True
    return False


# ==============================================================================
# MEDICION DE TIEMPOS
# ==============================================================================


def medir_tiempo(funcion, estructura, buscado):
    """Mide el tiempo transcurrido en nanosegundos al ejecutar una busqueda."""
    inicio = time.perf_counter_ns()              # Marca el tiempo antes de ejecutar la funcion.
    encontrado = funcion(estructura, buscado)    # Ejecuta la busqueda recibida como parametro.
    fin = time.perf_counter_ns()                 # Marca el tiempo despues de ejecutar.
    return encontrado, fin - inicio              # Devuelve resultado y duracion.


def medir_tiempo_promedio(funcion, estructura, buscado, repeticiones=1000):
    """Mide el tiempo promedio de una busqueda sin reemplazar medir_tiempo."""
    tiempo_total = 0                             # Acumula los nanosegundos de todas las repeticiones.
    resultado = None                             # Guarda el ultimo resultado funcional de la busqueda.

    for _ in range(repeticiones):                # Repite para suavizar variaciones del sistema.
        inicio = time.perf_counter_ns()
        resultado = funcion(estructura, buscado)
        fin = time.perf_counter_ns()
        tiempo_total += fin - inicio             # Acumula la duracion individual.

    promedio = tiempo_total / repeticiones       # Calcula el promedio aritmetico.
    return resultado, promedio                   # Devuelve resultado y tiempo promedio.


# ==============================================================================
# DIBUJO DEL ARBOL EN TEXTO (REPRESENTACION ASCII)
# ==============================================================================


def arbol_a_ascii(raiz):
    """Genera un dibujo ASCII del arbol binario con ramas visuales sin .append() ni .join()."""
    if raiz is None:                             # Si no hay raiz, no existe arbol para dibujar.
        return "Árbol vacío"

    def display_aux(nodo):
        """Construye recursivamente las lineas ASCII de cada subarbol."""
        if nodo.izquierda is None and nodo.derecha is None: # Caso hoja: no tiene hijos.
            if hasattr(nodo, 'dato'):             # NodoJSON guarda el valor dentro de dato.
                linea = str(nodo.dato["valor"])
            else:
                linea = str(nodo.valor)
            ancho = len(linea)                    # Ancho del texto del nodo.
            alto = 1                              # Una hoja ocupa una linea.
            centro = ancho // 2                   # Centro visual del nodo.
            return [linea], ancho, alto, centro

        if nodo.derecha is None:                  # Caso con solo hijo izquierdo.
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

        if nodo.izquierda is None:                # Caso con solo hijo derecho.
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

        izquierda, ancho_izq, alto_izq, centro_izq = display_aux(nodo.izquierda) # Dibuja rama izquierda.
        derecha, ancho_der, alto_der, centro_der = display_aux(nodo.derecha)     # Dibuja rama derecha.
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
        if alto_izq < alto_der:                   # Iguala alturas agregando lineas vacias.
            diferencia = alto_der - alto_izq
            for _ in range(diferencia):
                relleno_izq = ""                  # Relleno para alinear la rama izquierda.
                for _ in range(ancho_izq):
                    relleno_izq += " "
                izquierda = izquierda + [relleno_izq]
        elif alto_der < alto_izq:
            diferencia = alto_izq - alto_der
            for _ in range(diferencia):
                relleno_der = ""                  # Relleno para alinear la rama derecha.
                for _ in range(ancho_der):
                    relleno_der += " "
                derecha = derecha + [relleno_der]
        lineas = [primera, segunda]               # Primeras dos lineas: nodo y conectores.
        for idx in range(len(izquierda)):
            linea_izq = izquierda[idx]
            linea_der = derecha[idx]
            relleno_central = ""
            for _ in range(ancho_valor):
                relleno_central += " "
            lineas = lineas + [linea_izq + relleno_central + linea_der]
        return lineas, ancho_izq + ancho_valor + ancho_der, max(alto_izq, alto_der) + 2, ancho_izq + ancho_valor // 2

    lineas, _, _, _ = display_aux(raiz)           # Genera el dibujo completo desde la raiz.
    if not lineas:
        return "Árbol vacío"
    ancho_maximo = 0                              # Busca la linea mas ancha para centrar el dibujo.
    for i in range(len(lineas)):
        l = len(lineas[i])
        if l > ancho_maximo:
            ancho_maximo = l
    lineas_centradas = []                         # Guarda cada linea con margen visual.
    for i in range(len(lineas)):
        linea = lineas[i]
        ancho_actual = len(linea)
        faltante = (ancho_maximo + 8) - ancho_actual # Espacio faltante para centrar.
        mitad_izq = faltante // 2
        mitad_der = faltante - mitad_izq
        espacio_izq = ""                          # Espacios agregados antes de la linea.
        for _ in range(mitad_izq):
            espacio_izq += " "
        espacio_der = ""
        for _ in range(mitad_der):
            espacio_der += " "
        linea_centrada = espacio_izq + linea + espacio_der
        lineas_centradas = lineas_centradas + [linea_centrada]
    return unir_con_delimitador(lineas_centradas, "\n") # Une las lineas del dibujo.

