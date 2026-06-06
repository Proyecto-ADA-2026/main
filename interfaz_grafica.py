"""
interfaz_grafica.py
Frontend del proyecto: ventana grafica, botones y visualizacion de resultados.
Backend (algoritmos puros): Proyecto_final.py

"""

import tkinter as tk                 # Libreria para crear la ventana grafica en escritorio
from tkinter import ttk, messagebox  # ttk = widgets modernos; messagebox = dialogos de alerta
import os                            # Solo se usa os.mkdir y os.startfile (no hay alternativa pura en Python)

MAX_N = 150                          # Tamano maximo de n (A3 cuesta O(n3) en tiempo y O(n2) en memoria)

try:
    import tksheet                   # Hoja de calculo interactiva (opcional)
    TKSHEET_DISPONIBLE = True
except ImportError:
    TKSHEET_DISPONIBLE = False       # Si no esta instalada, los botones de tabla mostraran aviso

from Proyecto_final import (
    crear_matriz,                     # Genera matriz n*n con numeros aleatorios 0-9
    calcular_A3,                      # Calcula A3 = A*A*A con multiplicacion propia O(n3)
    guardar_A3_directo_txt,           # Calcula y guarda A3 fila por fila para matrices grandes
    analizar_matriz,                  # Clasifica cada elemento: par, impar, primo, perfecto, cuadrado
    contar_repeticiones,              # Cuenta cuantas veces aparece cada valor en la matriz
    frecuencias_a_json_ordenado,      # Convierte el dict de frecuencias a lista de dicts ordenada
    matriz_a_vector,                  # Aplana la matriz n*n en un vector de n2 elementos
    ordenar_ascendente,               # Ordena de menor a mayor (algoritmo propio, sin sorted())
    invertir_vector,                  # Invierte el vector para obtener el orden descendente
    construir_arbol_json_equilibrado, # Construye BST equilibrado desde lista ordenada
    buscar_y_contar_en_matriz,        # Busqueda lineal O(n2) en la matriz con conteo
    buscar_en_arbol_json,             # Busqueda binaria O(log n) en el arbol BST
    medir_tiempo,                     # Mide nanosegundos que tarda una funcion
    arbol_a_ascii,                    # Convierte el arbol a dibujo ASCII con ramas / y \
    iniciar_medicion_memoria,         # Inicia tracemalloc para medir RAM usada
    obtener_memoria_actual_y_pico,    # Lee uso actual y pico de RAM desde tracemalloc
    detener_medicion_memoria,         # Detiene tracemalloc y libera sus recursos
    estimar_memoria_matriz,           # Estimacion teorica de bytes que ocupa la matriz
    contar_nodos_arbol_json,          # Cuenta todos los nodos del arbol recursivamente
    altura_arbol_json,                # Calcula la altura (niveles) del arbol
    recorrido_inorden_json,           # Recorre el arbol en inorden (menor a mayor)
)


# ================================================================
# CLASE: GestorArchivos
# Responsabilidad: toda la escritura y lectura de archivos.
# No usa os.makedirs, os.path.exists, os.path.join ni json.dump.
# ================================================================

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
        resultado += sangria + "}"                  # Cierra el objeto JSON
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


# ================================================================
# CLASE: ConstructorTexto
# Responsabilidad: construir el string del panel de resultados.
# Sin .append(), .join(), set(). Solo for, while, if, +=.
# ================================================================

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
            while i < len(unicos):                 # Busca manualmente si ya fue agregado
                if unicos[i] == val:
                    esta = True
                    break
                i += 1
            if not esta:
                unicos = unicos + [val]             # Concatenacion en lugar de .append()
        return unicos

    def lista_a_texto(self, lista, max_mostrar):
        """Convierte una lista de enteros a string "v1, v2, v3..." sin .join().
        Si hay mas de max_mostrar elementos, muestra los primeros y agrega '... (+N mas)'.
        """
        if len(lista) == 0:
            return "  (ninguno)"

        texto = "  "                               # Sangria al inicio
        total = len(lista)

        if total <= max_mostrar:
            for i in range(total):
                texto += str(lista[i])
                if i < total - 1:
                    texto += ", "
            return texto

        for i in range(max_mostrar):               # Solo los primeros max_mostrar
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
        unicos = self.quitar_duplicados(valores)   # Elimina duplicados manualmente
        unicos = ordenar_ascendente(unicos)        # Ordena con el algoritmo propio del backend
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
        for k in rep:                              # Itera sobre las claves del dict
            claves = claves + [k]                  # Sin .append()
        claves = ordenar_ascendente(claves)        # Ordena las claves

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


# ================================================================
# CLASE: VisualizadorArbol
# Responsabilidad: Dibujar graficamente el arbol BST en un Canvas.
# Sin .append(), sin .join(), sin set().
# ================================================================

class VisualizadorArbol(tk.Toplevel):
    """Ventana emergente para visualizar el arbol BST graficamente con nodos y lineas."""

    def __init__(self, padre, raiz, titulo):
        super().__init__(padre)
        self.title(titulo)
        self.geometry("1100x750")
        self.configure(bg="#121214")
        self.minsize(800, 600)

        # Hacer la ventana flotante sobre el padre
        self.transient(padre)

        self.raiz = raiz
        self.nodos_ovales = {}
        self.nodos_datos = {}

        # Contenedor principal con scrollbars
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        sb_y = ttk.Scrollbar(frame, orient="vertical")
        sb_x = ttk.Scrollbar(frame, orient="horizontal")

        self.canvas = tk.Canvas(
            frame,
            bg="#121214",
            xscrollcommand=sb_x.set,
            yscrollcommand=sb_y.set,
            highlightthickness=0
        )

        sb_y.config(command=self.canvas.yview)
        sb_x.config(command=self.canvas.xview)

        sb_y.pack(side="right", fill="y")
        sb_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Barra de informacion al pasar el mouse por encima de los nodos
        self.lbl_info = tk.Label(
            self,
            text="Pasa el mouse sobre un nodo para ver mas informacion. Usa las barras para desplazarte.",
            bg="#1c1c1f",
            fg="#a1a1aa",
            font=("Segoe UI", 10, "bold"),
            pady=8
        )
        self.lbl_info.pack(fill="x")

        # Dibujar el arbol
        self.graficar()

    def _calcular_altura(self, nodo):
        """Calcula la altura maxima de forma recursiva sin max()."""
        if nodo is None:
            return 0
        h_izq = self._calcular_altura(nodo.izquierda)
        h_der = self._calcular_altura(nodo.derecha)
        if h_izq > h_der:
            return h_izq + 1
        return h_der + 1

    def _calcular_posiciones(self, nodo, depth, coordenadas, contador):
        """Calcula las posiciones de cada nodo usando recorrido inorden."""
        if nodo is None:
            return contador
        # Rama izquierda
        contador = self._calcular_posiciones(nodo.izquierda, depth + 1, coordenadas, contador)

        # Nodo actual
        x = 60 + contador * 90
        y = 60 + depth * 90
        coordenadas[id(nodo)] = (x, y)
        self.nodos_datos[id(nodo)] = nodo.dato
        contador += 1

        # Rama derecha
        contador = self._calcular_posiciones(nodo.derecha, depth + 1, coordenadas, contador)
        return contador

    def _dibujar(self, nodo, coordenadas):
        """Dibuja de forma recursiva lineas y luego nodos (ovalos + textos)."""
        if nodo is None:
            return
        x, y = coordenadas[id(nodo)]

        # 1. Dibujar lineas de conexion primero (para que queden por debajo del circulo del nodo)
        if nodo.izquierda is not None:
            x_izq, y_izq = coordenadas[id(nodo.izquierda)]
            self.canvas.create_line(x, y, x_izq, y_izq, fill="#3f3f46", width=2)
            self._dibujar(nodo.izquierda, coordenadas)

        if nodo.derecha is not None:
            x_der, y_der = coordenadas[id(nodo.derecha)]
            self.canvas.create_line(x, y, x_der, y_der, fill="#3f3f46", width=2)
            self._dibujar(nodo.derecha, coordenadas)

        # 2. Dibujar circulo del nodo
        r = 24
        oval_id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="#1e3a8a",
            outline="#3b82f6",
            width=2.5
        )
        self.nodos_ovales[id(nodo)] = oval_id

        # 3. Dibujar el texto del valor y repeticiones
        valor = nodo.dato["valor"]
        cant = nodo.dato["cantidad"]
        texto = str(valor) + "\n(" + str(cant) + ")"
        text_id = self.canvas.create_text(
            x, y,
            text=texto,
            fill="#f8fafc",
            font=("Segoe UI", 9, "bold"),
            justify="center"
        )

        # 4. Vincular eventos hover
        self.canvas.tag_bind(oval_id, "<Enter>", lambda e, nid=id(nodo): self.al_entrar(nid))
        self.canvas.tag_bind(oval_id, "<Leave>", lambda e, nid=id(nodo): self.al_salir(nid))
        self.canvas.tag_bind(text_id, "<Enter>", lambda e, nid=id(nodo): self.al_entrar(nid))
        self.canvas.tag_bind(text_id, "<Leave>", lambda e, nid=id(nodo): self.al_salir(nid))

    def al_entrar(self, nid):
        """Cambia el color del nodo enfocado a verde esmeralda y actualiza la barra."""
        oval_id = self.nodos_ovales[nid]
        self.canvas.itemconfig(oval_id, fill="#047857", outline="#34d399")

        dato = self.nodos_datos[nid]
        val = dato["valor"]
        cant = dato["cantidad"]
        self.lbl_info.config(
            text="Nodo enfocado -> Valor: " + str(val) + " | Repeticiones en la matriz: " + str(cant),
            fg="#34d399"
        )

    def al_salir(self, nid):
        """Restaura el color original del nodo y limpia la barra."""
        oval_id = self.nodos_ovales[nid]
        self.canvas.itemconfig(oval_id, fill="#1e3a8a", outline="#3b82f6")

        self.lbl_info.config(
            text="Pasa el mouse sobre un nodo para ver mas informacion. Usa las barras para desplazarte.",
            fg="#a1a1aa"
        )

    def graficar(self):
        """Dibuja el arbol calculando dimensiones y configurando el scrollregion."""
        if self.raiz is None:
            self.canvas.create_text(
                200, 100,
                text="El arbol esta vacio. Primero genera la matriz.",
                fill="#f8fafc",
                font=("Segoe UI", 12)
            )
            return

        coordenadas = {}

        # Contar total de nodos de forma recursiva
        def contar(n):
            if n is None:
                return 0
            return 1 + contar(n.izquierda) + contar(n.derecha)

        total_nodos = contar(self.raiz)
        altura = self._calcular_altura(self.raiz)

        # 1. Calcular coordenadas
        self._calcular_posiciones(self.raiz, 0, coordenadas, 0)

        # 2. Dibujar
        self._dibujar(self.raiz, coordenadas)

        # 3. Ajustar limites de desplazamiento
        ancho = 120 + total_nodos * 90
        alto = 120 + altura * 90
        self.canvas.config(scrollregion=(0, 0, ancho, alto))


# ================================================================
# CLASE: App (ventana principal)
# Responsabilidad: construir la GUI y manejar los eventos del usuario.
# ================================================================

class App(tk.Tk):
    """Ventana principal de la aplicacion. Hereda de tk.Tk."""

    def __init__(self):
        """Constructor: inicializa la ventana, crea los objetos auxiliares y construye la UI."""
        super().__init__()                          # Llama al constructor de tk.Tk

        self.title("Analisis de Matriz A, A3 y Arbol Binario")
        self.geometry("1280x820")
        self.minsize(1080, 720)
        self.configure(bg="#f4f6f9")

        # Variables de estado
        self.A        = None                        # Matriz A generada
        self.A3       = None                        # Matriz A3 calculada
        self.arbol_A  = None                        # Raiz del BST de A
        self.arbol_A3 = None                        # Raiz del BST de A3

        # Objetos auxiliares (separacion de responsabilidades)
        self.gestor      = GestorArchivos()         # Maneja archivos
        self.constructor = ConstructorTexto()        # Construye el texto del resumen

        self._estilos()
        self._construir_ui()

    # ── Estilos visuales ────────────────────────────────────────

    def _estilos(self):
        """Configura el tema visual de todos los widgets ttk."""
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Main.TFrame",   background="#f4f6f9")
        s.configure("Header.TFrame", background="#1f4e79")
        s.configure("Header.TLabel",    background="#1f4e79", foreground="white",   font=("Segoe UI", 18, "bold"))
        s.configure("HeaderSub.TLabel", background="#1f4e79", foreground="#d9e8f5", font=("Segoe UI", 10))
        s.configure("Card.TLabelframe",       background="#ffffff", borderwidth=1, relief="solid")
        s.configure("Card.TLabelframe.Label", background="#f4f6f9", foreground="#1f4e79", font=("Segoe UI", 11, "bold"))
        s.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
        s.configure("TEntry", padding=6,             font=("Segoe UI", 10))
        s.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#1f4e79", foreground="white")
        s.map("Primary.TButton", background=[("active", "#173a5c")], foreground=[("active", "white")])
        s.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(12, 6))

    # ── Construccion de la interfaz ──────────────────────────────

    def _construir_ui(self):
        """Crea y posiciona todos los widgets de la ventana principal."""

        principal = ttk.Frame(self, style="Main.TFrame")
        principal.pack(fill="both", expand=True)

        # Header azul oscuro
        header = ttk.Frame(principal, style="Header.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text="Matriz A, A3 y Arbol Binario",
                  style="Header.TLabel").pack(anchor="w", padx=20, pady=(14, 2))
        ttk.Label(header, text="Generacion, analisis, ordenamiento y busqueda comparativa",
                  style="HeaderSub.TLabel").pack(anchor="w", padx=20, pady=(0, 14))

        # Fila superior: campo n + boton Generar
        top = ttk.Frame(principal, style="Main.TFrame")
        top.pack(fill="x", padx=20, pady=(14, 6))
        ttk.Label(top, text="Tamano n (n >= 4):").pack(side="left")
        self.entry_n = ttk.Entry(top, width=10)
        self.entry_n.pack(side="left", padx=8)
        self.entry_n.insert(0, "4")
        ttk.Button(top, text="Generar matriz A y A3",
                   style="Primary.TButton",
                   command=self.generar).pack(side="left", padx=10)
        tk.Label(top, text="(Si n > 20 se muestra vista previa y se guarda en .txt)",
                 bg="#f4f6f9", fg="#666666", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # Botones secundarios
        bf = ttk.Frame(principal, style="Main.TFrame")
        bf.pack(fill="x", padx=20, pady=(0, 10))
        ttk.Button(bf, text="Abrir TXT A",       command=lambda: self._abrir("matriz_A.txt")).pack(side="left",  padx=5)
        ttk.Button(bf, text="Abrir TXT A3",      command=lambda: self._abrir("matriz_A3.txt")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver JSON Arbol A",  command=lambda: self._abrir("arbol_A.json")).pack(side="left",  padx=5)
        ttk.Button(bf, text="Ver Grafico Arbol A",  command=lambda: self._mostrar_grafico_arbol("Grafico Arbol A",  self.arbol_A)).pack(side="left",  padx=5)
        ttk.Button(bf, text="Ver JSON Arbol A3", command=lambda: self._abrir("arbol_A3.json")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver Grafico Arbol A3", command=lambda: self._mostrar_grafico_arbol("Grafico Arbol A3", self.arbol_A3)).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver tabla A",       command=lambda: self._mostrar_tabla("Matriz A",  self.A)).pack(side="left",  padx=5)
        ttk.Button(bf, text="Ver tabla A3",      command=lambda: self._mostrar_tabla("Matriz A3", self.A3)).pack(side="left", padx=5)

        # Panel de busqueda
        pf = tk.LabelFrame(principal, text="Busqueda",
                            bg="#f4f6f9", fg="#333333", font=("Segoe UI", 9))
        pf.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(pf, text="Numero a buscar:", bg="#f4f6f9", fg="#222222",
                 font=("Segoe UI", 9)).pack(side="left", padx=(12, 5), pady=8)
        self.entry_buscado = tk.Entry(pf, width=10, font=("Segoe UI", 9),
                                       bg="white", fg="black", relief="solid", bd=1)
        self.entry_buscado.pack(side="left", padx=5)
        tk.Button(pf, text="Buscar en matriz y arbol",
                  command=self.buscar,
                  font=("Segoe UI", 9), bg="#f5f5f5", fg="#111111",
                  activebackground="#e6e6e6", relief="raised",
                  bd=1, padx=8, pady=2, cursor="hand2").pack(side="left", padx=10)

        # Area central: matrices (izq) + resumen (der)
        centro = ttk.Frame(principal, style="Main.TFrame")
        centro.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        izq = ttk.LabelFrame(centro, text="Matrices generadas", style="Card.TLabelframe")
        izq.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.notebook = ttk.Notebook(izq)
        self.tab_A    = ttk.Frame(self.notebook)
        self.tab_A3   = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_A,  text="Matriz A")
        self.notebook.add(self.tab_A3, text="Matriz A3")
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)
        self.text_A  = self._text_scroll(self.tab_A)
        self.text_A3 = self._text_scroll(self.tab_A3)

        der = ttk.LabelFrame(centro, text="Resumen y analisis", style="Card.TLabelframe")
        der.pack(side="left", fill="both", expand=False)
        self.txt_result = tk.Text(der, width=50, height=24, wrap="word",
                                   font=("Consolas", 10), bg="#ffffff", fg="#222222",
                                   relief="flat", padx=10, pady=10)
        sb_r = ttk.Scrollbar(der, orient="vertical", command=self.txt_result.yview)
        self.txt_result.configure(yscrollcommand=sb_r.set)
        self.txt_result.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        sb_r.pack(side="right", fill="y", padx=(0, 8), pady=8)
        self.txt_result.insert("1.0", "Aqui aparecera el resumen.\n\nPrimero genera la matriz.")
        self.txt_result.config(state="disabled")

        # Panel del arbol ASCII
        af = ttk.LabelFrame(principal, text="Arbol binario de busqueda (A y A3)",
                             style="Card.TLabelframe")
        af.pack(fill="both", expand=False, padx=20, pady=(0, 10))
        self.txt_arbol = tk.Text(af, height=10, wrap="none",
                                  font=("Consolas", 12), bg="#fbfbfb", fg="#1e1e1e",
                                  relief="flat", padx=10, pady=10)
        sb_ay = ttk.Scrollbar(af, orient="vertical",   command=self.txt_arbol.yview)
        sb_ax = ttk.Scrollbar(af, orient="horizontal", command=self.txt_arbol.xview)
        self.txt_arbol.configure(yscrollcommand=sb_ay.set, xscrollcommand=sb_ax.set)
        self.txt_arbol.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=(8, 0))
        sb_ay.grid(row=0, column=1, sticky="ns",  padx=(0, 8), pady=(8, 0))
        sb_ax.grid(row=1, column=0, sticky="ew",  padx=(8, 0), pady=(0, 8))
        af.rowconfigure(0, weight=1)
        af.columnconfigure(0, weight=1)
        self.txt_arbol.insert("1.0", "Aqui se mostrara el arbol binario.\n(primero A, luego A3).")
        self.txt_arbol.config(state="disabled")

        # Barra de estado
        self.status = tk.Label(principal, text="Estado: esperando datos...",
                               anchor="w", bg="#e8eef3", fg="#333333",
                               font=("Segoe UI", 10, "bold"))
        self.status.pack(fill="x", padx=20, pady=(0, 12), ipady=6)

    # ── Metodos auxiliares de widgets ────────────────────────────

    def _text_scroll(self, parent):
        """Crea un widget Text con barras de scroll horizontal y vertical."""
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        text = tk.Text(frame, wrap="none", font=("Consolas", 11),
                       bg="#fbfbfb", fg="#1f1f1f", relief="flat", padx=10, pady=10)
        sby = ttk.Scrollbar(frame, orient="vertical",   command=text.yview)
        sbx = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=sby.set, xscrollcommand=sbx.set)
        text.grid(row=0, column=0, sticky="nsew")
        sby.grid(row=0, column=1, sticky="ns")
        sbx.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        text.config(state="disabled")
        return text

    def _set_text(self, widget, contenido):
        """Reemplaza todo el contenido de un widget Text."""
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", contenido)
        widget.config(state="disabled")

    def _add_text(self, widget, contenido):
        """Agrega texto al final de un widget Text sin borrar el existente."""
        widget.config(state="normal")
        widget.insert("end", contenido)
        widget.see("end")
        widget.config(state="disabled")

    def _abrir(self, nombre_archivo):
        """Abre un archivo de resultados con el programa predeterminado del SO."""
        ok = self.gestor.abrir_archivo(nombre_archivo)
        if not ok:
            messagebox.showwarning("Archivo no encontrado",
                                   "Primero genera la matriz para crear el archivo.")

    def _mostrar_tabla(self, titulo, matriz):
        """Abre la matriz en una ventana emergente como tabla interactiva."""
        if matriz is None:
            messagebox.showwarning("Sin datos", "Primero genera la matriz.")
            return
        if not TKSHEET_DISPONIBLE:
            messagebox.showinfo("tksheet no disponible",
                                "Instala tksheet o abre el archivo .txt.")
            return
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("900x600")
        hoja = tksheet.Sheet(ventana, data=matriz)
        hoja.pack(fill="both", expand=True)
        hoja.enable_bindings(("single_select", "row_select",
                               "column_width_resize", "arrowkeys",
                               "right_click_popup_menu"))

    def _mostrar_grafico_arbol(self, titulo, raiz_arbol):
        """Abre la ventana emergente con la visualizacion grafica del arbol."""
        if raiz_arbol is None:
            messagebox.showwarning("Sin datos", "Primero genera la matriz para construir el arbol.")
            return
        VisualizadorArbol(self, raiz_arbol, titulo)

    def _mat_to_str(self, M, lim=10):
        """Convierte la matriz M a texto para mostrar en pantalla.
        n > 20: vista previa lim x lim.
        n <= 20: muestra la matriz completa.
        Usa for, if y +=. Sin .join() ni str(lista).
        """
        n = len(M)
        resultado = ""

        if n > 20:
            l = lim if lim < n else n
            for i in range(l):
                for j in range(l):
                    resultado += f"{M[i][j]:6}"
                    if j < l - 1:
                        resultado += "   "
                if i < l - 1:
                    resultado += "\n"
            resultado += "\n\n( Vista previa: " + str(l) + "x" + str(l)
            resultado += " de " + str(n) + "x" + str(n) + " )"
            return resultado

        for i in range(n):
            for j in range(n):
                resultado += f"{M[i][j]:6}"
                if j < n - 1:
                    resultado += "   "
            if i < n - 1:
                resultado += "\n"
        return resultado

    def _arbol_a_dict(self, nodo):
        """Convierte el arbol BST (NodoJSON) a diccionario Python de forma recursiva.
        NodoJSON tiene: nodo.dato = {"valor": num, "cantidad": freq}.
        """
        if nodo is None:
            return None
        return {
            "valor":     nodo.dato["valor"],
            "cantidad":  nodo.dato["cantidad"],
            "izquierda": self._arbol_a_dict(nodo.izquierda),
            "derecha":   self._arbol_a_dict(nodo.derecha),
        }

    def _limpiar_texto(self, texto):
        """Quita espacios al inicio y al final del string sin usar .strip().
        Avanza con while desde los dos extremos.
        """
        i = 0
        while i < len(texto) and texto[i] == " ":
            i += 1
        j = len(texto) - 1
        while j >= 0 and texto[j] == " ":
            j -= 1
        if i > j:
            return ""
        return texto[i:j + 1]

    def _es_entero(self, texto):
        """Verifica si un string es un numero entero valido sin int() previo.
        Recorre caracter a caracter comparando con '0' y '9'.
        """
        if len(texto) == 0:
            return False
        inicio = 0
        if texto[0] == "-":
            inicio = 1
        if inicio == len(texto):
            return False
        i = inicio
        while i < len(texto):
            if texto[i] < "0" or texto[i] > "9":
                return False
            i += 1
        return True

    # ── Accion: GENERAR ─────────────────────────────────────────

    def generar(self):
        """Genera A, calcula A3, analiza, construye arboles BST y muestra todo."""

        # Validar n
        texto_n = self._limpiar_texto(self.entry_n.get())
        if not self._es_entero(texto_n):
            messagebox.showerror("Error", "Ingrese un valor entero para n.")
            return
        n = int(texto_n)

        if n < 4:
            messagebox.showerror("Error", "n debe ser mayor o igual a 4.")
            return
        if n > MAX_N:
            messagebox.showerror("Error",
                "n supera el limite de " + str(MAX_N) +
                ". El calculo de A3 (O(n3)) consumiria demasiada RAM.")
            return
        if n > 20:
            ok = messagebox.askyesno("Advertencia",
                "n es grande. Se mostrara vista previa y se guardaran archivos .txt. Continuar?")
            if not ok:
                return

        self.status.config(text="Estado: generando matriz y calculando A3...")
        self.update_idletasks()

        try:
            # Paso 1: crear A y calcular A3
            iniciar_medicion_memoria()
            self.A = crear_matriz(n)

            if n > 100:
                self.gestor.guardar_matriz("matriz_A.txt", self.A, "Matriz A")
                self.status.config(text="Estado: guardando A3 fila por fila...")
                self.update_idletasks()
                ruta_a3 = self.gestor.CARPETA + "\\" + "matriz_A3.txt"
                self.A3 = guardar_A3_directo_txt(self.A, ruta_a3)
            else:
                self.A3 = calcular_A3(self.A)
                self.gestor.guardar_matriz("matriz_A.txt",  self.A,  "Matriz A")
                self.gestor.guardar_matriz("matriz_A3.txt", self.A3, "Matriz A3")

            # Paso 2: analizar
            analisis_A  = analizar_matriz(self.A)
            analisis_A3 = analizar_matriz(self.A3)

            # Paso 3: repeticiones
            rep_A  = contar_repeticiones(self.A)
            rep_A3 = contar_repeticiones(self.A3)

            # Paso 4: construir BST
            lista_A  = frecuencias_a_json_ordenado(rep_A)
            self.arbol_A  = construir_arbol_json_equilibrado(lista_A,  0, len(lista_A)  - 1)
            lista_A3 = frecuencias_a_json_ordenado(rep_A3)
            self.arbol_A3 = construir_arbol_json_equilibrado(lista_A3, 0, len(lista_A3) - 1)

            # Paso 5: vectores ordenados
            vec_A   = matriz_a_vector(self.A)
            vec_A3  = matriz_a_vector(self.A3)
            va_asc  = ordenar_ascendente(vec_A)
            va3_asc = ordenar_ascendente(vec_A3)
            va_desc = invertir_vector(va_asc)
            va3_desc= invertir_vector(va3_asc)

            # Paso 6: mostrar matrices
            self._set_text(self.text_A,  self._mat_to_str(self.A))
            self._set_text(self.text_A3, self._mat_to_str(self.A3))

            # Paso 7: arbol ASCII
            if len(lista_A) <= 63:
                ascii_A = arbol_a_ascii(self.arbol_A)
            else:
                ascii_A = "Arbol A generado (" + str(len(lista_A)) + " nodos). Busqueda disponible."
            if len(lista_A3) <= 63:
                ascii_A3 = arbol_a_ascii(self.arbol_A3)
            else:
                ascii_A3 = "Arbol A3 generado (" + str(len(lista_A3)) + " nodos). Busqueda disponible."
            self._set_text(self.txt_arbol,
                           "ARBOL A:\n" + ascii_A + "\n\nARBOL A3:\n" + ascii_A3)

            # Paso 8: memoria
            mem_actual, mem_pico = obtener_memoria_actual_y_pico()
            detener_medicion_memoria()
            estimacion = estimar_memoria_matriz(n)

            # Paso 9: resumen en el panel
            salida = self.constructor.construir_salida(
                analisis_A, analisis_A3, rep_A, rep_A3,
                va_asc, va_desc, va3_asc, va3_desc,
                mem_actual, mem_pico, estimacion
            )
            self._set_text(self.txt_result, salida)

            # Paso 10: guardar JSON del arbol manualmente
            self.gestor.guardar_arbol_json("arbol_A.json",  self._arbol_a_dict(self.arbol_A),  "ArbolA")
            self.gestor.guardar_arbol_json("arbol_A3.json", self._arbol_a_dict(self.arbol_A3), "ArbolA3")

            if n > 20:
                self.status.config(text="Estado: generado. Vista previa en pantalla. Archivos en /resultados.")
            else:
                self.status.config(text="Estado: generado correctamente. Ya puedes buscar un numero.")

        except Exception as e:
            messagebox.showerror("Error", "Ocurrio un problema al generar:\n" + str(e))
            self.status.config(text="Estado: error al generar.")

    # ── Accion: BUSCAR ──────────────────────────────────────────

    def buscar(self):
        """Busca un numero en la matriz y en el arbol BST, mide tiempos y compara."""
        if self.A is None or self.A3 is None or self.arbol_A is None or self.arbol_A3 is None:
            messagebox.showwarning("Aviso", "Primero genera la matriz A y A3.")
            return

        texto_b = self._limpiar_texto(self.entry_buscado.get())
        if not self._es_entero(texto_b):
            messagebox.showerror("Error", "Ingrese un numero entero para buscar.")
            return
        buscado = int(texto_b)

        self.status.config(text="Estado: buscando...")
        self.update_idletasks()

        # Busquedas en A
        res_mat_A,  t_mat_A  = medir_tiempo(buscar_y_contar_en_matriz, self.A,        buscado)
        enc_mat_A, cant_mat_A = res_mat_A
        res_arb_A,  t_arb_A  = medir_tiempo(buscar_en_arbol_json,      self.arbol_A,  buscado)

        # Busquedas en A3
        res_mat_A3, t_mat_A3  = medir_tiempo(buscar_y_contar_en_matriz, self.A3,       buscado)
        enc_mat_A3, cant_mat_A3 = res_mat_A3
        res_arb_A3, t_arb_A3  = medir_tiempo(buscar_en_arbol_json,     self.arbol_A3,  buscado)

        if res_arb_A is not None:
            cant_arb_A = res_arb_A["cantidad"]
        else:
            cant_arb_A = 0

        if res_arb_A3 is not None:
            cant_arb_A3 = res_arb_A3["cantidad"]
        else:
            cant_arb_A3 = 0

        # Estado de cada busqueda (sin operador ternario en una sola linea)
        if enc_mat_A:
            txt_mat_A = "encontrado"
        else:
            txt_mat_A = "no encontrado"
        if res_arb_A is not None:
            txt_arb_A = "encontrado"
        else:
            txt_arb_A = "no encontrado"
        if t_arb_A < t_mat_A:
            rapido_A = "arbol BST"
        elif t_mat_A < t_arb_A:
            rapido_A = "matriz"
        else:
            rapido_A = "empate"

        if enc_mat_A3:
            txt_mat_A3 = "encontrado"
        else:
            txt_mat_A3 = "no encontrado"
        if res_arb_A3 is not None:
            txt_arb_A3 = "encontrado"
        else:
            txt_arb_A3 = "no encontrado"
        if t_arb_A3 < t_mat_A3:
            rapido_A3 = "arbol BST"
        elif t_mat_A3 < t_arb_A3:
            rapido_A3 = "matriz"
        else:
            rapido_A3 = "empate"

        # Construye el mensaje de resultado con +=
        msg = "\n\nBUSQUEDA: " + str(buscado) + "\n"
        msg += "-------------------\n"
        msg += "Matriz A:\n"
        msg += "  En matriz   : " + txt_mat_A  + ", cantidad: " + str(cant_mat_A)  + ", tiempo: " + str(t_mat_A)  + " ns\n"
        msg += "  En arbol BST: " + txt_arb_A  + ", cantidad: " + str(cant_arb_A)  + ", tiempo: " + str(t_arb_A)  + " ns\n"
        msg += "  -> Mas rapido: " + rapido_A  + "\n\n"
        msg += "Matriz A3:\n"
        msg += "  En matriz   : " + txt_mat_A3 + ", cantidad: " + str(cant_mat_A3) + ", tiempo: " + str(t_mat_A3) + " ns\n"
        msg += "  En arbol BST: " + txt_arb_A3 + ", cantidad: " + str(cant_arb_A3) + ", tiempo: " + str(t_arb_A3) + " ns\n"
        msg += "  -> Mas rapido: " + rapido_A3 + "\n"

        self._add_text(self.txt_result, msg)
        self.status.config(text="Estado: busqueda completada.")


# ================================================================
# PUNTO DE ENTRADA
# ================================================================

if __name__ == "__main__":
    app = App()        # Crea la ventana principal
    app.mainloop()     # Inicia el bucle de eventos de tkinter
