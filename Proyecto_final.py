# ==============================================================================
# PROYECTO FINAL - BACKEND (LÓGICA ALGORÍTMICA)
# ==============================================================================
# Este archivo contiene todos los algoritmos requeridos para el análisis de
# matrices, conteo de frecuencias, ordenamientos, construcción y búsqueda en 
# árboles binarios equilibrados (BST).
# ==============================================================================

import random         # Importa el módulo random para generar números aleatorios.
import time           # Importa el módulo time para medir el tiempo de ejecución.
import tracemalloc    # Importa el módulo tracemalloc para medir el uso de memoria RAM.
 

def unir_con_delimitador(lista, delimitador):
    """Une una lista de elementos en un solo string usando un delimitador manual."""
    resultado = ""                                             # Inicializa un string vacío para el resultado.
    for i in range(len(lista)):                                # Recorre los índices de la lista desde 0 hasta su longitud - 1.
        resultado += str(lista[i])                             # Concatena el elemento actual convertido a texto.
        if i < len(lista) - 1:                                 # Verifica si el elemento actual no es el último de la lista.
            resultado += delimitador                           # Concatena el delimitador después del elemento.
    return resultado                                           # Retorna la cadena de texto resultante.


def crear_matriz(n):
    """Genera una matriz de tamaño n x n con valores aleatorios entre 0 y 9 sin usar .append()."""
    matriz = []                                                # Inicializa la matriz como una lista vacía.
    for _ in range(n):                                         # Itera n veces para crear las n filas de la matriz.
        fila = []                                              # Inicializa una fila vacía para la iteración actual.
        for _ in range(n):                                     # Itera n veces para rellenar la fila actual con columnas.
            valor = random.randint(0, 9)                       # Genera un número entero aleatorio entre 0 y 9 inclusive.
            fila = fila + [valor]                              # Agrega el valor generado a la fila usando concatenación de listas.
        matriz = matriz + [fila]                               # Agrega la fila terminada a la matriz usando concatenación de listas.
    return matriz                                              # Retorna la matriz completa de tamaño n x n.


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
    """Calcula A3 = A * A * A y escribe el resultado directo en TXT fila por fila sin .append() ni .join()."""
    n = len(matriz_A)                                          # Obtiene la dimensión n de la matriz A.
    A2 = multiplicar_matrices(matriz_A, matriz_A)              # Calcula la matriz cuadrada A2 = A * A.
    A3 = multiplicar_matrices(A2, matriz_A)                    # Calcula la matriz cúbica A3 = A2 * A.
    with open(nombre_archivo, "w", encoding="utf-8") as archivo: # Abre el archivo TXT para guardar los resultados.
        archivo.write("Matriz A³ de tamaño " + str(n) + " x " + str(n) + "\n") # Escribe el encabezado.
        linea_separadora = ""                                  # Inicializa el string para la línea divisoria.
        for _ in range(60):                                    # Itera 60 veces para armar la línea divisoria.
            linea_separadora += "="                            # Agrega un '=' a la línea divisoria en cada iteración.
        archivo.write(linea_separadora + "\n\n")               # Escribe el separador en el archivo.
        for i in range(len(A3)):                               # Recorre cada fila del resultado A3.
            fila = A3[i]                                       # Obtiene la fila i de la matriz A3.
            linea_texto = ""                                   # Inicializa el string para la fila.
            for k in range(len(fila)):                         # Itera por cada número de la fila.
                num_str = str(fila[k])                         # Convierte el valor numérico a texto.
                espacios = 10 - len(num_str)                   # Calcula los espacios para alineación a la derecha.
                formateado = num_str                           # Inicializa la celda formateada.
                for _ in range(espacios):                      # Agrega los espacios necesarios.
                    formateado += " "                          # Suma un espacio en blanco.
                linea_texto += formateado                      # Agrega el valor formateado a la línea.
                if k < len(fila) - 1:                          # Si no es el último número.
                    linea_texto += "   "                       # Agrega tres espacios para separar columnas.
            archivo.write(linea_texto + "\n")                  # Escribe la línea completa en el archivo con salto de línea.
            if i % 100 == 0:                                   # Informa el progreso cada 100 filas escritas.
                print("Guardando fila " + str(i) + " de " + str(n) + "...") # Imprime el estado del guardado en consola.
    print("Matriz A³ guardada correctamente en " + str(nombre_archivo)) # Imprime mensaje de éxito final en consola.
    return A3                                                  # Retorna la matriz A3 calculada.


def calcular_A3(A):
    """Calcula la potencia de la matriz A al cubo (A3 = A2 * A)."""
    A2 = multiplicar_matrices(A, A)                            # Calcula A al cuadrado.
    A3 = multiplicar_matrices(A2, A)                           # Multiplica A al cuadrado por A para obtener A al cubo.
    return A3                                                  # Retorna la matriz cúbica resultante.


def estimar_memoria_matriz(n):
    """Realiza una estimación teórica del tamaño en bytes que ocupa la matriz A en memoria."""
    return n * n * 28                                          # Estima 28 bytes por cada número entero en la matriz de n*n.


def iniciar_medicion_memoria():
    """Inicia el rastreo de uso de memoria utilizando el módulo tracemalloc."""
    tracemalloc.start()                                        # Activa el rastreo de memoria de Python.


def obtener_memoria_actual_y_pico():
    """Retorna el uso de memoria RAM actual y el pico máximo alcanzado durante el rastreo."""
    actual, pico = tracemalloc.get_traced_memory()             # Consulta el estado del gestor de memoria de Python.
    return actual, pico                                        # Retorna los bytes actuales y el pico máximo registrado.


def detener_medicion_memoria():
    """Detiene el rastreador de memoria de tracemalloc y libera recursos."""
    tracemalloc.stop()                                         # Apaga el rastreo de asignaciones de memoria de Python.


def es_primo(numero):
    """Determina si un número entero es primo utilizando un bucle básico."""
    if numero < 2:                                             # Si el número es menor a 2, no es primo por definición.
        return False                                           # Retorna Falso.
    divisor = 2                                                # Inicializa el primer divisor posible en 2.
    while divisor * divisor <= numero:                         # Bucle mientras el cuadrado del divisor sea menor o igual al número.
        if numero % divisor == 0:                              # Si la división da residuo cero, es divisible por otro número.
            return False                                       # Retorna Falso (no es primo).
        divisor += 1                                           # Incrementa el divisor para verificar el siguiente.
    return True                                                # Si no se hallaron divisores, el número es primo, retorna Verdadero.


def es_perfecto(numero):
    """Determina si un número entero es perfecto (la suma de sus divisores propios es igual a él)."""
    if numero <= 1:                                            # Los números menores o iguales a 1 no son perfectos.
        return False                                           # Retorna Falso.
    suma_divisores = 1                                         # Inicializa la suma de divisores propios en 1 (el 1 siempre es divisor).
    divisor = 2                                                # Comienza la búsqueda de divisores desde el 2.
    while divisor * divisor <= numero:                         # Bucle hasta la raíz cuadrada del número.
        if numero % divisor == 0:                              # Si el residuo es cero, divisor es un divisor del número.
            suma_divisores += divisor                          # Suma el divisor encontrado.
            otro_divisor = numero // divisor                   # Obtiene el divisor complementario.
            if otro_divisor != divisor:                        # Verifica que el divisor complementario no sea igual al divisor actual.
                suma_divisores += otro_divisor                 # Suma el divisor complementario.
        divisor += 1                                           # Avanza al siguiente entero.
    return suma_divisores == numero                            # Retorna Verdadero si la suma acumulada es igual al número original.


def es_cuadrado_perfecto(numero):
    """Comprueba si un número es un cuadrado perfecto mediante una búsqueda binaria simple."""
    if numero < 0:                                             # Los números negativos no tienen raíz real, no son cuadrados perfectos.
        return False                                           # Retorna Falso.
    if numero == 0 or numero == 1:                             # El 0 y el 1 son cuadrados perfectos por definición.
        return True                                            # Retorna Verdadero.
    izquierda = 1                                              # Límite izquierdo de búsqueda binaria.
    derecha = numero                                           # Límite derecho de búsqueda binaria.
    while izquierda <= derecha:                                # Bucle mientras los límites no se crucen.
        mitad = (izquierda + derecha) // 2                     # Encuentra el elemento del centro del rango.
        cuadrado = mitad * mitad                               # Calcula el cuadrado del valor medio.
        if cuadrado == numero:                                 # Si el cuadrado coincide con el número, se halló la raíz exacta.
            return True                                        # Retorna Verdadero.
        if cuadrado < numero:                                  # Si el cuadrado es menor, la raíz debe ser mayor.
            izquierda = mitad + 1                              # Mueve el límite izquierdo hacia adelante.
        else:                                                  # Si el cuadrado es mayor, la raíz debe ser menor.
            derecha = mitad - 1                                # Mueve el límite derecho hacia atrás.
    return False                                               # Si termina el bucle sin coincidencia, no es cuadrado perfecto, retorna Falso.


def analizar_matriz(matriz):
    """Analiza y clasifica todos los elementos de una matriz sin usar .append()."""
    pares = []                                                 # Inicializa la lista de números pares vacía.
    impares = []                                               # Inicializa la lista de números impares vacía.
    primos = []                                                # Inicializa la lista de números primos vacía.
    perfectos = []                                             # Inicializa la lista de números perfectos vacía.
    cuadrados = []                                             # Inicializa la lista de cuadrados perfectos vacía.
    cache = {}                                                 # Crea un diccionario para no repetir cálculos con valores duplicados.
    for i in range(len(matriz)):                               # Recorre cada fila de la matriz usando su índice.
        fila = matriz[i]                                       # Obtiene la fila actual.
        for j in range(len(fila)):                             # Recorre cada columna de la fila actual usando su índice.
            valor = fila[j]                                    # Obtiene el número en la posición (i, j).
            if valor in cache:                                 # Verifica si las propiedades de este valor ya fueron calculadas.
                datos = cache[valor]                           # Recupera las propiedades almacenadas de la memoria caché.
            else:                                              # Si es la primera vez que se ve el número.
                datos = {                                      # Genera un nuevo diccionario con las propiedades calculadas.
                    "par": valor % 2 == 0,                     # Comprueba si el valor es par.
                    "primo": es_primo(valor),                  # Comprueba si el valor es primo.
                    "perfecto": es_perfecto(valor),            # Comprueba si el valor es perfecto.
                    "cuadrado": es_cuadrado_perfecto(valor)    # Comprueba si el valor es cuadrado perfecto.
                }                                              # Cierra el diccionario temporal.
                cache[valor] = datos                           # Guarda el resultado en el diccionario caché para futuros usos.
            if datos["par"]:                                   # Si la propiedad par es verdadera.
                pares = pares + [valor]                        # Agrega el valor a pares con concatenación de listas.
            else:                                              # Si el valor no es par (es impar).
                impares = impares + [valor]                    # Agrega el valor a impares con concatenación de listas.
            if datos["primo"]:                                 # Si el valor es primo.
                primos = primos + [valor]                      # Agrega el valor a primos con concatenación de listas.
            if datos["perfecto"]:                              # Si el valor es perfecto.
                perfectos = perfectos + [valor]                # Agrega el valor a perfectos con concatenación de listas.
            if datos["cuadrado"]:                              # Si el valor es cuadrado perfecto.
                cuadrados = cuadrados + [valor]                # Agrega el valor a cuadrados con concatenación de listas.
    return {                                                   # Retorna el análisis estructurado en forma de diccionarios de valores.
        "pares": {"cantidad": len(pares), "valores": pares},   # Cantidad y lista de pares.
        "impares": {"cantidad": len(impares), "valores": impares}, # Cantidad y lista de impares.
        "primos": {"cantidad": len(primos), "valores": primos},   # Cantidad y lista de primos.
        "perfectos": {"cantidad": len(perfectos), "valores": perfectos}, # Cantidad y lista de perfectos.
        "cuadrados": {"cantidad": len(cuadrados), "valores": cuadrados}  # Cantidad y lista de cuadrados.
    }                                                          # Fin del retorno del análisis.


def contar_repeticiones(matriz):
    """Cuenta cuántas veces aparece cada valor en la matriz, guardándolo en un diccionario."""
    frecuencias = {}                                           # Inicializa el diccionario de frecuencias como vacío.
    for i in range(len(matriz)):                               # Recorre cada una de las filas.
        fila = matriz[i]                                       # Extrae la fila actual.
        for j in range(len(fila)):                             # Recorre cada elemento en las columnas de la fila.
            valor = fila[j]                                    # Obtiene el valor del elemento.
            if valor in frecuencias:                           # Si el valor ya está registrado en el diccionario.
                frecuencias[valor] += 1                        # Incrementa el conteo del valor en 1.
            else:                                              # Si es la primera vez que se encuentra este valor.
                frecuencias[valor] = 1                         # Inicializa el conteo del valor en 1.
    return frecuencias                                         # Retorna el diccionario con los conteos de frecuencia.


def buscar_y_contar_en_matriz(matriz, buscado):
    """Realiza una búsqueda secuencial en la matriz para determinar si existe y cuántas veces se repite."""
    encontrado = False                                         # Inicializa el estado de bandera en Falso.
    cantidad = 0                                               # Inicializa el contador de repeticiones en 0.
    for i in range(len(matriz)):                               # Recorre cada una de las filas de la matriz.
        fila = matriz[i]                                       # Obtiene la fila actual.
        for j in range(len(fila)):                             # Recorre cada número en la fila.
            valor = fila[j]                                    # Obtiene el valor en la posición actual.
            if valor == buscado:                               # Si el valor coincide con el número buscado.
                encontrado = True                              # Cambia el estado de la bandera a Verdadero.
                cantidad += 1                                  # Incrementa el contador de repeticiones.
    return encontrado, cantidad                                # Retorna la tupla indicando si se encontró y la frecuencia.


def frecuencias_a_json_ordenado(frecuencias):
    """Convierte el diccionario de frecuencias en una lista ordenada por valor sin usar .append()."""
    claves = []                                                # Inicializa la lista para guardar las claves.
    for clave in frecuencias:                                  # Itera sobre todas las claves del diccionario de frecuencias.
        claves = claves + [clave]                              # Agrega la clave actual por concatenación de listas.
    claves_ordenadas = ordenar_ascendente(claves)              # Ordena la lista de claves de menor a mayor.
    lista_json = []                                            # Inicializa la lista final en formato ordenado.
    for i in range(len(claves_ordenadas)):                     # Itera sobre los elementos ordenados.
        clave = claves_ordenadas[i]                            # Obtiene la clave actual.
        dato = {                                               # Crea un nodo diccionario con valor y cantidad.
            "valor": clave,                                    # Guarda el valor de la clave.
            "cantidad": frecuencias[clave]                     # Asocia su correspondiente frecuencia.
        }                                                      # Cierra el diccionario de datos.
        lista_json = lista_json + [dato]                       # Concatena el diccionario a la lista de salida.
    return lista_json                                          # Retorna la lista ordenada en formato de representación.


def frecuencias_a_tuplas_ordenadas(frecuencias):
    """Convierte el diccionario de frecuencias en una lista de tuplas ordenada sin usar .append()."""
    claves = []                                                # Inicializa la lista para guardar las claves del diccionario.
    for clave in frecuencias:                                  # Itera sobre las claves del diccionario.
        claves = claves + [clave]                              # Agrega la clave actual usando concatenación de listas.
    claves_ordenadas = ordenar_ascendente(claves)              # Ordena las claves.
    tuplas = []                                                # Inicializa la lista final de tuplas.
    for i in range(len(claves_ordenadas)):                     # Itera por el índice de las claves ordenadas.
        clave = claves_ordenadas[i]                            # Obtiene la clave del índice.
        tuplas = tuplas + [(clave, frecuencias[clave])]         # Agrega la tupla (clave, cantidad) a la lista.
    return tuplas                                              # Retorna la lista de tuplas ordenadas.


def matriz_a_vector(matriz):
    """Aplana una matriz n x n en un vector unidimensional sin usar .append()."""
    vector = []                                                # Inicializa el vector unidimensional como vacío.
    for i in range(len(matriz)):                               # Recorre cada fila.
        fila = matriz[i]                                       # Obtiene la fila actual.
        for j in range(len(fila)):                             # Recorre cada valor en la fila.
            vector = vector + [fila[j]]                        # Agrega el número al vector usando concatenación de listas.
    return vector                                              # Retorna el vector plano resultante.


def insertion_sort_ascendente(vector):
    """Ordena un vector de menor a mayor usando el algoritmo de ordenamiento por inserción."""
    for i in range(1, len(vector)):                            # Comienza desde la segunda posición del vector.
        actual = vector[i]                                     # Guarda el valor actual a posicionar.
        j = i - 1                                              # Inicializa el índice para buscar la posición correcta hacia la izquierda.
        while j >= 0 and vector[j] > actual:                   # Desplaza elementos mayores a la derecha.
            vector[j + 1] = vector[j]                          # Mueve el elemento una posición a la derecha.
            j -= 1                                             # Retrocede una posición en el vector.
        vector[j + 1] = actual                                 # Inserta el elemento actual en la posición vacante.
    return vector                                              # Retorna el vector ordenado.


def invertir_vector(vector):
    """Invierte el orden de un vector sin usar métodos incorporados ni .append()."""
    invertido = []                                             # Inicializa la lista invertida vacía.
    for i in range(len(vector) - 1, -1, -1):                   # Recorre la lista de atrás hacia adelante.
        invertido = invertido + [vector[i]]                    # Concatena el elemento al nuevo vector invertido.
    return invertido                                           # Retorna la lista en el orden inverso.


def merge_sort_ascendente(vector):
    """Ordena un vector usando división y conquista (Merge Sort) sin usar .append()."""
    if len(vector) <= 1:                                       # Caso base: un vector con 0 o 1 elementos ya está ordenado.
        return vector                                          # Retorna el vector sin modificar.
    medio = len(vector) // 2                                   # Calcula la mitad del vector.
    izquierda = merge_sort_ascendente(vector[:medio])          # Ordena recursivamente la mitad izquierda del vector.
    derecha = merge_sort_ascendente(vector[medio:])            # Ordena recursivamente la mitad derecha del vector.
    resultado = []                                             # Inicializa la lista resultante de la mezcla vacía.
    i = 0                                                      # Inicializa el puntero de la mitad izquierda en 0.
    j = 0                                                      # Inicializa el puntero de la mitad derecha en 0.
    while i < len(izquierda) and j < len(derecha):             # Bucle mientras existan elementos en ambas sublistas.
        if izquierda[i] <= derecha[j]:                         # Si el elemento de la izquierda es menor o igual.
            resultado = resultado + [izquierda[i]]             # Agrega el valor de la izquierda al resultado.
            i += 1                                             # Avanza el puntero de la izquierda.
        else:                                                  # Si el elemento de la derecha es menor.
            resultado = resultado + [derecha[j]]               # Agrega el valor de la derecha al resultado.
            j += 1                                             # Avanza el puntero de la derecha.
    while i < len(izquierda):                                  # Agrega los elementos restantes en la izquierda, si los hay.
        resultado = resultado + [izquierda[i]]                 # Concatena el elemento restante al resultado.
        i += 1                                                 # Incrementa el puntero de la izquierda.
    while j < len(derecha):                                    # Agrega los elementos restantes en la derecha, si los hay.
        resultado = resultado + [derecha[j]]                   # Concatena el elemento restante al resultado.
        j += 1                                                 # Incrementa el puntero de la derecha.
    return resultado                                           # Retorna la lista mezclada y ordenada.


def ordenar_ascendente(vector):
    """Elige el mejor algoritmo de ordenamiento según el tamaño de los datos."""
    if len(vector) <= 64:                                      # Si el tamaño es pequeño (menor o igual a 64).
        return insertion_sort_ascendente(vector)               # Usa Insertion Sort para ahorrar sobrecarga de recursividad.
    return merge_sort_ascendente(vector)                       # Usa Merge Sort si el tamaño del vector es mayor.


# ==============================================================================
# CLASES DE NODOS PARA ÁRBOLES BINARIOS DE BÚSQUEDA
# ==============================================================================

class NodoJSON:
    """Clase que representa un nodo con estructura compatible con formato JSON."""
    def __init__(self, valor, cantidad):
        self.dato = {                                          # Inicializa el diccionario de datos del nodo.
            "valor": valor,                                    # Clave 'valor' guarda el identificador del nodo.
            "cantidad": cantidad                               # Clave 'cantidad' guarda la frecuencia del valor.
        }                                                      # Cierra el diccionario de inicialización.
        self.izquierda = None                                  # Puntero al subárbol izquierdo (menores).
        self.derecha = None                                    # Puntero al subárbol derecho (mayores).


class NodoFrecuencia:
    """Clase que representa un nodo en formato de tupla simple."""
    def __init__(self, valor, cantidad):
        self.dato = (valor, cantidad)                          # Guarda la tupla (valor, cantidad).
        self.izquierda = None                                  # Puntero izquierdo inicializado en None.
        self.derecha = None                                    # Puntero derecho inicializado en None.


class Nodo:
    """Clase que representa un nodo básico que guarda un único valor."""
    def __init__(self, valor):
        self.valor = valor                                     # Asigna el valor del nodo.
        self.izquierda = None                                  # Puntero al hijo izquierdo.
        self.derecha = None                                    # Puntero al hijo derecho.


# ==============================================================================
# ALGORITMOS DE CONSTRUCCIÓN DE ÁRBOLES EQUILIBRADOS (BST)
# ==============================================================================

def construir_arbol_json_equilibrado(lista_json, inicio, fin):
    """Construye un árbol binario equilibrado desde una lista JSON ordenada."""
    if inicio > fin:                                           # Caso base: si los límites del subvector se cruzaron.
        return None                                            # Retorna None indicando un nodo vacío.
    mitad = (inicio + fin) // 2                                # Encuentra el índice central para equilibrar la raíz.
    valor = lista_json[mitad]["valor"]                         # Obtiene el valor central.
    cantidad = lista_json[mitad]["cantidad"]                   # Obtiene la cantidad de repeticiones central.
    raiz = NodoJSON(valor, cantidad)                           # Crea el nodo raíz del subárbol.
    raiz.izquierda = construir_arbol_json_equilibrado(lista_json, inicio, mitad - 1) # Construye la rama izquierda.
    raiz.derecha = construir_arbol_json_equilibrado(lista_json, mitad + 1, fin)  # Construye la rama derecha.
    return raiz                                                # Retorna el nodo raíz del subárbol equilibrado.


def construir_arbol_frecuencias_equilibrado(tuplas, inicio, fin):
    """Construye un árbol equilibrado utilizando tuplas ordenadas de valores y frecuencias."""
    if inicio > fin:                                           # Caso base: rango vacío.
        return None                                            # Retorna None.
    mitad = (inicio + fin) // 2                                # Halla el elemento de en medio.
    valor = tuplas[mitad][0]                                   # Obtiene el valor.
    cantidad = tuplas[mitad][1]                                # Obtiene la cantidad.
    raiz = NodoFrecuencia(valor, cantidad)                     # Crea el nodo de frecuencia.
    raiz.izquierda = construir_arbol_frecuencias_equilibrado(tuplas, inicio, mitad - 1) # Construye la parte izquierda.
    raiz.derecha = construir_arbol_frecuencias_equilibrado(tuplas, mitad + 1, fin)  # Construye la parte derecha.
    return raiz                                                # Retorna la raíz del subárbol.


def construir_arbol_equilibrado(vector, inicio, fin):
    """Construye un BST equilibrado básico a partir de un vector plano de enteros ordenados."""
    if inicio > fin:                                           # Caso base: si el rango es inválido.
        return None                                            # Retorna None.
    mitad = (inicio + fin) // 2                                # Obtiene la posición central.
    raiz = Nodo(vector[mitad])                                 # Crea un nodo básico con el valor medio del vector.
    raiz.izquierda = construir_arbol_equilibrado(vector, inicio, mitad - 1) # Genera recursivamente la rama izquierda.
    raiz.derecha = construir_arbol_equilibrado(vector, mitad + 1, fin)  # Genera recursivamente la rama derecha.
    return raiz                                                # Retorna la raíz.


# ==============================================================================
# ALGORITMOS DE BÚSQUEDA Y OPERACIONES EN ÁRBOLES
# ==============================================================================

def buscar_en_arbol(raiz, buscado):
    """Busca un valor de forma binaria en un árbol binario básico."""
    if raiz is None:                                           # Si la raíz es nula, el valor no existe en la estructura.
        return False                                           # Retorna Falso.
    if hasattr(raiz, 'valor'):                                 # Verifica si el objeto tiene la propiedad 'valor'.
        valor_nodo = raiz.valor                                # Si es un Nodo simple, extrae su propiedad 'valor'.
    else:                                                      # Si no tiene propiedad 'valor'.
        valor_nodo = raiz.dato[0]                              # Asume que es una tupla y extrae el primer elemento.
    if buscado == valor_nodo:                                  # Si el valor coincide con el buscado, fue encontrado.
        return True                                            # Retorna Verdadero.
    if buscado < valor_nodo:                                   # Si es menor, continúa la búsqueda en la izquierda.
        return buscar_en_arbol(raiz.izquierda, buscado)        # Llama a la función en el hijo izquierdo.
    return buscar_en_arbol(raiz.derecha, buscado)              # Si es mayor, busca en el hijo derecho.


def buscar_en_arbol_json(raiz, buscado):
    """Busca un número de forma binaria en un árbol de estructura compatible JSON."""
    if raiz is None:                                           # Si la raíz es nula, no se encontró el elemento.
        return None                                            # Retorna None.
    valor_nodo = raiz.dato["valor"]                            # Extrae el valor del diccionario del nodo.
    if buscado == valor_nodo:                                  # Si el número coincide.
        return raiz.dato                                       # Retorna el diccionario con la información del nodo.
    if buscado < valor_nodo:                                   # Si es menor, navega a la izquierda.
        return buscar_en_arbol_json(raiz.izquierda, buscado)   # Continúa la búsqueda en la rama izquierda.
    return buscar_en_arbol_json(raiz.derecha, buscado)         # Si es mayor, continúa la búsqueda en la rama derecha.


def contar_nodos_arbol_json(raiz):
    """Cuenta todos los nodos del árbol JSON recursivamente."""
    if raiz is None:                                           # Caso base: nodo nulo no aporta al conteo.
        return 0                                               # Retorna 0.
    return 1 + contar_nodos_arbol_json(raiz.izquierda) + contar_nodos_arbol_json(raiz.derecha) # Suma 1 más los hijos.


def altura_arbol_json(raiz):
    """Calcula la altura máxima del árbol compatible JSON."""
    if raiz is None:                                           # Caso base: árbol vacío tiene altura 0.
        return 0                                               # Retorna 0.
    altura_izquierda = altura_arbol_json(raiz.izquierda)       # Calcula recursivamente la altura de la rama izquierda.
    altura_derecha = altura_arbol_json(raiz.derecha)           # Calcula recursivamente la altura de la rama derecha.
    if altura_izquierda > altura_derecha:                      # Si la rama izquierda es más profunda.
        return altura_izquierda + 1                            # Retorna la altura izquierda incrementada en 1.
    return altura_derecha + 1                                  # Retorna la altura derecha incrementada en 1.


def recorrido_inorden_json(raiz):
    """Retorna una lista con la estructura de recorrido inorden sin usar .append()."""
    if raiz is None:                                           # Caso base: si el nodo es None, retorna lista vacía.
        return []                                              # Retorna lista vacía.
    izq = recorrido_inorden_json(raiz.izquierda)               # Obtiene el recorrido del hijo izquierdo de forma recursiva.
    der = recorrido_inorden_json(raiz.derecha)                 # Obtiene el recorrido del hijo derecho de forma recursiva.
    return izq + [raiz.dato] + der                             # Retorna la suma de la lista izquierda, el dato actual y el derecho.


def buscar_en_arbol_frecuencias(raiz, buscado):
    """Busca binariamente en un árbol construido con nodos de tuplas de frecuencia."""
    if raiz is None:                                           # Caso base: si la raíz es vacía.
        return None                                            # Retorna None.
    valor_nodo = raiz.dato[0]                                  # Obtiene el valor almacenado en el primer campo de la tupla.
    if buscado == valor_nodo:                                  # Si hay coincidencia de valores.
        return raiz.dato                                       # Retorna la tupla del nodo actual.
    if buscado < valor_nodo:                                   # Si es menor, busca en el hijo izquierdo.
        return buscar_en_arbol_frecuencias(raiz.izquierda, buscado) # Llama recursivamente a la rama izquierda.
    return buscar_en_arbol_frecuencias(raiz.derecha, buscado)  # Si es mayor, busca en el hijo derecho de forma recursiva.


def contar_nodos_arbol_frecuencias(raiz):
    """Cuenta el número total de nodos de frecuencias."""
    if raiz is None:                                           # Caso base: nodo nulo.
        return 0                                               # Retorna 0.
    return 1 + contar_nodos_arbol_frecuencias(raiz.izquierda) + contar_nodos_arbol_frecuencias(raiz.derecha) # Cuenta la raíz e hijos.


def altura_arbol(raiz):
    """Calcula la altura máxima de un árbol binario básico."""
    if raiz is None:                                           # Si el nodo es nulo.
        return 0                                               # Retorna altura 0.
    altura_izq = altura_arbol(raiz.izquierda)                  # Calcula la altura de la rama izquierda.
    altura_der = altura_arbol(raiz.derecha)                    # Calcula la altura de la rama derecha.
    if altura_izq >= altura_der:                               # Si la izquierda es mayor o igual.
        return 1 + altura_izq                                  # Retorna 1 más la altura de la izquierda.
    return 1 + altura_der                                      # Retorna 1 más la altura de la derecha.


def recorrido_inorden_frecuencias(raiz):
    """Retorna una lista plana de recorrido inorden sin usar .append() ni .extend()."""
    if raiz is None:                                           # Si el nodo actual es None.
        return []                                              # Retorna lista vacía.
    izq = recorrido_inorden_frecuencias(raiz.izquierda)        # Recorrido recursivo izquierdo.
    der = recorrido_inorden_frecuencias(raiz.derecha)          # Recorrido recursivo derecho.
    return izq + [raiz.dato] + der                             # Retorna la concatenación de las partes izquierdas, el nodo y derechas.


def buscar_en_matriz(matriz, buscado):
    """Busca de forma directa si un valor entero existe dentro de la matriz."""
    for i in range(len(matriz)):                               # Recorre cada una de las filas de la matriz.
        fila = matriz[i]                                       # Obtiene la fila.
        for j in range(len(fila)):                             # Recorre cada una de las columnas.
            if fila[j] == buscado:                             # Si hay coincidencia exacta con el valor.
                return True                                    # Retorna Verdadero de inmediato.
    return False                                               # Si termina sin encontrarlo, retorna Falso.


def medir_tiempo(funcion, estructura, buscado):
    """Mide el tiempo transcurrido en nanosegundos al ejecutar una búsqueda."""
    inicio = time.perf_counter_ns()                            # Registra el tiempo de reloj en nanosegundos al iniciar.
    encontrado = funcion(estructura, buscado)                  # Ejecuta la función de búsqueda de interés.
    fin = time.perf_counter_ns()                               # Registra el tiempo en nanosegundos al finalizar.
    return encontrado, fin - inicio                            # Retorna el resultado de la búsqueda y la diferencia de tiempo.


# ==============================================================================
# DIBUJO DEL ÁRBOL EN TEXTO (REPRESENTACIÓN ASCII Y DOT DE GRAPHVIZ)
# ==============================================================================

def arbol_a_ascii(raiz):
    """Genera un dibujo ASCII del árbol binario con ramas visuales sin .append() ni .join()."""
    if raiz is None:                                           # Si el árbol está vacío.
        return "Árbol vacío"                                   # Retorna un texto descriptivo.

    def display_aux(nodo):                                     # Función auxiliar recursiva para construir las líneas.
        if nodo.izquierda is None and nodo.derecha is None:    # Si es un nodo hoja (sin hijos izquierdo ni derecho).
            if hasattr(nodo, 'dato'):                          # Verifica si almacena la información en la propiedad 'dato'.
                linea = str(nodo.dato["valor"])                # Toma el valor de dato["valor"] si aplica.
            else:                                              # Si no tiene 'dato'.
                linea = str(nodo.valor)                        # Toma la propiedad 'valor'.
            ancho = len(linea)                                 # Mide el ancho del texto generado.
            alto = 1                                           # Fija la altura del bloque en 1 línea.
            centro = ancho // 2                                # Obtiene la posición media del bloque.
            return [linea], ancho, alto, centro                # Retorna los resultados para este nodo.

        if nodo.derecha is None:                               # Si no tiene hijo derecho pero sí izquierdo.
            lineas, ancho, alto, centro = display_aux(nodo.izquierda) # Procesa recursivamente el hijo izquierdo.
            if hasattr(nodo, 'dato'):                          # Verifica 'dato'.
                valor = str(nodo.dato["valor"])                # Extrae valor del nodo.
            else:                                              # De lo contrario.
                valor = str(nodo.valor)                        # Extrae valor simple.
            ancho_valor = len(valor)                           # Mide el ancho del valor actual.
            primera = ""                                       # Construye la primera línea de la rama izquierda.
            for _ in range(centro + 1):                        # Agrega espacios en blanco a la izquierda.
                primera += " "                                 # Espacio en blanco.
            for _ in range(ancho - centro - 1):                # Agrega guiones de conexión.
                primera += "_"                                 # Carácter de conexión.
            primera += valor                                   # Concatena el valor al final.
            segunda = ""                                       # Construye la segunda línea de la rama (línea de enlace).
            for _ in range(centro):                            # Agrega espacios en blanco.
                segunda += " "                                 # Espacio.
            segunda += "/"                                     # Agrega el carácter divisor '/'.
            for _ in range(ancho - centro - 1 + ancho_valor):  # Agrega espacios de relleno.
                segunda += " "                                 # Espacio de relleno.
            lineas_movidas = []                                # Lista para alinear las líneas del hijo izquierdo.
            for idx in range(len(lineas)):                     # Recorre cada una de las líneas devueltas por el hijo.
                linea_aux = lineas[idx]                        # Obtiene la línea actual.
                relleno = ""                                   # Crea relleno de texto.
                for _ in range(ancho_valor):                   # Rellena los espacios según el tamaño del nodo padre.
                    relleno += " "                             # Espacio en blanco.
                lineas_movidas = lineas_movidas + [linea_aux + relleno] # Guarda la línea con su respectivo desfase.
            return [primera, segunda] + lineas_movidas, ancho + ancho_valor, alto + 2, ancho_valor // 2 # Retorna el bloque construido.

        if nodo.izquierda is None:                             # Si no tiene hijo izquierdo pero sí derecho.
            lineas, ancho, alto, centro = display_aux(nodo.derecha) # Procesa recursivamente el hijo derecho.
            if hasattr(nodo, 'dato'):                          # Comprueba propiedad 'dato'.
                valor = str(nodo.dato["valor"])                # Extrae el valor.
            else:                                              # De lo contrario.
                valor = str(nodo.valor)                        # Extrae el valor simple.
            ancho_valor = len(valor)                           # Mide el tamaño del string del valor.
            primera = valor                                    # Escribe el valor inicial.
            for _ in range(centro):                            # Agrega caracteres de conexión.
                primera += "_"                                 # Conexión.
            for _ in range(ancho - centro):                    # Rellena el resto de espacios.
                primera += " "                                 # Espacio de relleno.
            segunda = ""                                       # Construye la línea del enlace derecho.
            for _ in range(ancho_valor + centro):              # Rellena espacios previos.
                segunda += " "                                 # Espacio en blanco.
            segunda += "\\"                                    # Escribe el carácter divisor '\'.
            for _ in range(ancho - centro - 1):                # Rellena los espacios sobrantes.
                segunda += " "                                 # Espacio en blanco.
            lineas_movidas = []                                # Prepara desfase para las líneas de la derecha.
            for idx in range(len(lineas)):                     # Recorre las líneas.
                linea_aux = lineas[idx]                        # Extrae la línea.
                relleno = ""                                   # Inicializa relleno.
                for _ in range(ancho_valor):                   # Agrega los espacios de desfase al inicio.
                    relleno += " "                             # Espacio en blanco.
                lineas_movidas = lineas_movidas + [relleno + linea_aux] # Guarda con desfase.
            return [primera, segunda] + lineas_movidas, ancho + ancho_valor, alto + 2, ancho_valor // 2 # Retorna el bloque construido.

        izquierda, ancho_izq, alto_izq, centro_izq = display_aux(nodo.izquierda) # Procesa la rama izquierda.
        derecha, ancho_der, alto_der, centro_der = display_aux(nodo.derecha) # Procesa la rama derecha.
        if hasattr(nodo, 'dato'):                              # Obtiene valor de la raíz del subárbol.
            valor = str(nodo.dato["valor"])                    # Extrae valor.
        else:                                                  # Si es nodo plano.
            valor = str(nodo.valor)                            # Obtiene el valor.
        ancho_valor = len(valor)                               # Mide el ancho del valor.
        primera = ""                                           # Arma la línea superior (unión de ambos hijos).
        for _ in range(centro_izq + 1):                        # Espacios previos.
            primera += " "                                     # Espacio.
        for _ in range(ancho_izq - centro_izq - 1):            # Conexión izquierda.
            primera += "_"                                     # Guion bajo.
        primera += valor                                       # Escribe valor del nodo actual.
        for _ in range(centro_der):                            # Conexión derecha.
            primera += "_"                                     # Guion bajo.
        for _ in range(ancho_der - centro_der):                # Espacios posteriores.
            primera += " "                                     # Espacio en blanco.
        segunda = ""                                           # Arma la línea de enlaces.
        for _ in range(centro_izq):                            # Relleno izquierdo.
            segunda += " "                                     # Espacio.
        segunda += "/"                                         # Conector izquierdo.
        for _ in range(ancho_izq - centro_izq - 1 + ancho_valor + centro_der): # Espacios de separación central.
            segunda += " "                                     # Espacio en blanco.
        segunda += "\\"                                        # Conector derecho.
        for _ in range(ancho_der - centro_der - 1):            # Relleno derecho.
            segunda += " "                                     # Espacio.
        if alto_izq < alto_der:                                # Si la rama izquierda tiene menor altura que la derecha.
            diferencia = alto_der - alto_izq                   # Calcula cuántas líneas hacen falta para igualar.
            for _ in range(diferencia):                        # Añade líneas de espacio en blanco al final de la izquierda.
                relleno_izq = ""                               # Inicializa el relleno para esa línea.
                for _ in range(ancho_izq):                     # Agrega el ancho.
                    relleno_izq += " "                         # Relleno de espacios en blanco.
                izquierda = izquierda + [relleno_izq]          # Concatena la línea vacía al subárbol izquierdo.
        elif alto_der < alto_izq:                              # Si la derecha tiene menor altura.
            diferencia = alto_izq - alto_der                   # Calcula la diferencia.
            for _ in range(diferencia):                        # Añade relleno al final de la derecha.
                relleno_der = ""                               # Relleno.
                for _ in range(ancho_der):                     # Rellena.
                    relleno_der += " "                         # Espacio en blanco.
                derecha = derecha + [relleno_der]              # Concatena a la derecha.
        lineas = [primera, segunda]                            # Inicializa el bloque de líneas del nivel actual.
        for idx in range(len(izquierda)):                      # Itera por el índice de líneas (tienen el mismo alto).
            linea_izq = izquierda[idx]                         # Línea de la izquierda.
            linea_der = derecha[idx]                           # Línea de la derecha.
            relleno_central = ""                               # Relleno central.
            for _ in range(ancho_valor):                       # Espacios del ancho del valor del nodo.
                relleno_central += " "                         # Espacio en blanco.
            lineas = lineas + [linea_izq + relleno_central + linea_der] # Combina ambas ramas con el desfase central.
        return lineas, ancho_izq + ancho_valor + ancho_der, max(alto_izq, alto_der) + 2, ancho_izq + ancho_valor // 2 # Retorna el bloque combinado.

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
    return unir_con_delimitador(lineas_centradas, "\n")        # Une las líneas usando saltos de línea con la función manual.


def exportar_arbol_dot(raiz, nombre_grafo="Arbol"):
    """Exporta el árbol a formato DOT de Graphviz para renderizar grafos, sin usar .append() ni .join()."""
    lineas = []                                                # Inicializa la lista de líneas vacía.
    lineas = lineas + ["digraph " + str(nombre_grafo) + " {"]  # Escribe la etiqueta de inicio del grafo.
    lineas = lineas + ["    node [shape=circle];"]             # Fija la forma geométrica predeterminada de los nodos a círculos.
    contador = [0]                                             # Usa una lista de un elemento para pasar el contador por referencia.

    def recorrer(nodo):                                        # Función recursiva para escribir las relaciones.
        nonlocal lineas                                        # Permite modificar la variable 'lineas' del entorno padre.
        if nodo is None:                                       # Si el nodo actual es nulo.
            return None                                        # Retorna None.
        id_actual = contador[0]                                # Obtiene el identificador numérico único de este nodo.
        contador[0] += 1                                       # Incrementa el contador global en 1.
        if hasattr(nodo, 'dato'):                              # Si el nodo es tipo frecuencia o JSON con estructura de datos.
            if isinstance(nodo.dato, dict):                    # Si la propiedad dato es un diccionario.
                label = str(nodo.dato['valor']) + " | cant: " + str(nodo.dato['cantidad']) # Formatea el texto del nodo con su cantidad.
            else:                                              # Si es una tupla simple.
                label = str(nodo.dato[0]) + " | cant: " + str(nodo.dato[1]) # Formatea el texto extraído de la tupla.
        else:                                                  # Si es un nodo plano de valor simple.
            label = str(nodo.valor)                            # Usa el valor simple como etiqueta.
        lineas = lineas + ["    nodo" + str(id_actual) + " [label=\"" + label + "\"];"] # Genera la línea de definición del nodo en DOT.
        id_izq = recorrer(nodo.izquierda)                      # Recorre el hijo izquierdo para definir su identificador.
        if id_izq is not None:                                 # Si existe el hijo izquierdo.
            lineas = lineas + ["    nodo" + str(id_actual) + " -> nodo" + str(id_izq) + ";"] # Escribe la flecha de enlace izquierdo.
        id_der = recorrer(nodo.derecha)                        # Recorre el hijo derecho.
        if id_der is not None:                                 # Si el hijo derecho existe.
            lineas = lineas + ["    nodo" + str(id_actual) + " -> nodo" + str(id_der) + ";"] # Escribe la flecha de enlace derecho.
        return id_actual                                       # Retorna el identificador para que el padre pueda enlazarlo.

    recorrer(raiz)                                             # Llama al recorrido inicial desde la raíz del árbol.
    lineas = lineas + ["}"]                                    # Escribe la llave de cierre de la sintaxis DOT.
    return unir_con_delimitador(lineas, "\n")                  # Retorna el string DOT completo uniendo las líneas de texto.
