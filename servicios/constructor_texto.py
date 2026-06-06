from Proyecto_final import ordenar_ascendente


class ConstructorTexto:
    """Genera el texto del panel 'Resumen y analisis' con estructuras de control basicas."""

    def quitar_duplicados(self, lista):
        """Elimina valores repetidos de una lista.
        No usa set(): busca con while si el valor ya esta antes de agregarlo.
        """
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
        """Convierte una lista de enteros a string "v1, v2, v3..." sin .join().
        Si hay mas de max_mostrar elementos, muestra los primeros y agrega '... (+N mas)'.
        """
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
        """Genera una linea de '=' de la longitud dada, sin usar el operador '*'."""
        linea = ""
        for i in range(longitud):
            linea += "="
        return linea

    def bloque_categoria(self, etiqueta, cantidad, valores):
        """Genera dos lineas para una categoria: 'Etiqueta: N' y '  v1, v2...'"""
        unicos = self.quitar_duplicados(valores)
        unicos = ordenar_ascendente(unicos)
        texto  = etiqueta + ": " + str(cantidad) + "\n"
        texto += self.lista_a_texto(unicos, 30) + "\n"
        return texto

    def resumen_matriz(self, titulo, analisis):
        """Genera el bloque completo de resumen para una matriz (A o A3)."""
        sep   = self.separador_igual(len(titulo))
        texto = titulo + "\n" + sep + "\n"
        texto += self.bloque_categoria("Pares          ", analisis["pares"]["cantidad"],     analisis["pares"]["valores"])
        texto += self.bloque_categoria("Impares        ", analisis["impares"]["cantidad"],   analisis["impares"]["valores"])
        texto += self.bloque_categoria("Primos         ", analisis["primos"]["cantidad"],    analisis["primos"]["valores"])
        texto += self.bloque_categoria("Perfectos      ", analisis["perfectos"]["cantidad"], analisis["perfectos"]["valores"])
        texto += self.bloque_categoria("Cuadrados perf.", analisis["cuadrados"]["cantidad"], analisis["cuadrados"]["valores"])
        return texto

    def repeticiones_a_texto(self, rep):
        """Convierte el dict de repeticiones a string 'v: n, v: n...'
        Extrae claves con for (sin .keys() ni list()), ordena y concatena con +=.
        """
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
        """Convierte un vector a string '[v1, v2, v3]' con limite de caracteres.
        Sin str(lista) ni .join(). Construye el string con for e if.
        """
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
        """Construye el texto completo del panel de resultados.
        Solo usa +=, for e if. Sin .append(), .join() ni str(lista).
        """
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
