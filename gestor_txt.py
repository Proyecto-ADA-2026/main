# ==============================================================================
# IMPORTACIONES Y CONFIGURACION INICIAL
# ==============================================================================
# Este modulo separa la construccion de textos y archivos del backend algoritmico.
# La interfaz lo usa para guardar resultados en la carpeta "resultados" y para
# armar el resumen que aparece en el panel derecho.
# No calcula matrices ni arboles: solo transforma datos ya generados en texto.

import os # Permite crear carpetas y abrir archivos con el programa predeterminado.

from medicion_memoria import reporte_memoria_a_texto
from proyecto_final import ordenar_ascendente


# ==============================================================================
# GESTION DE ARCHIVOS TXT Y JSON
# ==============================================================================

class GestorArchivos:
    """Maneja la creacion de la carpeta de resultados y la escritura de archivos.

    Centraliza las salidas externas del proyecto. Asi la interfaz no repite
    codigo de rutas, escritura TXT, escritura JSON ni apertura de archivos.
    """

    CARPETA = "resultados"                    # Carpeta unica donde se guardan salidas generadas.

    def crear_carpeta(self):
        """Crea la carpeta resultados si todavia no existe."""
        try:
            os.mkdir(self.CARPETA)             # Crea una sola carpeta, sin os.makedirs.
        except:
            pass                               # Si ya existe, continua sin interrumpir el programa.

    def _ruta(self, nombre_archivo):
        """Construye la ruta de un archivo dentro de resultados.

        El proyecto mantiene rutas con "\\" porque esta pensado para Windows.
        """
        return self.CARPETA + "\\" + nombre_archivo # Une manualmente carpeta y nombre.

    def archivo_existe(self, nombre_archivo):
        """Verifica si un archivo generado existe intentando abrirlo.

        Devuelve True si se pudo abrir en lectura y False si no existe o falla.
        """
        ruta = self._ruta(nombre_archivo)      # Ruta completa dentro de resultados.
        try:
            f = open(ruta, "r", encoding="utf-8") # Intenta abrir en lectura.
            f.close()
            return True
        except:
            return False

    def guardar_txt(self, nombre_archivo, contenido):
        """Guarda un texto completo dentro de la carpeta resultados.

        Sirve para textos generales ya construidos por otros componentes.
        """
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)      # Calcula la ubicacion del archivo.
        f = open(ruta, "w", encoding="utf-8")
        f.write(contenido)                     # Escribe el contenido recibido.
        f.close()

    def guardar_matriz(self, nombre_archivo, matriz, titulo):
        """Guarda una matriz en TXT con columnas alineadas.

        Recorre fila por fila y celda por celda. No cambia la matriz recibida;
        solo la serializa de forma legible.
        """
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)      # Ruta donde se guardara la matriz.
        n = len(matriz)                        # Tamano de la matriz cuadrada.
        f = open(ruta, "w", encoding="utf-8")

        f.write(titulo + "\n")
        f.write("Tamano: " + str(n) + "x" + str(n) + "\n")

        sep = ""                               # Separador visual del encabezado.
        for i in range(60):                    # Construye el separador manualmente.
            sep += "="
        f.write(sep + "\n\n")

        for fila in matriz:                    # Recorre cada fila de la matriz.
            linea = ""                         # Acumulador de la fila formateada.
            for i in range(len(fila)):         # Recorre cada columna.
                linea += f"{fila[i]:10}"       # Alinea cada valor con ancho fijo.
                if i < len(fila) - 1:          # Agrega separacion entre columnas.
                    linea += "   "
            f.write(linea + "\n")

        f.close()

    def _nodo_a_texto_json(self, nodo_dict, sangria):
        """Convierte recursivamente un diccionario de nodo a texto JSON manual.

        Cada llamada escribe un nodo y delega sus ramas izquierda/derecha a la
        misma funcion. Si la rama esta vacia, escribe null.
        """
        if nodo_dict is None:
            return "null"

        s = sangria + "  "                    # Aumenta sangria para los hijos.
        resultado = "{\n"                     # Inicio del objeto JSON.
        resultado += s + '"valor": ' + str(nodo_dict["valor"]) + ",\n"
        resultado += s + '"cantidad": ' + str(nodo_dict["cantidad"]) + ",\n"
        resultado += s + '"izquierda": ' + self._nodo_a_texto_json(nodo_dict["izquierda"], s) + ",\n" # Rama izquierda.
        resultado += s + '"derecha": ' + self._nodo_a_texto_json(nodo_dict["derecha"], s) + "\n"      # Rama derecha.
        resultado += sangria + "}"
        return resultado

    def guardar_arbol_json(self, nombre_archivo, dict_arbol, nombre_id):
        """Guarda el arbol en JSON sin usar json.dump.

        El archivo conserva valor, cantidad y punteros logicos izquierda/derecha
        para demostrar que el arbol guarda valores unicos con frecuencias.
        """
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)      # Archivo JSON de salida.

        texto = "{\n"                          # Construccion manual del JSON principal.
        texto += '  "arbol": "' + nombre_id + '",\n'
        texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
        texto += '  "estructura": '
        texto += self._nodo_a_texto_json(dict_arbol, "  ") # Serializa el arbol recursivamente.
        texto += "\n}"

        f = open(ruta, "w", encoding="utf-8")
        f.write(texto)
        f.close()

    def abrir_archivo(self, nombre_archivo):
        """Abre un archivo de resultados con la aplicacion predeterminada.

        Usa os.startfile, por eso esta funcionalidad es especifica de Windows.
        """
        if not self.archivo_existe(nombre_archivo):
            return False
        ruta = self._ruta(nombre_archivo)      # Ruta del archivo que se intentara abrir.
        try:
            os.startfile(ruta)                 # Windows abre el archivo con su programa asociado.
            return True
        except:
            return False


# ==============================================================================
# CONSTRUCCION DE TEXTO PARA EL PANEL DE RESUMEN
# ==============================================================================

class ConstructorTexto:
    """Genera el texto del panel 'Resumen y analisis' con estructuras de control basicas.

    Su objetivo es presentar de forma ordenada el analisis numerico, repeticiones,
    vectores, memoria y validacion de arboles sin mezclar esa logica con Tkinter.
    """

    def quitar_duplicados(self, lista):
        """Elimina duplicados manualmente conservando valores unicos.

        Se usa para que el resumen de categorias no imprima el mismo valor muchas
        veces aunque aparezca repetido en la matriz.
        """
        unicos = []                            # Acumulador de valores sin repetir.
        for val in lista:                      # Revisa cada valor recibido.
            esta = False                       # Bandera para saber si ya existe.
            i = 0
            while i < len(unicos):             # Busca manualmente dentro de unicos.
                if unicos[i] == val:
                    esta = True
                    break
                i += 1
            if not esta:                       # Si no se encontro, se agrega.
                unicos = unicos + [val]
        return unicos

    def lista_a_texto(self, lista, max_mostrar):
        """Convierte una lista a texto, limitando la cantidad visible.

        Cuando la lista es larga, muestra una vista previa y la cantidad restante
        para que la interfaz siga siendo legible.
        """
        if len(lista) == 0:
            return "  (ninguno)"

        texto = "  "                           # Indentacion visual del listado.
        total = len(lista)                     # Cantidad total de valores.

        if total <= max_mostrar:
            for i in range(total):             # Muestra todos los valores si caben.
                texto += str(lista[i])
                if i < total - 1:
                    texto += ", "
            return texto

        for i in range(max_mostrar):           # Muestra solo una vista previa.
            texto += str(lista[i])
            if i < max_mostrar - 1:
                texto += ", "
        texto += " ... (+" + str(total - max_mostrar) + " mas)"
        return texto

    def separador_igual(self, longitud):
        """Crea una linea de signos igual del largo indicado."""
        linea = ""                             # Acumulador del separador.
        for i in range(longitud):
            linea += "="
        return linea

    def bloque_categoria(self, etiqueta, cantidad, valores):
        """Construye el bloque de una categoria del analisis numerico.

        Recibe los valores de una categoria, quita duplicados, ordena y arma
        un bloque textual con cantidad total y muestra de valores.
        """
        unicos = self.quitar_duplicados(valores) # Evita repetir valores en la vista.
        unicos = ordenar_ascendente(unicos)      # Ordena con algoritmo propio del backend.
        texto = etiqueta + ": " + str(cantidad) + "\n"
        texto += self.lista_a_texto(unicos, 30) + "\n"
        return texto

    def resumen_matriz(self, titulo, analisis):
        """Genera el resumen textual de pares, impares, primos y otros grupos.

        El diccionario de analisis viene del backend. Este metodo solo organiza
        la informacion para lectura humana.
        """
        sep = self.separador_igual(len(titulo)) # Separador del titulo.
        texto = titulo + "\n" + sep + "\n"
        texto += self.bloque_categoria("Pares          ", analisis["pares"]["cantidad"],     analisis["pares"]["valores"])
        texto += self.bloque_categoria("Impares        ", analisis["impares"]["cantidad"],   analisis["impares"]["valores"])
        texto += self.bloque_categoria("Primos         ", analisis["primos"]["cantidad"],    analisis["primos"]["valores"])
        texto += self.bloque_categoria("Perfectos      ", analisis["perfectos"]["cantidad"], analisis["perfectos"]["valores"])
        texto += self.bloque_categoria("Cuadrados perf.", analisis["cuadrados"]["cantidad"], analisis["cuadrados"]["valores"])
        return texto

    def repeticiones_a_texto(self, rep):
        """Convierte el diccionario de repeticiones en texto ordenado.

        Ordenar las claves permite mostrar frecuencias de menor a mayor valor.
        """
        claves = []                            # Guarda los valores del diccionario.
        for k in rep:
            claves = claves + [k]
        claves = ordenar_ascendente(claves)    # Ordena las claves numericas.

        texto = ""                             # Acumulador del texto final.
        for i in range(len(claves)):
            texto += str(claves[i]) + ": " + str(rep[claves[i]])
            if i < len(claves) - 1:
                texto += ", "
        return texto

    def vector_a_texto(self, vector, max_chars):
        """Convierte un vector a texto y recorta si supera el maximo de caracteres.

        Evita saturar el panel cuando n crece, pero conserva una vista parcial
        del ordenamiento ascendente o descendente.
        """
        texto = "["                            # Inicio visual del vector.
        for i in range(len(vector)):
            texto += str(vector[i])
            if i < len(vector) - 1:
                texto += ", "
        texto += "]"
        if len(texto) > max_chars:
            return texto[:max_chars] + "..."
        return texto

    def bloque_validacion_arbol(self, titulo, elementos_matriz,
                                 elementos_arbol, valores_unicos,
                                 nodos_arbol, altura):
        """Construye el bloque que valida si el arbol representa toda la matriz.

        La validacion importante es:
        elementos_matriz == suma de cantidades del arbol, y
        valores_unicos == numero de nodos del arbol.
        """
        texto = titulo + ":\n"
        texto += "- Elementos matriz: " + str(elementos_matriz) + "\n"
        texto += "- Elementos representados en arbol: " + str(elementos_arbol) + "\n"
        texto += "- Valores unicos: " + str(valores_unicos) + "\n"
        texto += "- Nodos del arbol: " + str(nodos_arbol) + "\n"
        texto += "- Altura: " + str(altura) + "\n"
        if elementos_matriz == elementos_arbol and valores_unicos == nodos_arbol: # Verifica consistencia.
            texto += "- Validacion: correcta\n"
        else:
            texto += "- Validacion: revisar\n"
        return texto

    def construir_salida(self, analisis_A, analisis_A3, rep_A, rep_A3,
                          va_asc, va_desc, va3_asc, va3_desc,
                          mem_actual, mem_pico, estimacion,
                          validacion_A=None, validacion_A3=None):
        """Une todos los bloques de texto que se muestran en el panel derecho.

        Es el reporte final de ejecucion para la interfaz: analisis de A/A3,
        frecuencias, vectores ordenados, memoria medida/estimada y arboles.
        """
        salida = ""                            # Acumulador completo del resumen.
        salida += self.resumen_matriz("RESUMEN MATRIZ A", analisis_A)
        salida += "\nRepeticiones A:\n"
        salida += self.repeticiones_a_texto(rep_A)

        salida += "\n\n"
        salida += self.resumen_matriz("RESUMEN MATRIZ A3", analisis_A3)
        salida += "\nRepeticiones A3:\n"
        salida += self.repeticiones_a_texto(rep_A3)

        salida += "\n\nVECTORES ORDENADOS\n"
        salida += "------------------\n"
        salida += "A ascendente:\n"    + self.vector_a_texto(va_asc,  1200)
        salida += "\n\nA descendente:\n"  + self.vector_a_texto(va_desc, 1200)
        salida += "\n\nA3 ascendente:\n"  + self.vector_a_texto(va3_asc, 1200)
        salida += "\n\nA3 descendente:\n" + self.vector_a_texto(va3_desc,1200)

        salida += "\n\nMEMORIA\n"
        salida += "-------\n"
        if isinstance(estimacion, dict):
            salida += reporte_memoria_a_texto(estimacion)
        else:
            salida += "Estimacion A   : " + str(estimacion) + " bytes\n"
        salida += "\nMedicion real con tracemalloc:\n"
        salida += "Memoria actual : " + str(mem_actual // 1024) + " KB\n"
        salida += "Memoria pico   : " + str(mem_pico   // 1024) + " KB\n"

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

        return salida


def arbol_a_json_texto(raiz):
    """Convierte un arbol NodoJSON a texto JSON manualmente.

    Funcion independiente para convertir una raiz NodoJSON directamente a texto,
    util cuando no se parte de un diccionario ya transformado por la interfaz.
    """
    def nodo_a_texto(nodo, sangria):
        """Serializa un nodo del arbol usando recursion y sangria manual."""
        if nodo is None:
            return "null"
        s = sangria + "  "                    # Aumenta la sangria del nivel actual.
        resultado = "{\n"                     # Inicio del objeto de nodo.
        resultado += s + '"valor": ' + str(nodo.dato["valor"]) + ",\n"
        resultado += s + '"cantidad": ' + str(nodo.dato["cantidad"]) + ",\n"
        resultado += s + '"izquierda": ' + nodo_a_texto(nodo.izquierda, s) + ",\n" # Rama izquierda.
        resultado += s + '"derecha": ' + nodo_a_texto(nodo.derecha, s) + "\n"      # Rama derecha.
        resultado += sangria + "}"
        return resultado

    texto = "{\n"                              # Objeto raiz del archivo JSON.
    texto += '  "arbol": "Raiz",\n'
    texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
    texto += '  "estructura": ' + nodo_a_texto(raiz, "  ") + "\n"
    texto += "}"
    return texto


# ==============================================================================
# RESUMEN DEL ARCHIVO
# ==============================================================================
# gestor_txt.py contiene utilidades de salida:
# - GestorArchivos crea resultados, guarda matrices TXT y arboles JSON.
# - ConstructorTexto arma el resumen visible con analisis, vectores y memoria.
# - arbol_a_json_texto serializa un arbol NodoJSON de forma recursiva.
# - No modifica la logica algoritmica; solo presenta y persiste resultados.
