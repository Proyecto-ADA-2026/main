# ==============================================================================
# GESTOR DE ARCHIVOS Y CONSTRUCTOR DE TEXTO
# ==============================================================================
# Este archivo tiene DOS responsabilidades separadas:
#
#   1. GestorArchivos: crea la carpeta "resultados/" y escribe/lee archivos
#      (.txt para matrices y .json para arboles) de forma manual, sin json.dump.
#
#   2. ConstructorTexto: arma el texto del panel "Resumen y analisis" de la
#      interfaz, usando solo bucles y concatenacion (sin f-strings ni join).
#
# RESTRICCION ACADEMICA: El JSON se serializa caracter a caracter sin usar
# el modulo json. Esto demuestra comprension del formato JSON.
# ==============================================================================

import os # Modulo estandar para operaciones del sistema de archivos (crear carpetas, abrir archivos).

from medicion_memoria import reporte_memoria_a_texto  # Convierte dict de memoria a texto legible.
from proyecto_final import ordenar_ascendente          # Algoritmo propio de ordenamiento (sin sorted()).


# ==============================================================================
# CLASE: GESTION DE ARCHIVOS TXT Y JSON
# ==============================================================================

class GestorArchivos:
    """Maneja la carpeta de resultados y la escritura/lectura de archivos.

    Principio de diseno: toda interaccion con el disco pasa por esta clase,
    manteniendo el resto del codigo limpio de llamadas a open() directas.
    """

    CARPETA = "resultados"  # Nombre de la carpeta donde se guardan todos los archivos generados.
                            # Es un atributo de clase (compartido por todas las instancias).

    def crear_carpeta(self):
        """Crea la carpeta 'resultados' si todavia no existe.

        Se usa os.mkdir en lugar de os.makedirs porque solo se necesita
        un nivel de carpeta. Si ya existe, el except silencia el error
        (FileExistsError) para no interrumpir el flujo del programa.
        """
        try:
            os.mkdir(self.CARPETA)             # Intenta crear la carpeta en el directorio actual.
        except:
            pass                               # Si ya existe (o cualquier otro error), continua sin fallar.

    def _ruta(self, nombre_archivo):
        """Construye la ruta completa de un archivo dentro de la carpeta resultados.

        Ejemplo: _ruta("matriz_A.txt") => "resultados\\matriz_A.txt"
        Se construye manualmente con "\\" en lugar de os.path.join para
        mantener la restriccion de no usar funciones auxiliares externas.
        """
        return self.CARPETA + "\\" + nombre_archivo # Une carpeta y nombre con separador de Windows.

    def archivo_existe(self, nombre_archivo):
        """Verifica si un archivo existe intentando abrirlo en modo lectura.

        Se usa try/except en lugar de os.path.exists para demostrar manejo
        de excepciones. Si open() falla, el archivo no existe.
        """
        ruta = self._ruta(nombre_archivo)      # Construye la ruta completa.
        try:
            f = open(ruta, "r", encoding="utf-8") # Intenta abrir para lectura.
            f.close()                          # Si no hay error, cierra el archivo.
            return True                        # El archivo existe y es legible.
        except:
            return False                       # Cualquier excepcion (FileNotFoundError, etc.) => no existe.

    def guardar_txt(self, nombre_archivo, contenido):
        """Guarda un texto completo en un archivo dentro de la carpeta resultados.

        Modo "w" sobreescribe si el archivo ya existe (comportamiento deseado
        para regenerar resultados con nuevos datos).
        """
        self.crear_carpeta()                   # Asegura que la carpeta existe antes de escribir.
        ruta = self._ruta(nombre_archivo)      # Ruta completa del archivo de destino.
        f = open(ruta, "w", encoding="utf-8")  # Abre en modo escritura (sobreescribe si existe).
        f.write(contenido)                     # Escribe todo el contenido de una vez.
        f.close()                              # Libera el recurso del archivo.

    def guardar_matriz(self, nombre_archivo, matriz, titulo):
        """Guarda una matriz numerica en TXT con columnas alineadas.

        Formato de salida:
          Titulo
          Tamano: NxN
          ============================================================
          val1      val2      val3   ...
          ...

        Se usa ancho fijo de 10 caracteres por celda para alinear columnas
        incluso cuando los valores tienen distinto numero de digitos (A3 puede
        tener valores de muchos digitos).
        """
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)
        n = len(matriz)                        # Dimension de la matriz cuadrada.
        f = open(ruta, "w", encoding="utf-8")

        f.write(titulo + "\n")                 # Primera linea: nombre de la matriz.
        f.write("Tamano: " + str(n) + "x" + str(n) + "\n") # Segunda linea: dimension.

        sep = ""                               # Construye la linea separadora manualmente.
        for i in range(60):                    # 60 signos "=" como separador visual.
            sep += "="
        f.write(sep + "\n\n")                  # Escribe separador y linea en blanco.

        for fila in matriz:                    # Itera sobre cada fila de la matriz.
            linea = ""                         # Acumulador del texto de esta fila.
            for i in range(len(fila)):         # Itera sobre cada columna de la fila.
                linea += f"{fila[i]:10}"       # Formato con ancho fijo 10: alinea a la derecha.
                if i < len(fila) - 1:          # Agrega separacion entre columnas (no al final).
                    linea += "   "
            f.write(linea + "\n")              # Escribe la fila formateada y salta de linea.

        f.close()

    def _nodo_a_texto_json(self, nodo_dict, sangria):
        """Serializa recursivamente un nodo del arbol (como dict) a texto JSON.

        FORMATO JSON GENERADO para un nodo:
          {
            "valor": 5,
            "cantidad": 12,
            "izquierda": { ... } o null,
            "derecha": { ... } o null
          }

        La sangria (indentacion) se incrementa en cada nivel de recursion
        para que el JSON sea legible (pretty-print).

        PARAMETROS:
          nodo_dict: dict con claves "valor", "cantidad", "izquierda", "derecha".
          sangria: string de espacios que representa el nivel de indentacion actual.
        """
        if nodo_dict is None:                  # Un hijo que no existe se escribe como "null" en JSON.
            return "null"

        s = sangria + "  "                    # Aumenta la sangria para los campos del objeto hijo.
        resultado = "{\n"                     # Inicio del objeto JSON (llave de apertura).
        resultado += s + '"valor": ' + str(nodo_dict["valor"]) + ",\n"     # Campo valor (numero entero).
        resultado += s + '"cantidad": ' + str(nodo_dict["cantidad"]) + ",\n" # Campo cantidad (frecuencia).
        # Serializacion recursiva de los hijos (puede retornar "null" o un objeto JSON anidado).
        resultado += s + '"izquierda": ' + self._nodo_a_texto_json(nodo_dict["izquierda"], s) + ",\n"
        resultado += s + '"derecha": '   + self._nodo_a_texto_json(nodo_dict["derecha"],   s) + "\n"
        resultado += sangria + "}"            # Cierre del objeto JSON con la sangria del nivel padre.
        return resultado

    def guardar_arbol_json(self, nombre_archivo, dict_arbol, nombre_id):
        """Guarda la estructura del arbol en un archivo JSON escrito manualmente.

        FORMATO DEL ARCHIVO:
          {
            "arbol": "ArbolA",
            "descripcion": "...",
            "estructura": { ... arbol completo ... }
          }

        Se construye el JSON como string usando concatenacion, sin json.dump.
        Esto garantiza que el formato es correcto porque se controla caracter
        a caracter, y demuestra comprension del formato JSON.
        """
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)

        texto = "{\n"                          # Objeto raiz del JSON.
        texto += '  "arbol": "' + nombre_id + '",\n'  # Identificador del arbol.
        texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
        texto += '  "estructura": '
        texto += self._nodo_a_texto_json(dict_arbol, "  ") # Serializa el arbol entero recursivamente.
        texto += "\n}"                         # Cierre del objeto raiz.

        f = open(ruta, "w", encoding="utf-8")
        f.write(texto)
        f.close()

    def abrir_archivo(self, nombre_archivo):
        """Abre un archivo de la carpeta resultados con la aplicacion predeterminada del SO.

        os.startfile() es exclusivo de Windows; abre el archivo como si el usuario
        hiciera doble clic (usa el programa asociado a la extension: .txt => Bloc de notas,
        .json => editor de texto o VS Code).
        Retorna False si el archivo no existe o no se puede abrir.
        """
        if not self.archivo_existe(nombre_archivo): # Verifica antes de intentar abrir.
            return False
        ruta = self._ruta(nombre_archivo)
        try:
            os.startfile(ruta)                 # Instruccion de Windows para abrir con programa predeterminado.
            return True
        except:
            return False                       # Puede fallar si no hay programa asociado.


# ==============================================================================
# CLASE: CONSTRUCCION DEL TEXTO DEL PANEL DE RESUMEN
# ==============================================================================

class ConstructorTexto:
    """Genera el texto completo del panel 'Resumen y analisis' de la interfaz.

    Cada metodo construye un fragmento de texto y los une en construir_salida().
    Se usan solo for/while y += (sin f-strings ni .join()) para cumplir la
    restriccion de no usar funciones de string avanzadas.
    """

    def quitar_duplicados(self, lista):
        """Elimina elementos duplicados de una lista conservando la primera aparicion.

        Sustituye manualmente a list(set(lista)) porque set() no garantiza orden
        y no cumple la restriccion de no usar estructuras avanzadas sin explicacion.

        ALGORITMO: Para cada valor nuevo, busca si ya esta en la lista de unicos.
        Si no esta, lo agrega. Costo O(n^2) pero las listas son pequenas (valores 0-9 para A).
        """
        unicos = []                            # Lista resultado sin duplicados.
        for val in lista:                      # Revisa cada valor de la lista original.
            esta = False                       # Bandera: asume que val NO esta en unicos.
            i = 0
            while i < len(unicos):             # Busca manualmente en la lista de unicos.
                if unicos[i] == val:
                    esta = True                # Encontro el valor: marcar como duplicado.
                    break                      # No hace falta seguir buscando.
                i += 1
            if not esta:                       # Solo agrega si no se encontro en unicos.
                unicos = unicos + [val]
        return unicos

    def lista_a_texto(self, lista, max_mostrar):
        """Convierte una lista numerica a texto, limitando la cantidad visible.

        Si la lista tiene mas de max_mostrar elementos, muestra los primeros
        max_mostrar y agrega "... (+N mas)" para indicar el truncado.
        Esto evita que el panel de resumen se desborde con listas muy largas.
        """
        if len(lista) == 0:
            return "  (ninguno)"               # Lista vacia: mensaje especial.

        texto = "  "                           # Indentacion visual de 2 espacios.
        total = len(lista)

        if total <= max_mostrar:               # Caben todos: muestra la lista completa.
            for i in range(total):
                texto += str(lista[i])
                if i < total - 1:
                    texto += ", "              # Separador entre elementos.
            return texto

        for i in range(max_mostrar):           # No caben todos: muestra solo los primeros max_mostrar.
            texto += str(lista[i])
            if i < max_mostrar - 1:
                texto += ", "
        texto += " ... (+" + str(total - max_mostrar) + " mas)" # Indica cuantos se omitieron.
        return texto

    def separador_igual(self, longitud):
        """Crea una linea de signos '=' de la longitud especificada.

        Se usa para subrayar los titulos de cada seccion del resumen,
        dando la misma longitud que el titulo para alinearlos visualmente.
        """
        linea = ""
        for i in range(longitud):
            linea += "="
        return linea

    def bloque_categoria(self, etiqueta, cantidad, valores):
        """Construye el bloque de texto de una categoria del analisis numerico.

        Formato generado:
          Pares          : 52
            2, 4, 6, ...

        Se eliminan duplicados y se ordenan los valores para una presentacion limpia.
        """
        unicos = self.quitar_duplicados(valores) # Elimina valores repetidos de la lista.
        unicos = ordenar_ascendente(unicos)      # Ordena los valores unicos de menor a mayor.
        texto = etiqueta + ": " + str(cantidad) + "\n"  # Primera linea: etiqueta y cantidad total.
        texto += self.lista_a_texto(unicos, 30) + "\n"  # Segunda linea: valores unicos (max 30 visibles).
        return texto

    def resumen_matriz(self, titulo, analisis):
        """Genera el bloque de resumen completo de una matriz (A o A3).

        Muestra las 5 categorias: pares, impares, primos, perfectos, cuadrados.
        El dict 'analisis' viene de analizar_matriz() del backend.
        """
        sep = self.separador_igual(len(titulo)) # Subrayado del mismo ancho que el titulo.
        texto = titulo + "\n" + sep + "\n"
        texto += self.bloque_categoria("Pares          ", analisis["pares"]["cantidad"],     analisis["pares"]["valores"])
        texto += self.bloque_categoria("Impares        ", analisis["impares"]["cantidad"],   analisis["impares"]["valores"])
        texto += self.bloque_categoria("Primos         ", analisis["primos"]["cantidad"],    analisis["primos"]["valores"])
        texto += self.bloque_categoria("Perfectos      ", analisis["perfectos"]["cantidad"], analisis["perfectos"]["valores"])
        texto += self.bloque_categoria("Cuadrados perf.", analisis["cuadrados"]["cantidad"], analisis["cuadrados"]["valores"])
        return texto

    def repeticiones_a_texto(self, rep):
        """Convierte el diccionario de frecuencias {valor: cantidad} a texto ordenado.

        Ejemplo de salida: "0: 5, 1: 8, 2: 6, ..."
        Los valores se ordenan para que el texto sea consistente entre ejecuciones.
        """
        claves = []                            # Lista con todos los valores unicos del diccionario.
        for k in rep:
            claves = claves + [k]              # Extrae claves sin usar list(rep.keys()).
        claves = ordenar_ascendente(claves)    # Ordena los valores de menor a mayor.

        texto = ""
        for i in range(len(claves)):
            texto += str(claves[i]) + ": " + str(rep[claves[i]]) # "valor: frecuencia".
            if i < len(claves) - 1:
                texto += ", "                  # Separador entre pares, excepto al final.
        return texto

    def vector_a_texto(self, vector, max_chars):
        """Convierte un vector a texto y lo trunca si supera max_chars caracteres.

        Los vectores de A3 pueden ser muy largos (n^2 elementos con valores grandes).
        Se trunca con "..." para que el panel de resumen no se desborde.
        """
        texto = "["                            # Inicio del vector en formato lista.
        for i in range(len(vector)):
            texto += str(vector[i])
            if i < len(vector) - 1:
                texto += ", "
        texto += "]"                           # Cierre del vector.
        if len(texto) > max_chars:
            return texto[:max_chars] + "..."   # Trunca al limite y agrega puntos suspensivos.
        return texto

    def bloque_validacion_arbol(self, titulo, elementos_matriz,
                                 elementos_arbol, valores_unicos,
                                 nodos_arbol, altura):
        """Construye el bloque de validacion de consistencia entre la matriz y el arbol.

        VERIFICACION:
          - elementos_matriz debe == elementos_arbol:
              La suma de todas las frecuencias del arbol debe igualar n*n.
          - valores_unicos debe == nodos_arbol:
              Cada valor unico de la matriz tiene exactamente un nodo en el arbol.
        Si ambas condiciones se cumplen, el arbol representa fielmente la matriz.
        """
        texto = titulo + ":\n"
        texto += "- Elementos matriz: " + str(elementos_matriz) + "\n"          # Total de celdas n*n.
        texto += "- Elementos representados en arbol: " + str(elementos_arbol) + "\n" # Suma de frecuencias del arbol.
        texto += "- Valores unicos: " + str(valores_unicos) + "\n"              # Cantidad de valores distintos.
        texto += "- Nodos del arbol: " + str(nodos_arbol) + "\n"                # Cantidad de nodos en el BST.
        texto += "- Altura: " + str(altura) + "\n"                              # Niveles del arbol.
        if elementos_matriz == elementos_arbol and valores_unicos == nodos_arbol: # Ambas condiciones deben cumplirse.
            texto += "- Validacion: correcta\n"
        else:
            texto += "- Validacion: revisar\n"  # Indica inconsistencia si algo no coincide.
        return texto

    def construir_salida(self, analisis_A, analisis_A3, rep_A, rep_A3,
                          va_asc, va_desc, va3_asc, va3_desc,
                          mem_actual, mem_pico, estimacion,
                          validacion_A=None, validacion_A3=None):
        """Une todos los bloques de texto que se muestran en el panel derecho de la interfaz.

        PARAMETROS:
          analisis_A/A3: dicts de analizar_matriz() con pares, impares, primos, etc.
          rep_A/A3: dicts de contar_repeticiones() con frecuencias.
          va_asc/desc, va3_asc/desc: vectores ordenados (ascendente y descendente).
          mem_actual/pico: bytes medidos por tracemalloc.
          estimacion: dict de estimar_memoria_estructuras() o un numero simple.
          validacion_A/A3: dicts de validacion del arbol (opcional).
        """
        salida = ""                            # Acumulador del texto completo del panel.

        # SECCION 1: Resumen de categorias numericas de la matriz A.
        salida += self.resumen_matriz("RESUMEN MATRIZ A", analisis_A)
        salida += "\nRepeticiones A:\n"
        salida += self.repeticiones_a_texto(rep_A) # Frecuencia de cada valor en A.

        salida += "\n\n"

        # SECCION 2: Resumen de categorias numericas de A3.
        salida += self.resumen_matriz("RESUMEN MATRIZ A3", analisis_A3)
        salida += "\nRepeticiones A3:\n"
        salida += self.repeticiones_a_texto(rep_A3)

        # SECCION 3: Vectores ordenados de A y A3.
        salida += "\n\nVECTORES ORDENADOS\n"
        salida += "------------------\n"
        salida += "A ascendente:\n"    + self.vector_a_texto(va_asc,  1200) # Limite de 1200 chars para evitar desborde.
        salida += "\n\nA descendente:\n"  + self.vector_a_texto(va_desc, 1200)
        salida += "\n\nA3 ascendente:\n"  + self.vector_a_texto(va3_asc, 1200)
        salida += "\n\nA3 descendente:\n" + self.vector_a_texto(va3_desc,1200)

        # SECCION 4: Informacion de memoria.
        salida += "\n\nMEMORIA\n"
        salida += "-------\n"
        if isinstance(estimacion, dict):       # Si es un dict, es la estimacion detallada por estructura.
            salida += reporte_memoria_a_texto(estimacion)
        else:                                  # Si es un numero, es la estimacion simple (bytes totales).
            salida += "Estimacion A   : " + str(estimacion) + " bytes\n"
        salida += "\nMedicion real con tracemalloc:\n"
        salida += "Memoria actual : " + str(mem_actual // 1024) + " KB\n" # Convierte bytes a KB con division entera.
        salida += "Memoria pico   : " + str(mem_pico   // 1024) + " KB\n" # El pico es el maximo alcanzado durante la ejecucion.

        # SECCION 5: Validacion de consistencia entre matrices y arboles (si se proporcionan).
        if validacion_A is not None and validacion_A3 is not None:
            salida += "\nVALIDACION DE ARBOLES\n"
            salida += "---------------------\n"
            salida += self.bloque_validacion_arbol(
                "Validacion arbol A",
                validacion_A["elementos_matriz"],
                validacion_A["elementos_arbol"],
                validacion_A["valores_unicos"],
                validacion_A["nodos_arbol"],
                validacion_A["altura"]
            )
            salida += "\n"
            salida += self.bloque_validacion_arbol(
                "Validacion arbol A3",
                validacion_A3["elementos_matriz"],
                validacion_A3["elementos_arbol"],
                validacion_A3["valores_unicos"],
                validacion_A3["nodos_arbol"],
                validacion_A3["altura"]
            )

        return salida                          # Texto completo listo para mostrarse en la interfaz.


def arbol_a_json_texto(raiz):
    """Convierte un arbol de NodoJSON a texto JSON manualmente (funcion independiente).

    Alternativa a GestorArchivos.guardar_arbol_json para cuando solo se necesita
    el texto JSON sin guardarlo en disco (ej: para pruebas o comparacion).
    """
    def nodo_a_texto(nodo, sangria):
        """Serializa un nodo de NodoJSON a texto JSON con sangria progresiva."""
        if nodo is None:
            return "null"                      # Hijo vacio => null en JSON.
        s = sangria + "  "                    # Aumenta la sangria para los campos de este nodo.
        resultado = "{\n"
        resultado += s + '"valor": ' + str(nodo.dato["valor"]) + ",\n"
        resultado += s + '"cantidad": ' + str(nodo.dato["cantidad"]) + ",\n"
        resultado += s + '"izquierda": ' + nodo_a_texto(nodo.izquierda, s) + ",\n" # Rama izquierda recursiva.
        resultado += s + '"derecha": '   + nodo_a_texto(nodo.derecha,   s) + "\n"  # Rama derecha recursiva.
        resultado += sangria + "}"
        return resultado

    texto = "{\n"                              # Objeto raiz del JSON.
    texto += '  "arbol": "Raiz",\n'
    texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
    texto += '  "estructura": ' + nodo_a_texto(raiz, "  ") + "\n" # Serializa el arbol desde la raiz.
    texto += "}"
    return texto
