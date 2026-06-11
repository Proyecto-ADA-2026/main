# ==============================================================================
# LOGICA DEL PROYECTO - ALGORITMOS Y ESTRUCTURAS DE DATOS
# ==============================================================================
# Este archivo es el NUCLEO del proyecto. Contiene:
#   - Generacion y multiplicacion de matrices
#   - Clasificacion de numeros (pares, primos, perfectos, cuadrados perfectos)
#   - Algoritmos de ordenamiento propios (Insertion Sort y Merge Sort)
#   - Estructura de arbol binario de busqueda equilibrado (BST)
#   - Medicion de tiempos de busqueda
#   - Dibujo ASCII del arbol
# RESTRICCION ACADEMICA: No se usa .append(), .join(), sorted(), ni librerias
# de algebra lineal. Todo se construye manualmente con for/while y concatenacion.
# ==============================================================================


# ==============================================================================
# IMPORTACIONES
# ==============================================================================

import random      # Modulo estandar para generar numeros pseudoaleatorios.
import time        # Modulo estandar para medir tiempo en nanosegundos.


# ==============================================================================
# FUNCIONES AUXILIARES DE TEXTO
# ==============================================================================


def unir_con_delimitador(lista, delimitador):
    """Une todos los elementos de una lista en un solo string con un separador.

    Sustituye manualmente a ''.join(lista) sin usar ese metodo incorporado.
    Ejemplo: unir_con_delimitador(["a","b","c"], "-") => "a-b-c"
    """
    resultado = ""                              # Acumulador que va creciendo con cada elemento.
    for i in range(len(lista)):                 # Recorre por indice para saber cuando es el ultimo.
        resultado += str(lista[i])              # Convierte el elemento a texto antes de concatenar.
        if i < len(lista) - 1:                  # Solo agrega el delimitador si NO es el ultimo.
            resultado += delimitador            # Evita poner delimitador al final ("a-b-c" no "a-b-c-").
    return resultado                            # Devuelve el texto completamente armado.


# ==============================================================================
# FUNCIONES PARA MATRICES
# ==============================================================================


def crear_matriz(n):
    """Genera una matriz cuadrada de n x n con valores enteros aleatorios entre 0 y 9.

    No usa .append(); en su lugar hace lista = lista + [nuevo_elemento].
    Esa restriccion es academica: demuestra que se entiende como funciona append
    por debajo (concatenar una lista de un elemento al acumulador).
    """
    matriz = []                                 # Lista de listas; cada sublista sera una fila.
    for _ in range(n):                          # Crea exactamente n filas.
        fila = []                               # Cada iteracion crea una fila nueva y vacia.
        for _ in range(n):                      # Llena la fila con n valores, uno por columna.
            valor = random.randint(0, 9)        # Entero aleatorio en [0, 9] (ambos inclusive).
            fila = fila + [valor]               # Equivale a fila.append(valor) pero manual.
        matriz = matriz + [fila]                # Agrega la fila completa como un elemento de la matriz.
    return matriz                               # Retorna la lista de listas n x n.


def guardar_matriz_directo_txt(n, nombre_archivo="matriz.txt"):
    """Genera una matriz fila por fila y la escribe en TXT sin guardar todo en RAM.

    Util para matrices muy grandes donde almacenar n*n enteros consumiria mucha memoria.
    Se genera un valor, se escribe, y se descarta; no se acumula la matriz completa.
    """
    with open(nombre_archivo, "w", encoding="utf-8") as archivo: # Abre (o crea) el archivo para escritura.
        archivo.write("Matriz generada de tamaño " + str(n) + " x " + str(n) + "\n")
        linea_separadora = ""                  # Construye "===...===" manualmente (60 caracteres).
        for _ in range(60):
            linea_separadora += "="
        archivo.write(linea_separadora + "\n\n")
        for i in range(n):                     # Una iteracion = una fila de la matriz.
            fila = []                          # Solo guarda los valores de ESTA fila como texto.
            for j in range(n):                 # Genera y almacena cada celda de la fila.
                valor = random.randint(0, 9)
                fila = fila + [str(valor)]     # Guarda como string para escribirlo directamente.
            linea_texto = ""                   # Construye la fila formateada con ancho fijo.
            for k in range(len(fila)):
                formateado = ""
                num_str = fila[k]
                espacios = 10 - len(num_str)   # Calcula cuantos espacios hacen falta para ancho=10.
                formateado += num_str
                for _ in range(espacios):
                    formateado += " "          # Rellena con espacios para alinear columnas.
                linea_texto += formateado
                if k < len(fila) - 1:
                   linea_texto += "   "        # Separacion visual entre columnas.
            archivo.write(linea_texto + "\n")
            if i % 100 == 0:                   # Informa progreso cada 100 filas.
                print("Generando fila " + str(i) + " de " + str(n) + "...")
    print("Matriz guardada correctamente en " + str(nombre_archivo))


def multiplicar_matrices(x, y):
    """Multiplica dos matrices cuadradas x e y de tamaño n x n.

    Algoritmo clasico O(n^3): para cada celda (i, j) del resultado calcula
    el producto punto entre la fila i de x y la columna j de y.

    TRUCO DE OPTIMIZACION: primero se TRANSPONE y para convertir sus columnas
    en filas. Asi, el acceso a columnas se convierte en acceso a filas, lo cual
    es mas eficiente en memoria (los datos de una fila estan contiguos en RAM).
    Sin transponer, acceder a la columna j de y requiere saltar de fila en fila.
    """
    n = len(x)                                  # Dimension de las matrices (son cuadradas, n x n).
    y_transpuesta = []                          # Almacenara las columnas de y como filas.
    for j in range(n):                          # Recorre cada columna j de y.
        columna = []                            # Acumula todos los elementos de la columna j.
        for i in range(n):                      # Recorre las filas de y para extraer columna j.
            columna = columna + [y[i][j]]       # y[i][j] es el elemento en fila i, columna j.
        y_transpuesta = y_transpuesta + [columna] # La columna j de y queda como fila j en la transpuesta.
    resultado = []                              # Matriz resultado de la multiplicacion.
    for i in range(n):                          # Para cada fila i del resultado (= fila i de x).
        fila_resultado = []                     # Acumula los n valores de la fila i del resultado.
        for j in range(n):                      # Para cada columna j del resultado.
            columna_y = y_transpuesta[j]        # Toma la columna j de y (ya como fila por la transpuesta).
            suma = 0                            # Acumula el producto punto entre fila i de x y columna j de y.
            for k in range(n):                  # Multiplica elemento a elemento y suma (producto escalar).
                suma += x[i][k] * columna_y[k]  # x[i][k] * y[k][j] en la notacion clasica.
            fila_resultado = fila_resultado + [suma] # El valor calculado es el (i, j) del resultado.
        resultado = resultado + [fila_resultado] # Agrega la fila completa al resultado.
    return resultado                            # Devuelve la matriz producto x * y.


def guardar_A3_directo_txt(matriz_A, nombre_archivo="matriz_A3.txt"):
    """Calcula A^3 = A*A*A y escribe el resultado en TXT fila por fila.

    Diferencia con guardar_matriz_directo_txt: aqui SI se necesita A3 completa
    en RAM para los algoritmos posteriores, por eso se retorna A3.
    El guardado a disco es adicional, para permitir abrir el archivo.
    """
    n = len(matriz_A)                           # Dimension de A.
    A2 = multiplicar_matrices(matriz_A, matriz_A) # Primer paso: A2 = A * A.
    A3 = multiplicar_matrices(A2, matriz_A)     # Segundo paso: A3 = A2 * A = A^3.
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("Matriz A³ de tamaño " + str(n) + " x " + str(n) + "\n")
        linea_separadora = ""
        for _ in range(60):
            linea_separadora += "="
        archivo.write(linea_separadora + "\n\n")
        for i in range(len(A3)):               # Escribe fila por fila de A3.
            fila = A3[i]
            linea_texto = ""
            for k in range(len(fila)):
                num_str = str(fila[k])
                espacios = 10 - len(num_str)   # Los valores de A3 pueden tener varios digitos.
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
    return A3                                   # Retorna A3 para usarla en los algoritmos siguientes.


def calcular_A3(A):
    """Calcula A^3 usando dos multiplicaciones de matrices (sin guardar en disco).

    Se usa en flujos donde solo se necesita el resultado en memoria.
    A^3 requiere dos productos porque la exponenciacion de matrices se hace
    multiplicacion a multiplicacion: A^3 = (A^2) * A.
    """
    A2 = multiplicar_matrices(A, A)             # Paso 1: calcula A al cuadrado.
    A3 = multiplicar_matrices(A2, A)            # Paso 2: multiplica A^2 por A para obtener A^3.
    return A3                                   # Retorna la matriz elevada al cubo.


# ==============================================================================
# FUNCIONES DE ANALISIS NUMERICO
# ==============================================================================


def es_primo(numero):
    """Determina si un numero entero es primo.

    DEFINICION: Un numero es primo si solo es divisible por 1 y por si mismo.
    OPTIMIZACION CLAVE: Solo se prueban divisores hasta la raiz cuadrada del numero.
    Razon: si numero = a * b y a <= b, entonces a <= sqrt(numero). Si no hay
    ningun divisor hasta sqrt(numero), tampoco lo habra por encima.
    Esto reduce el costo de O(n) a O(sqrt(n)).
    """
    if numero < 2:                              # 0 y 1 NO son primos por definicion matematica.
        return False
    divisor = 2                                 # El menor divisor primo posible.
    while divisor * divisor <= numero:          # Prueba hasta raiz cuadrada (sin calcular math.sqrt).
        if numero % divisor == 0:               # Si divide exactamente (sin residuo), no es primo.
            return False
        divisor += 1                            # Prueba el siguiente candidato a divisor.
    return True                                 # Ningun divisor encontrado => es primo.


def es_perfecto(numero):
    """Determina si un numero es perfecto.

    DEFINICION: Un numero es perfecto si la suma de todos sus divisores propios
    (todos los divisores excepto el mismo) es igual al numero.
    Ejemplo: 6 = 1 + 2 + 3 (divisores de 6 sin contar el 6), entonces 6 es perfecto.
    Otros numeros perfectos: 28, 496, 8128.

    OPTIMIZACION: Como en es_primo, solo se prueban divisores hasta sqrt(numero).
    Para cada divisor d encontrado se suma tambien su complemento numero/d,
    evitando recorrer la segunda mitad del rango.
    """
    if numero <= 1:                             # 0 y 1 no son perfectos (por convencion matematica).
        return False
    suma_divisores = 1                          # Se empieza en 1 porque 1 siempre es divisor propio.
    divisor = 2                                 # Comienza a buscar divisores desde 2.
    while divisor * divisor <= numero:          # Solo hasta la raiz cuadrada.
        if numero % divisor == 0:               # Se encontro un divisor exacto.
            suma_divisores += divisor           # Suma el divisor menor (ej: 2 en el caso de 28).
            otro_divisor = numero // divisor    # Calcula el complemento (ej: 14 = 28 // 2).
            if otro_divisor != divisor:         # Evita contar el mismo divisor dos veces cuando numero = d^2.
                suma_divisores += otro_divisor  # Suma el divisor complementario.
        divisor += 1
    return suma_divisores == numero             # Es perfecto si la suma de divisores propios iguala al numero.


def es_cuadrado_perfecto(numero):
    """Determina si un numero es un cuadrado perfecto (existe un entero k tal que k*k == numero).

    Ejemplos: 0, 1, 4, 9, 16, 25...

    ALGORITMO: Busqueda binaria sobre el rango [1, numero].
    En cada paso se prueba si la mitad del rango al cuadrado es igual al numero.
    - Si mitad^2 == numero: encontrado.
    - Si mitad^2 < numero: la raiz esta a la derecha, se mueve el limite izquierdo.
    - Si mitad^2 > numero: la raiz esta a la izquierda, se mueve el limite derecho.
    Costo: O(log n) en lugar de O(sqrt(n)) con busqueda lineal.
    """
    if numero < 0:                              # Los negativos no tienen raiz cuadrada real entera.
        return False
    if numero == 0 or numero == 1:              # Casos base triviales: 0^2=0 y 1^2=1.
        return True
    izquierda = 1                               # Extremo inferior del rango de busqueda.
    derecha = numero                            # Extremo superior (la raiz no puede ser mayor que numero).
    while izquierda <= derecha:                 # Mientras el rango tenga al menos un candidato.
        mitad = (izquierda + derecha) // 2      # Candidato central del rango actual.
        cuadrado = mitad * mitad                # Se calcula el cuadrado del candidato.
        if cuadrado == numero:                  # El candidato es exactamente la raiz entera.
            return True
        if cuadrado < numero:                   # El candidato es muy pequeno, busca a la derecha.
            izquierda = mitad + 1
        else:                                   # El candidato es muy grande, busca a la izquierda.
            derecha = mitad - 1
    return False                                # No existe entero k tal que k*k == numero.


def analizar_matriz(matriz):
    """Clasifica todos los elementos de la matriz en 5 categorias numericas.

    Categorias: pares, impares, primos, perfectos, cuadrados perfectos.
    Un mismo valor puede estar en varias categorias (ej: 4 es par Y cuadrado perfecto).

    OPTIMIZACION CON CACHE: La matriz puede tener valores repetidos (0-9).
    Sin cache, se recalcularian las propiedades del mismo numero miles de veces.
    Con cache (diccionario), cada valor se analiza UNA SOLA VEZ y se reutiliza.
    """
    pares = []                                  # Acumula todos los valores pares (con repeticion).
    impares = []                                # Acumula todos los valores impares (con repeticion).
    primos = []                                 # Acumula todos los valores primos encontrados.
    perfectos = []                              # Acumula todos los valores perfectos encontrados.
    cuadrados = []                              # Acumula todos los cuadrados perfectos encontrados.
    cache = {}                                  # Diccionario valor -> dict de propiedades ya calculadas.
    for i in range(len(matriz)):                # Recorre filas por indice (no usa for fila in matriz).
        fila = matriz[i]                        # Fila actual de la matriz.
        for j in range(len(fila)):              # Recorre columnas por indice.
            valor = fila[j]                     # Valor de la celda (i, j).
            if valor in cache:                  # Si ya se analizo este valor, reutiliza el resultado.
                datos = cache[valor]            # Evita llamar es_primo, es_perfecto, etc. de nuevo.
            else:
                datos = {                       # Primera vez que aparece este valor: calcula todo.
                    "par": valor % 2 == 0,      # True si el residuo de dividir entre 2 es 0.
                    "primo": es_primo(valor),   # Llama a la funcion de verificacion de primo.
                    "perfecto": es_perfecto(valor),      # Llama a la funcion de numero perfecto.
                    "cuadrado": es_cuadrado_perfecto(valor) # Llama a la funcion de cuadrado perfecto.
                }
                cache[valor] = datos            # Guarda el resultado para no recalcular.
            if datos["par"]:                    # Clasifica: par o impar (son mutuamente excluyentes).
                pares = pares + [valor]
            else:
                impares = impares + [valor]
            if datos["primo"]:                  # No es excluyente con par/impar (2 es primo y par).
                primos = primos + [valor]
            if datos["perfecto"]:               # Un numero puede ser primo Y perfecto? No en la practica.
                perfectos = perfectos + [valor]
            if datos["cuadrado"]:               # Cuadrado perfecto tampoco es excluyente (4 es par y cuadrado).
                cuadrados = cuadrados + [valor]
    return {                                    # Retorna un diccionario con cantidades y listas por categoria.
        "pares":     {"cantidad": len(pares),     "valores": pares},
        "impares":   {"cantidad": len(impares),   "valores": impares},
        "primos":    {"cantidad": len(primos),    "valores": primos},
        "perfectos": {"cantidad": len(perfectos), "valores": perfectos},
        "cuadrados": {"cantidad": len(cuadrados), "valores": cuadrados}
    }


def contar_repeticiones(matriz):
    """Cuenta cuantas veces aparece cada valor distinto en la matriz.

    Construye una tabla de frecuencias (diccionario valor -> cantidad).
    Esta tabla se usa luego para construir el BST: cada nodo del arbol
    representa un valor unico y guarda su frecuencia.
    """
    frecuencias = {}                            # Diccionario {valor: cantidad_de_apariciones}.
    for i in range(len(matriz)):                # Recorre filas.
        fila = matriz[i]
        for j in range(len(fila)):              # Recorre columnas.
            valor = fila[j]                     # Valor de la celda actual.
            if valor in frecuencias:            # Si ya aparecio antes, incrementa el contador.
                frecuencias[valor] += 1
            else:
                frecuencias[valor] = 1          # Primera aparicion: inicializa el contador en 1.
    return frecuencias                          # Retorna la tabla completa de frecuencias.


def buscar_y_contar_en_matriz(matriz, buscado):
    """Realiza busqueda secuencial (lineal) en la matriz.

    Costo: O(n^2) en el peor caso (recorre todas las celdas).
    Compara con la busqueda en arbol que cuesta O(log u) donde u = valores unicos.
    Retorna una tupla: (encontrado: bool, cantidad: int).
    """
    encontrado = False                          # Bandera: se vuelve True en la primera coincidencia.
    cantidad = 0                                # Contador de cuantas veces aparece buscado.
    for i in range(len(matriz)):                # Recorre todas las filas sin poder saltar.
        fila = matriz[i]
        for j in range(len(fila)):              # Recorre todas las columnas.
            valor = fila[j]
            if valor == buscado:                # Coincidencia con el numero pedido.
                encontrado = True               # Marca que existe al menos una vez.
                cantidad += 1                   # Suma esta aparicion al conteo total.
    return encontrado, cantidad                 # Devuelve si existe y cuantas veces.


# ==============================================================================
# FUNCIONES DE FRECUENCIAS Y VECTORES
# ==============================================================================


def frecuencias_a_json_ordenado(frecuencias):
    """Convierte la tabla de frecuencias a una lista de dicts ordenada por valor.

    La lista resultante tiene el formato:
        [{"valor": 0, "cantidad": 5}, {"valor": 1, "cantidad": 3}, ...]
    Esta lista ORDENADA es el insumo para construir el BST equilibrado:
    si los datos ya estan ordenados, se puede tomar el elemento del medio
    como raiz y garantizar balance con division binaria recursiva.
    """
    claves = []                                  # Lista con todos los valores unicos del diccionario.
    for clave in frecuencias:                    # Itera sobre las claves del diccionario.
        claves = claves + [clave]                # Agrega sin .append().
    claves_ordenadas = ordenar_ascendente(claves) # Ordena los valores de menor a mayor.
    lista_json = []                              # Lista final en el formato requerido por NodoJSON.
    for i in range(len(claves_ordenadas)):
        clave = claves_ordenadas[i]
        dato = {                                 # Cada elemento tiene el valor y su frecuencia.
            "valor": clave,
            "cantidad": frecuencias[clave]       # Frecuencia leida del diccionario original.
        }
        lista_json = lista_json + [dato]
    return lista_json                            # Lista ordenada lista para construir el arbol.


def matriz_a_vector(matriz):
    """Aplana una matriz n x n en un vector unidimensional de n^2 elementos.

    Orden de lectura: fila 0 completa, luego fila 1, etc. (orden fila-mayor).
    El vector resultante se usa para aplicar algoritmos de ordenamiento.
    """
    vector = []                                  # Acumulador lineal de todos los elementos.
    for i in range(len(matriz)):                 # Recorre filas.
        fila = matriz[i]
        for j in range(len(fila)):               # Recorre columnas de la fila actual.
            vector = vector + [fila[j]]          # Agrega cada elemento al final del vector.
    return vector                                # Vector de n*n elementos.


# ==============================================================================
# FUNCIONES DE ORDENAMIENTO
# ==============================================================================


def insertion_sort_ascendente(vector):
    """Ordena un vector de menor a mayor usando Insertion Sort (Ordenamiento por Insercion).

    IDEA: Mantiene un sub-arreglo izquierdo ya ordenado. En cada paso toma el
    siguiente elemento (actual) y lo inserta en la posicion correcta del sub-arreglo
    desplazando hacia la derecha los elementos mayores.

    COMPLEJIDAD:
      - Mejor caso O(n): vector ya ordenado, no hay desplazamientos.
      - Peor caso O(n^2): vector invertido, cada elemento se desplaza hasta el inicio.

    POR QUE SE USA PARA VECTORES PEQUENOS (<=64 elementos):
      Insertion Sort tiene muy bajo overhead de llamadas recursivas y aprovecha
      bien la cache de CPU para datos pequenos, superando a Merge Sort en la practica.
    """
    for i in range(1, len(vector)):              # Empieza en indice 1; el elemento 0 ya forma un sub-arreglo ordenado de 1.
        actual = vector[i]                       # Elemento que se va a insertar en la posicion correcta.
        j = i - 1                                # Empieza a comparar con el elemento inmediatamente anterior.
        while j >= 0 and vector[j] > actual:     # Mientras haya elementos a la izquierda mayores que actual:
            vector[j + 1] = vector[j]            # Desplaza el elemento mayor una posicion a la derecha.
            j -= 1                               # Retrocede para comparar con el elemento anterior.
        vector[j + 1] = actual                   # Inserta actual en el hueco que quedo tras los desplazamientos.
    return vector                                # El mismo vector ya ordenado (in-place).


def invertir_vector(vector):
    """Invierte el orden de un vector sin usar reversed(), [::-1] ni .reverse().

    Se construye un nuevo vector recorriendo el original de atras hacia adelante.
    Usado para obtener el orden descendente: primero se ordena ascendente
    con insertion/merge sort y luego se invierte el resultado.
    """
    invertido = []                               # Nuevo vector que tendra los elementos en orden opuesto.
    for i in range(len(vector) - 1, -1, -1):     # Recorre desde el ultimo indice (len-1) hasta el 0, inclusive.
        invertido = invertido + [vector[i]]      # Agrega cada elemento al nuevo vector en orden inverso.
    return invertido                             # Vector con el mismo contenido pero al reves.


def merge_sort_ascendente(vector):
    """Ordena un vector usando Merge Sort (Ordenamiento por Mezcla).

    IDEA (Divide y Conquista):
      1. DIVIDE: parte el vector en dos mitades.
      2. CONQUISTA: ordena recursivamente cada mitad.
      3. COMBINA: mezcla las dos mitades ya ordenadas en un solo vector ordenado.

    COMPLEJIDAD: O(n log n) en todos los casos (mejor, promedio y peor).
    POR QUE MEJOR QUE INSERTION SORT PARA n > 64:
      Para n grande, O(n log n) crece mucho mas lentamente que O(n^2).
    """
    if len(vector) <= 1:                         # Caso base: un vector de 0 o 1 elemento ya esta ordenado.
        return vector
    medio = len(vector) // 2                     # Punto de corte: division entera para partir en dos.
    izquierda = merge_sort_ascendente(vector[:medio]) # Ordena recursivamente la primera mitad.
    derecha = merge_sort_ascendente(vector[medio:])   # Ordena recursivamente la segunda mitad.
    # ---- FASE DE MEZCLA (MERGE): combina dos listas ya ordenadas en una ----
    resultado = []                               # Acumulador de la lista mezclada y ordenada.
    i = 0                                        # Indice que avanza sobre la mitad izquierda.
    j = 0                                        # Indice que avanza sobre la mitad derecha.
    while i < len(izquierda) and j < len(derecha): # Mientras AMBAS mitades tengan elementos sin procesar:
        if izquierda[i] <= derecha[j]:           # El elemento de la izquierda es menor o igual.
            resultado = resultado + [izquierda[i]] # Se elige el de la izquierda (mantiene estabilidad con <=).
            i += 1                               # Avanza el puntero de la izquierda.
        else:                                    # El elemento de la derecha es menor.
            resultado = resultado + [derecha[j]]
            j += 1                               # Avanza el puntero de la derecha.
    while i < len(izquierda):                    # La derecha se agoto; copia los sobrantes de la izquierda.
        resultado = resultado + [izquierda[i]]
        i += 1
    while j < len(derecha):                      # La izquierda se agoto; copia los sobrantes de la derecha.
        resultado = resultado + [derecha[j]]
        j += 1
    return resultado                             # Vector completamente ordenado de menor a mayor.


def ordenar_ascendente(vector):
    """Selecciona el algoritmo de ordenamiento optimo segun el tamaño del vector.

    Para vectores pequeños (hasta 64 elementos): Insertion Sort.
      - Menor overhead de memoria y llamadas recursivas.
      - Mejor uso del cache de CPU para pocos datos.
    Para vectores grandes (mas de 64 elementos): Merge Sort.
      - Garantia O(n log n) vs O(n^2) de insertion sort en el peor caso.

    El umbral de 64 es un valor practico estandar en implementaciones reales
    (por ejemplo, Python usa Timsort que tambien alterna entre ambos).
    """
    if len(vector) <= 64:                        # Umbral empírico donde insertion sort es mas rapido.
        return insertion_sort_ascendente(vector)
    return merge_sort_ascendente(vector)         # Para entradas grandes, merge sort garantiza O(n log n).


# ==============================================================================
# CLASES DE NODOS PARA EL ARBOL BINARIO DE BUSQUEDA
# ==============================================================================

class NodoJSON:
    """Nodo del arbol binario de busqueda (BST) con estructura compatible JSON.

    Cada nodo almacena:
      - dato: diccionario con "valor" (numero unico) y "cantidad" (frecuencia en la matriz).
      - izquierda: referencia al hijo izquierdo (valores menores).
      - derecha: referencia al hijo derecho (valores mayores).

    La estructura de dato como diccionario (en lugar de atributos directos) facilita
    la serializacion a JSON manual sin usar json.dump.
    """

    def __init__(self, valor, cantidad):
        self.dato = {                            # Diccionario que se mapea directamente a objeto JSON.
            "valor": valor,                      # El numero que representa este nodo (clave de busqueda).
            "cantidad": cantidad                 # Cuantas veces aparecio ese numero en la matriz.
        }
        self.izquierda = None                    # Hijo izquierdo: valores menores que self.dato["valor"].
        self.derecha = None                      # Hijo derecho: valores mayores que self.dato["valor"].


# ==============================================================================
# ARBOLES BINARIOS DE BUSQUEDA EQUILIBRADOS
# ==============================================================================


def construir_arbol_json_equilibrado(lista_json, inicio, fin):
    """Construye un BST equilibrado a partir de una lista ORDENADA de dicts.

    ALGORITMO (recursivo, similar a busqueda binaria al reves):
      - Toma el elemento del MEDIO de la sublista [inicio, fin] como raiz.
      - Construye recursivamente el subarbol izquierdo con la mitad inferior.
      - Construye recursivamente el subarbol derecho con la mitad superior.

    POR QUE GARANTIZA BALANCE:
      Al elegir siempre el elemento central, ambos subarboles tendran igual
      (o casi igual) cantidad de nodos. La altura del arbol sera O(log n)
      en lugar de O(n) que ocurriria si se insertaran en orden.

    PARAMETROS:
      lista_json: lista de {"valor": ..., "cantidad": ...} ORDENADA por valor.
      inicio: indice del primer elemento a considerar en esta llamada.
      fin: indice del ultimo elemento a considerar en esta llamada.
    """
    if inicio > fin:                             # Caso base: rango vacio, no hay nodo que crear.
        return None
    mitad = (inicio + fin) // 2                  # Indice central: sera la raiz de este subarbol.
    valor = lista_json[mitad]["valor"]           # Valor numerico del nodo central.
    cantidad = lista_json[mitad]["cantidad"]     # Frecuencia del valor en la matriz.
    raiz = NodoJSON(valor, cantidad)             # Crea el nodo raiz del subarbol actual.
    raiz.izquierda = construir_arbol_json_equilibrado(lista_json, inicio, mitad - 1) # Sub-arbol con valores menores.
    raiz.derecha = construir_arbol_json_equilibrado(lista_json, mitad + 1, fin)      # Sub-arbol con valores mayores.
    return raiz                                  # Retorna la raiz del subarbol construido.


# ==============================================================================
# ALGORITMOS DE BUSQUEDA Y OPERACIONES EN ARBOLES
# ==============================================================================


def buscar_en_arbol_json(raiz, buscado):
    """Busqueda binaria en el BST: O(log n) en arbol equilibrado.

    ALGORITMO:
      - Si el nodo actual es None: el valor no existe en el arbol.
      - Si buscado == valor del nodo: encontrado, retorna el dict del nodo.
      - Si buscado < valor: busca en el subarbol IZQUIERDO (valores menores).
      - Si buscado > valor: busca en el subarbol DERECHO (valores mayores).

    La propiedad del BST garantiza que en cada paso se descarta la mitad
    del arbol restante, igual que la busqueda binaria en una lista ordenada.
    """
    if raiz is None:                             # Caso base: se llego a una hoja sin encontrar el valor.
        return None
    valor_nodo = raiz.dato["valor"]              # Valor almacenado en el nodo actual.
    if buscado == valor_nodo:                    # COINCIDENCIA: se encontro el numero.
        return raiz.dato                         # Retorna el dict {"valor": ..., "cantidad": ...}.
    if buscado < valor_nodo:                     # El buscado es menor: debe estar en la rama izquierda.
        return buscar_en_arbol_json(raiz.izquierda, buscado)
    return buscar_en_arbol_json(raiz.derecha, buscado) # El buscado es mayor: rama derecha.


def contar_nodos_arbol_json(raiz):
    """Cuenta el total de nodos del arbol usando recursion posorden.

    Para cada nodo: total = 1 (nodo actual) + nodos de subarbol izq + nodos de subarbol der.
    Caso base: arbol vacio tiene 0 nodos.
    """
    if raiz is None:                             # Arbol o subarbol vacio aporta cero nodos.
        return 0
    return 1 + contar_nodos_arbol_json(raiz.izquierda) + contar_nodos_arbol_json(raiz.derecha)


def altura_arbol_json(raiz):
    """Calcula la altura del arbol (numero de niveles).

    DEFINICION: La altura de un arbol es la longitud del camino mas largo
    desde la raiz hasta una hoja.
    - Un arbol vacio tiene altura 0.
    - Un arbol de un solo nodo tiene altura 1.
    - Se toma el maximo entre la altura izquierda y la derecha, mas 1 (el nodo actual).
    """
    if raiz is None:                             # Arbol vacio: altura cero.
        return 0
    altura_izquierda = altura_arbol_json(raiz.izquierda) # Desciende recursivamente por la izquierda.
    altura_derecha = altura_arbol_json(raiz.derecha)     # Desciende recursivamente por la derecha.
    if altura_izquierda > altura_derecha:        # Toma la rama mas larga (sin usar max()).
        return altura_izquierda + 1
    return altura_derecha + 1                    # +1 cuenta el nodo actual.


def recorrido_inorden_json(raiz):
    """Recorre el arbol en inorden: izquierda -> raiz -> derecha.

    PROPIEDAD IMPORTANTE del BST: el recorrido inorden siempre produce
    los valores en ORDEN ASCENDENTE. Esto sirve para verificar que el
    arbol esta correctamente construido.

    Retorna una lista de dicts {"valor": ..., "cantidad": ...} en orden.
    """
    if raiz is None:                             # Caso base: subarbol vacio aporta lista vacia.
        return []
    izq = recorrido_inorden_json(raiz.izquierda) # Primero visita todos los valores MENORES.
    der = recorrido_inorden_json(raiz.derecha)   # Luego visita todos los valores MAYORES.
    return izq + [raiz.dato] + der               # Concatena: menores + nodo_actual + mayores.


def contar_elementos_representados_arbol(raiz):
    """Suma las frecuencias de todos los nodos del arbol.

    El arbol de frecuencias no guarda cada elemento de la matriz como un nodo
    separado; en cambio, cada nodo guarda el CONTEO de apariciones.
    Esta funcion suma todos esos conteos para verificar que el total coincide
    con n*n (todos los elementos de la matriz estan representados).
    """
    if raiz is None:                             # Sin nodo no hay elementos que contar.
        return 0
    cantidad_actual = raiz.dato["cantidad"]      # Frecuencia almacenada en el nodo actual.
    izquierda = contar_elementos_representados_arbol(raiz.izquierda) # Suma recursiva por la izquierda.
    derecha = contar_elementos_representados_arbol(raiz.derecha)     # Suma recursiva por la derecha.
    return cantidad_actual + izquierda + derecha # Total: este nodo + todos los subarboles.


def buscar_en_matriz(matriz, buscado):
    """Busqueda secuencial simple en la matriz (version sin conteo).

    Retorna True en la primera coincidencia encontrada para ser eficiente
    cuando solo se necesita saber si el valor existe (no cuantas veces).
    Costo: O(n^2) peor caso.
    """
    for i in range(len(matriz)):                 # Recorre todas las filas.
        fila = matriz[i]
        for j in range(len(fila)):               # Recorre todas las columnas.
            if fila[j] == buscado:               # Primera coincidencia.
                return True                      # Retorno anticipado: no sigue buscando.
    return False                                 # Recorrio toda la matriz sin encontrar el valor.


# ==============================================================================
# MEDICION DE TIEMPOS
# ==============================================================================


def medir_tiempo(funcion, estructura, buscado):
    """Mide el tiempo de UNA ejecucion de la funcion de busqueda en nanosegundos.

    Usa time.perf_counter_ns() que tiene resolucion de nanosegundos y es el
    reloj mas preciso disponible en Python para microbenchmarks.
    """
    inicio = time.perf_counter_ns()              # Marca de tiempo antes de la busqueda.
    encontrado = funcion(estructura, buscado)    # Ejecuta la funcion recibida como parametro.
    fin = time.perf_counter_ns()                 # Marca de tiempo despues de la busqueda.
    return encontrado, fin - inicio              # Tupla: (resultado, duracion en nanosegundos).


def medir_tiempo_promedio(funcion, estructura, buscado, repeticiones=1000):
    """Mide el tiempo promedio de una busqueda ejecutandola multiples veces.

    POR QUE PROMEDIAR:
      Una sola medicion es ruidosa (el SO puede interrumpir el proceso, el
      cache de CPU puede estar frio, etc.). Con 1000 repeticiones los picos
      se suavizan y el promedio es representativo del costo real del algoritmo.

    Retorna: (ultimo_resultado_funcional, tiempo_promedio_en_nanosegundos).
    """
    tiempo_total = 0                             # Acumula la duracion total de todas las repeticiones.
    resultado = None                             # Guarda el resultado de la busqueda (sera el mismo siempre).

    for _ in range(repeticiones):                # Ejecuta la busqueda el numero de veces indicado.
        inicio = time.perf_counter_ns()
        resultado = funcion(estructura, buscado)
        fin = time.perf_counter_ns()
        tiempo_total += fin - inicio             # Suma la duracion de esta ejecucion al total.

    promedio = tiempo_total / repeticiones       # Promedio aritmetico de todos los tiempos.
    return resultado, promedio                   # Devuelve el resultado funcional y el tiempo promedio.


# ==============================================================================
# DIBUJO DEL ARBOL EN TEXTO ASCII
# ==============================================================================


def arbol_a_ascii(raiz):
    """Genera una representacion ASCII del arbol binario con ramas / y \\.

    IDEA GENERAL DEL ALGORITMO (funcion interna display_aux):
      Para dibujar el arbol se necesita conocer el ancho total de cada subarbol
      para alinear el nodo padre exactamente sobre sus hijos.
      display_aux retorna para cada subarbol:
        - lineas: lista de strings, cada uno es una linea del dibujo.
        - ancho: ancho total en caracteres del bloque del subarbol.
        - alto: numero de lineas del bloque.
        - centro: posicion horizontal (columna) de la raiz dentro del bloque.

      Con esa informacion se puede:
        1. Dibujar el nodo padre centrado sobre sus hijos.
        2. Dibujar las ramas / y \\ conectando padre con hijos.
        3. Unir los bloques izquierdo y derecho horizontalmente.
    """
    if raiz is None:                             # No hay arbol que dibujar.
        return "Árbol vacío"

    def display_aux(nodo):
        """Construye recursivamente el bloque ASCII de texto de un subarbol.

        Retorna: (lineas, ancho, alto, centro)
          - lineas: lista de strings de igual longitud que forman el dibujo del subarbol.
          - ancho: longitud de cada string en lineas.
          - alto: len(lineas).
          - centro: indice de columna donde esta la raiz del subarbol dentro del bloque.
        """
        # --- CASO BASE: NODO HOJA (sin hijos) ---
        if nodo.izquierda is None and nodo.derecha is None:
            if hasattr(nodo, 'dato'):             # NodoJSON guarda el valor dentro de un dict.
                linea = str(nodo.dato["valor"])
            else:
                linea = str(nodo.valor)           # Compatibilidad con otros tipos de nodo.
            ancho = len(linea)                    # El bloque tiene el ancho exacto del texto del nodo.
            alto = 1                              # Una hoja ocupa exactamente una linea.
            centro = ancho // 2                   # El centro visual es la mitad del texto.
            return [linea], ancho, alto, centro

        # --- CASO: SOLO HIJO IZQUIERDO (sin hijo derecho) ---
        if nodo.derecha is None:
            lineas, ancho, alto, centro = display_aux(nodo.izquierda)  # Dibuja el subarbol izquierdo.
            if hasattr(nodo, 'dato'):
                valor = str(nodo.dato["valor"])
            else:
                valor = str(nodo.valor)
            ancho_valor = len(valor)
            # Primera linea: espacios + guiones hasta el nodo + texto del nodo.
            primera = ""
            for _ in range(centro + 1):           # Espacios hasta donde sale la rama izquierda.
                primera += " "
            for _ in range(ancho - centro - 1):   # Guiones "_" que conectan rama con nodo padre.
                primera += "_"
            primera += valor                      # Texto del nodo padre.
            # Segunda linea: la rama "/" que conecta padre con hijo izquierdo.
            segunda = ""
            for _ in range(centro):
                segunda += " "
            segunda += "/"                        # La barra inclinada representa la rama izquierda.
            for _ in range(ancho - centro - 1 + ancho_valor):
                segunda += " "
            # Desplaza las lineas del hijo izquierdo para alinearlas bajo el padre.
            lineas_movidas = []
            for idx in range(len(lineas)):
                linea_aux = lineas[idx]
                relleno = ""
                for _ in range(ancho_valor):      # Agrega espacios a la derecha para igualar anchos.
                    relleno += " "
                lineas_movidas = lineas_movidas + [linea_aux + relleno]
            return [primera, segunda] + lineas_movidas, ancho + ancho_valor, alto + 2, ancho_valor // 2

        # --- CASO: SOLO HIJO DERECHO (sin hijo izquierdo) ---
        if nodo.izquierda is None:
            lineas, ancho, alto, centro = display_aux(nodo.derecha)    # Dibuja el subarbol derecho.
            if hasattr(nodo, 'dato'):
                valor = str(nodo.dato["valor"])
            else:
                valor = str(nodo.valor)
            ancho_valor = len(valor)
            # Primera linea: texto del nodo + guiones hasta la rama derecha.
            primera = valor
            for _ in range(centro):
                primera += "_"
            for _ in range(ancho - centro):
                primera += " "
            # Segunda linea: la rama "\" que conecta padre con hijo derecho.
            segunda = ""
            for _ in range(ancho_valor + centro):
                segunda += " "
            segunda += "\\"                       # La barra invertida representa la rama derecha.
            for _ in range(ancho - centro - 1):
                segunda += " "
            # Desplaza las lineas del hijo derecho para alinearlas bajo el padre.
            lineas_movidas = []
            for idx in range(len(lineas)):
                linea_aux = lineas[idx]
                relleno = ""
                for _ in range(ancho_valor):
                    relleno += " "
                lineas_movidas = lineas_movidas + [relleno + linea_aux]  # Relleno a la IZQUIERDA.
            return [primera, segunda] + lineas_movidas, ancho + ancho_valor, alto + 2, ancho_valor // 2

        # --- CASO GENERAL: NODO CON DOS HIJOS ---
        izquierda, ancho_izq, alto_izq, centro_izq = display_aux(nodo.izquierda) # Bloque del subarbol izquierdo.
        derecha, ancho_der, alto_der, centro_der = display_aux(nodo.derecha)     # Bloque del subarbol derecho.
        if hasattr(nodo, 'dato'):
            valor = str(nodo.dato["valor"])
        else:
            valor = str(nodo.valor)
        ancho_valor = len(valor)

        # Primera linea: espacios + guiones izquierdos + nodo + guiones derechos + espacios.
        primera = ""
        for _ in range(centro_izq + 1):           # Espacios antes del guion izquierdo.
            primera += " "
        for _ in range(ancho_izq - centro_izq - 1): # Guiones que llegan al nodo por la izquierda.
            primera += "_"
        primera += valor                          # Texto del nodo padre.
        for _ in range(centro_der):               # Guiones que salen del nodo hacia la derecha.
            primera += "_"
        for _ in range(ancho_der - centro_der):   # Espacios despues de los guiones derechos.
            primera += " "

        # Segunda linea: rama "/" a la izquierda y "\" a la derecha.
        segunda = ""
        for _ in range(centro_izq):
            segunda += " "
        segunda += "/"                            # Rama izquierda.
        for _ in range(ancho_izq - centro_izq - 1 + ancho_valor + centro_der):
            segunda += " "                        # Espacio entre las dos ramas.
        segunda += "\\"                           # Rama derecha.
        for _ in range(ancho_der - centro_der - 1):
            segunda += " "

        # Iguala la altura de los dos bloques agregando lineas vacias al mas corto.
        if alto_izq < alto_der:
            diferencia = alto_der - alto_izq      # Cuantas lineas le faltan al subarbol izquierdo.
            for _ in range(diferencia):
                relleno_izq = ""
                for _ in range(ancho_izq):
                    relleno_izq += " "
                izquierda = izquierda + [relleno_izq] # Agrega linea vacia al bloque izquierdo.
        elif alto_der < alto_izq:
            diferencia = alto_izq - alto_der      # Cuantas lineas le faltan al subarbol derecho.
            for _ in range(diferencia):
                relleno_der = ""
                for _ in range(ancho_der):
                    relleno_der += " "
                derecha = derecha + [relleno_der]  # Agrega linea vacia al bloque derecho.

        # Combina horizontalmente los bloques izquierdo y derecho linea por linea.
        lineas = [primera, segunda]               # Las dos primeras lineas ya estan construidas arriba.
        for idx in range(len(izquierda)):
            linea_izq = izquierda[idx]            # Linea idx del bloque izquierdo.
            linea_der = derecha[idx]              # Linea idx del bloque derecho (misma altura por igualacion).
            relleno_central = ""
            for _ in range(ancho_valor):          # Espacio entre los dos bloques del ancho del nodo padre.
                relleno_central += " "
            lineas = lineas + [linea_izq + relleno_central + linea_der] # Une los dos bloques horizontalmente.

        # Retorna el bloque completo, su ancho total, su alto total y el centro del nodo padre.
        return lineas, ancho_izq + ancho_valor + ancho_der, max(alto_izq, alto_der) + 2, ancho_izq + ancho_valor // 2

    lineas, _, _, _ = display_aux(raiz)           # Genera el dibujo completo empezando desde la raiz.
    if not lineas:
        return "Árbol vacío"

    # Encuentra el ancho de la linea mas larga para centrar todo el dibujo.
    ancho_maximo = 0
    for i in range(len(lineas)):
        l = len(lineas[i])
        if l > ancho_maximo:
            ancho_maximo = l

    # Centra cada linea agregando espacios a izquierda y derecha (margen simetrico).
    lineas_centradas = []
    for i in range(len(lineas)):
        linea = lineas[i]
        ancho_actual = len(linea)
        faltante = (ancho_maximo + 8) - ancho_actual # +8 es el margen total deseado.
        mitad_izq = faltante // 2                 # Espacios a la izquierda.
        mitad_der = faltante - mitad_izq          # Espacios a la derecha (puede diferir en 1 si faltante es impar).
        espacio_izq = ""
        for _ in range(mitad_izq):
            espacio_izq += " "
        espacio_der = ""
        for _ in range(mitad_der):
            espacio_der += " "
        linea_centrada = espacio_izq + linea + espacio_der
        lineas_centradas = lineas_centradas + [linea_centrada]

    return unir_con_delimitador(lineas_centradas, "\n") # Une todas las lineas con salto de linea.
