import os


class GestorArchivos:
    """Maneja la creacion de la carpeta de resultados y la escritura de archivos.

    Reglas:
      - No usa os.makedirs  -> os.mkdir en try/except
      - No usa os.path.join -> concatenacion de strings con +
      - No usa os.path.exists -> open() en try/except
      - No usa json.dump    -> _nodo_a_texto_json() escribe el JSON manualmente
    """

    CARPETA = "resultados"           # Carpeta donde se guardan todos los archivos generados

    def crear_carpeta(self):
        """Crea la carpeta 'resultados' si no existe.
        Usa os.mkdir en try/except: si ya existe, el error se ignora.
        """
        try:
            os.mkdir(self.CARPETA)   # Intenta crear la carpeta
        except:
            pass                     # Si ya existe o hay otro error, lo ignora silenciosamente

    def _ruta(self, nombre_archivo):
        """Construye la ruta completa sin os.path.join: concatena carpeta + nombre."""
        return self.CARPETA + "\\" + nombre_archivo  # Barra invertida de Windows

    def archivo_existe(self, nombre_archivo):
        """Verifica si un archivo existe intentando abrirlo en lectura (sin os.path.exists)."""
        ruta = self._ruta(nombre_archivo)
        try:
            f = open(ruta, "r", encoding="utf-8")  # Intenta abrir el archivo en lectura
            f.close()                               # Si se pudo abrir, lo cierra de inmediato
            return True                             # El archivo existe
        except:
            return False                            # No se pudo abrir: el archivo no existe

    def guardar_txt(self, nombre_archivo, contenido):
        """Guarda un string de texto en un archivo .txt dentro de 'resultados'."""
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)
        f = open(ruta, "w", encoding="utf-8")       # Abre en modo escritura
        f.write(contenido)                          # Escribe el contenido
        f.close()                                   # Cierra el archivo manualmente

    def guardar_matriz(self, nombre_archivo, matriz, titulo):
        """Guarda una matriz completa en un archivo .txt con encabezado.
        Construye cada linea con for e if, sin .join().
        """
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)
        n = len(matriz)
        f = open(ruta, "w", encoding="utf-8")

        f.write(titulo + "\n")
        f.write("Tamano: " + str(n) + "x" + str(n) + "\n")

        sep = ""
        for i in range(60):                         # Construye "=" x 60 con for, sin "*"
            sep += "="
        f.write(sep + "\n\n")

        for fila in matriz:                         # Recorre cada fila
            linea = ""
            for i in range(len(fila)):              # Recorre cada elemento de la fila
                linea += f"{fila[i]:10}"            # Formato 10 caracteres por numero
                if i < len(fila) - 1:              # Si no es el ultimo
                    linea += "   "                  # Tres espacios entre columnas
            f.write(linea + "\n")

        f.close()

    def _nodo_a_texto_json(self, nodo_dict, sangria):
        """Convierte recursivamente un nodo del arbol a texto JSON sin json.dump.

        Caso base : nodo_dict es None -> devuelve "null"
        Caso rec. : dict con valor/cantidad/izquierda/derecha -> objeto JSON anidado

        Parametros:
          nodo_dict : dict {"valor", "cantidad", "izquierda", "derecha"} o None
          sangria   : string de espacios para la indentacion del nivel actual
        """
        if nodo_dict is None:                       # Nodo vacio -> JSON null
            return "null"

        s = sangria + "  "                          # Sangria del nivel hijo (2 espacios mas)
        resultado = "{\n"
        resultado += s + '"valor": '     + str(nodo_dict["valor"])     + ",\n"
        resultado += s + '"cantidad": '  + str(nodo_dict["cantidad"])  + ",\n"
        resultado += s + '"izquierda": ' + self._nodo_a_texto_json(nodo_dict["izquierda"], s) + ",\n"
        resultado += s + '"derecha": '   + self._nodo_a_texto_json(nodo_dict["derecha"],   s) + "\n"
        resultado += sangria + "}"
        return resultado

    def guardar_arbol_json(self, nombre_archivo, dict_arbol, nombre_id):
        """Escribe el arbol BST como archivo .json construido manualmente con +=."""
        self.crear_carpeta()
        ruta = self._ruta(nombre_archivo)

        texto = "{\n"
        texto += '  "arbol": "' + nombre_id + '",\n'
        texto += '  "descripcion": "BST equilibrado. Nodos: valor, cantidad, izquierda, derecha.",\n'
        texto += '  "estructura": '
        texto += self._nodo_a_texto_json(dict_arbol, "  ")  # JSON del arbol recursivo
        texto += "\n}"

        f = open(ruta, "w", encoding="utf-8")
        f.write(texto)
        f.close()

    def abrir_archivo(self, nombre_archivo):
        """Abre un archivo de 'resultados' con el programa predeterminado del SO.
        Devuelve True si pudo, False si el archivo no existe.
        """
        if not self.archivo_existe(nombre_archivo):
            return False
        ruta = self._ruta(nombre_archivo)
        try:
            os.startfile(ruta)                      # Abre con el programa predeterminado (Bloc de notas, etc.)
            return True
        except:
            return False
