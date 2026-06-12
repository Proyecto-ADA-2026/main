# ==============================================================================
# MEDICION Y ESTIMACION DE MEMORIA
# ==============================================================================
# Este modulo concentra la medicion real con tracemalloc y la estimacion
# profunda de las principales estructuras generadas por el proyecto.
# Se mantiene separado del backend para que la logica algoritmica no dependa de
# detalles de medicion. La interfaz importa estas funciones cuando necesita
# reportar memoria actual, memoria pico y tamano aproximado de estructuras.
# ==============================================================================

import sys          # Permite consultar el tamano base de objetos con getsizeof.
import tracemalloc  # Permite medir memoria actual y pico durante la ejecucion.


def tamano_profundo(objeto, vistos=None):
    """Calcula el tamano aproximado de un objeto y sus contenidos internos.

    sys.getsizeof mide solo el objeto principal. Esta funcion baja de forma
    recursiva por diccionarios, listas, tuplas, sets y atributos internos para
    aproximar mejor el costo de matrices, vectores, frecuencias y arboles.
    """
    if vistos is None:                          # Primer llamado: crea conjunto de objetos visitados.
        vistos = set()

    obj_id = id(objeto)                         # Identificador unico del objeto en memoria.
    if obj_id in vistos:                        # Evita contar dos veces referencias compartidas.
        return 0

    vistos.add(obj_id)                          # Marca el objeto como procesado.
    tamano = sys.getsizeof(objeto)              # Tamano superficial del objeto actual.

    if isinstance(objeto, dict):                # Diccionario: cuenta claves y valores.
        for clave, valor in objeto.items():
            tamano += tamano_profundo(clave, vistos)
            tamano += tamano_profundo(valor, vistos)
    elif isinstance(objeto, (list, tuple, set)): # Colecciones: cuenta cada elemento contenido.
        for elemento in objeto:
            tamano += tamano_profundo(elemento, vistos)
    elif hasattr(objeto, "__dict__"):           # Objetos como NodoJSON: cuenta sus atributos.
        tamano += tamano_profundo(objeto.__dict__, vistos)

    return tamano                               # Retorna bytes estimados de todo el subgrafo.


def bytes_a_kb_mb(bytes_valor):
    """Convierte bytes a una tupla con bytes, KB y MB.

    La funcion evita repetir conversiones y mantiene uniforme el formato del
    reporte en consola e interfaz.
    """
    kb = bytes_valor / 1024                     # Conversion binaria de bytes a kilobytes.
    mb = kb / 1024                              # Conversion de kilobytes a megabytes.
    return bytes_valor, kb, mb                  # Devuelve las tres unidades.


def estimar_memoria_estructuras(A=None, A2=None, A3=None, vector=None,
                                frecuencias=None, arbol=None):
    """Estima memoria profunda de las estructuras principales del programa.

    Puede recibir estructuras individuales o diccionarios con variantes de A y
    A3. El resultado es un diccionario texto -> bytes para armar reportes.
    """
    memoria = {}                                # Acumulador de cada componente medido.

    if A is not None:                           # Matriz original.
        memoria["Matriz A"] = tamano_profundo(A)

    if A2 is not None:                          # Matriz intermedia usada para A3.
        memoria["Matriz A2"] = tamano_profundo(A2)

    if A3 is not None:                          # Matriz al cubo.
        memoria["Matriz A3"] = tamano_profundo(A3)

    if vector is not None:                      # Vector o diccionario de vectores.
        if isinstance(vector, dict):
            for nombre in vector:
                memoria["Vector " + str(nombre)] = tamano_profundo(vector[nombre])
        else:
            memoria["Vector"] = tamano_profundo(vector)

    if frecuencias is not None:                 # Frecuencias de valores unicos.
        if isinstance(frecuencias, dict) and ("A" in frecuencias or "A3" in frecuencias):
            for nombre in frecuencias:
                memoria["Frecuencias " + str(nombre)] = tamano_profundo(frecuencias[nombre])
        else:
            memoria["Frecuencias"] = tamano_profundo(frecuencias)

    if arbol is not None:                       # Arbol o diccionario de arboles.
        if isinstance(arbol, dict):
            for nombre in arbol:
                memoria["Arbol " + str(nombre)] = tamano_profundo(arbol[nombre])
        else:
            memoria["Arbol binario"] = tamano_profundo(arbol)

    total = 0                                   # Suma manual de todos los componentes estimados.
    for nombre in memoria:
        total += memoria[nombre]
    memoria["Total estimado estructuras"] = total

    return memoria                              # Diccionario final de reporte.


def imprimir_reporte_memoria(memoria):
    """Imprime en consola un reporte legible de memoria estimada.

    Es util para pruebas por terminal o revision rapida sin interfaz grafica.
    """
    print("MEMORIA DETALLADA")
    print("-----------------")

    for nombre, bytes_valor in memoria.items():
        bytes_total, kb, mb = bytes_a_kb_mb(bytes_valor)
        print(f"{nombre:30}: {bytes_total} bytes | {kb:.2f} KB | {mb:.4f} MB")


def reporte_memoria_a_texto(memoria):
    """Convierte el reporte de memoria estimada a texto para la interfaz.

    Devuelve un string completo para que ConstructorTexto lo inserte en el panel
    de resumen.
    """
    texto = "Estimacion detallada por estructura:\n" # Encabezado visible del bloque.
    for nombre, bytes_valor in memoria.items():
        bytes_total, kb, mb = bytes_a_kb_mb(bytes_valor)
        texto += "- " + str(nombre) + ": "
        texto += str(bytes_total) + " bytes | "
        texto += f"{kb:.2f} KB | {mb:.4f} MB\n"
    return texto


def iniciar_medicion_memoria():
    """Inicia el rastreo de uso de memoria utilizando tracemalloc.

    Debe llamarse antes de crear las estructuras que se desean observar.
    """
    tracemalloc.start()


def obtener_memoria_actual_y_pico():
    """Retorna memoria actual y pico maximo desde tracemalloc.

    actual representa memoria rastreada al momento de consultar.
    pico representa el maximo alcanzado desde que inicio tracemalloc.
    """
    actual, pico = tracemalloc.get_traced_memory() # Consulta medicion real del rastreador.
    return actual, pico                         # Devuelve ambos valores en bytes.


def detener_medicion_memoria():
    """Detiene el rastreador de memoria de tracemalloc.

    Libera el seguimiento para no dejar mediciones abiertas despues del reporte.
    """
    tracemalloc.stop()


def estimar_memoria_matriz(n):
    """Mantiene compatibilidad con la estimacion simple de una matriz n x n.

    Usa una aproximacion clasica de 28 bytes por entero en Python. La medicion
    principal del proyecto usa estimar_memoria_estructuras, que es mas completa.
    """
    return n * n * 28                           # n2 enteros por 28 bytes aproximados.


# ==============================================================================
# RESUMEN DEL ARCHIVO
# ==============================================================================
# medicion_memoria.py separa todo lo relacionado con memoria:
# - tamano_profundo estima bytes de estructuras compuestas.
# - estimar_memoria_estructuras mide A, A2, A3, vectores, frecuencias y arboles.
# - tracemalloc entrega memoria actual y memoria pico de ejecucion.
# - Las funciones no alteran matrices ni arboles; solo los inspeccionan.
