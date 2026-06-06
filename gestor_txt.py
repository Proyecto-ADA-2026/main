import os

from logica_arbol import ordenar_ascendente


class GestorArchivos:
    """Maneja la creacion de la carpeta de resultados y la escritura de archivos."""

    CARPETA = "resultados"

    def crear_carpeta(self):
        try:
            os.mkdir(self.CARPETA)
        except:
            pass

    def _ruta(self, nombre_archivo):
        return self.CARPETA + "\\" + nombre_archivo

    def archivo_existe(self, nombre_archivo):
        ruta = self._ruta(nombre_archivo)
        try:
            f = open(ruta, "r", encoding="utf-8")
            f.close()
            return True
        except:
            return False

    def guardar_txt(self, nombre_archivo, contenido):
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)
        f = open(ruta, "w", encoding="utf-8")
        f.write(contenido)
        f.close()

    def guardar_matriz(self, nombre_archivo, matriz, titulo):
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)
        n = len(matriz)
        f = open(ruta, "w", encoding="utf-8")

        f.write(titulo + "\n")
        f.write("Tamano: " + str(n) + "x" + str(n) + "\n")

        sep = ""
        for i in range(60):
            sep += "="
        f.write(sep + "\n\n")

        for fila in matriz:
            linea = ""
            for i in range(len(fila)):
                linea += f"{fila[i]:10}"
                if i < len(fila) - 1:
                    linea += "   "
            f.write(linea + "\n")

        f.close()

    def _nodo_a_texto_json(self, nodo_dict, sangria):
        if nodo_dict is None:
            return "null"

        s = sangria + "  "
        resultado = "{\n"
        resultado += s + '"valor": ' + str(nodo_dict["valor"]) + ",\n"
        resultado += s + '"cantidad": ' + str(nodo_dict["cantidad"]) + ",\n"
        resultado += s + '"izquierda": ' + self._nodo_a_texto_json(nodo_dict["izquierda"], s) + ",\n"
        resultado += s + '"derecha": ' + self._nodo_a_texto_json(nodo_dict["derecha"], s) + "\n"
        resultado += sangria + "}"
        return resultado

    def guardar_arbol_json(self, nombre_archivo, dict_arbol, nombre_id):
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)

        texto = "{\n"
        texto += '  "arbol": "' + nombre_id + '",\n'
        texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
        texto += '  "estructura": '
        texto += self._nodo_a_texto_json(dict_arbol, "  ")
        texto += "\n}"

        f = open(ruta, "w", encoding="utf-8")
        f.write(texto)
        f.close()

    def abrir_archivo(self, nombre_archivo):
        if not self.archivo_existe(nombre_archivo):
            return False
        ruta = self._ruta(nombre_archivo)
        try:
            os.startfile(ruta)
            return True
        except:
            return False


class ConstructorTexto:
    """Genera el texto del panel 'Resumen y analisis' con estructuras de control basicas."""

    def quitar_duplicados(self, lista):
        unicos = []
        for val in lista:
            esta = False
            i = 0
            while i < len(unicos):
                if unicos[i] == val:
                    esta = True
                    break
                i += 1
            if not esta:
                unicos = unicos + [val]
        return unicos

    def lista_a_texto(self, lista, max_mostrar):
        if len(lista) == 0:
            return "  (ninguno)"

        texto = "  "
        total = len(lista)

        if total <= max_mostrar:
            for i in range(total):
                texto += str(lista[i])
                if i < total - 1:
                    texto += ", "
            return texto

        for i in range(max_mostrar):
            texto += str(lista[i])
            if i < max_mostrar - 1:
                texto += ", "
        texto += " ... (+" + str(total - max_mostrar) + " mas)"
        return texto

    def separador_igual(self, longitud):
        linea = ""
        for i in range(longitud):
            linea += "="
        return linea

    def bloque_categoria(self, etiqueta, cantidad, valores):
        unicos = self.quitar_duplicados(valores)
        unicos = ordenar_ascendente(unicos)
        texto = etiqueta + ": " + str(cantidad) + "\n"
        texto += self.lista_a_texto(unicos, 30) + "\n"
        return texto

    def resumen_matriz(self, titulo, analisis):
        sep = self.separador_igual(len(titulo))
        texto = titulo + "\n" + sep + "\n"
        texto += self.bloque_categoria("Pares          ", analisis["pares"]["cantidad"],     analisis["pares"]["valores"])
        texto += self.bloque_categoria("Impares        ", analisis["impares"]["cantidad"],   analisis["impares"]["valores"])
        texto += self.bloque_categoria("Primos         ", analisis["primos"]["cantidad"],    analisis["primos"]["valores"])
        texto += self.bloque_categoria("Perfectos      ", analisis["perfectos"]["cantidad"], analisis["perfectos"]["valores"])
        texto += self.bloque_categoria("Cuadrados perf.", analisis["cuadrados"]["cantidad"], analisis["cuadrados"]["valores"])
        return texto

    def repeticiones_a_texto(self, rep):
        claves = []
        for k in rep:
            claves = claves + [k]
        claves = ordenar_ascendente(claves)

        texto = ""
        for i in range(len(claves)):
            texto += str(claves[i]) + ": " + str(rep[claves[i]])
            if i < len(claves) - 1:
                texto += ", "
        return texto

    def vector_a_texto(self, vector, max_chars):
        texto = "["
        for i in range(len(vector)):
            texto += str(vector[i])
            if i < len(vector) - 1:
                texto += ", "
        texto += "]"
        if len(texto) > max_chars:
            return texto[:max_chars] + "..."
        return texto

    def construir_salida(self, analisis_A, analisis_A3, rep_A, rep_A3,
                          va_asc, va_desc, va3_asc, va3_desc,
                          mem_actual, mem_pico, estimacion):
        salida = ""
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
        salida += "Estimacion A   : " + str(estimacion)         + " bytes\n"
        salida += "Memoria actual : " + str(mem_actual // 1024) + " KB\n"
        salida += "Memoria pico   : " + str(mem_pico   // 1024) + " KB\n"

        return salida


def arbol_a_json_texto(raiz):
    """Convierte un arbol NodoJSON a texto JSON manualmente."""
    def nodo_a_texto(nodo, sangria):
        if nodo is None:
            return "null"
        s = sangria + "  "
        resultado = "{\n"
        resultado += s + '"valor": ' + str(nodo.dato["valor"]) + ",\n"
        resultado += s + '"cantidad": ' + str(nodo.dato["cantidad"]) + ",\n"
        resultado += s + '"izquierda": ' + nodo_a_texto(nodo.izquierda, s) + ",\n"
        resultado += s + '"derecha": ' + nodo_a_texto(nodo.derecha, s) + "\n"
        resultado += sangria + "}"
        return resultado

    texto = "{\n"
    texto += '  "arbol": "Raiz",\n'
    texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
    texto += '  "estructura": ' + nodo_a_texto(raiz, "  ") + "\n"
    texto += "}"
    return texto
