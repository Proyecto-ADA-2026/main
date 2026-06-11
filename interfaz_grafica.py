# ==============================================================================
# INTERFAZ GRAFICA DEL PROYECTO
# ==============================================================================
# Este archivo contiene la ventana principal de Tkinter, la visualizacion del
# arbol, las validaciones de entrada y los eventos que llaman al backend.
# ==============================================================================


# ==============================================================================
# IMPORTACIONES Y CONFIGURACION INICIAL
# ==============================================================================

import tkinter as tk                 # Libreria para crear la ventana grafica en escritorio
from tkinter import ttk, messagebox  # ttk = widgets modernos; messagebox = dialogos de alerta
from gestor_txt import GestorArchivos, ConstructorTexto # Servicios para archivos y textos de resumen.

from proyecto_final import (         # Importa solo funciones algoritmicas usadas por la interfaz.
    MAX_N,                            # Limite logico de n definido por el backend.
    crear_matriz,                     # Genera matriz n*n con numeros aleatorios 0-9
    multiplicar_matrices,             # Multiplica matrices cuadradas para calcular A2 y A3
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
    medir_tiempo_promedio,            # Mide promedio de nanosegundos que tarda una funcion
    arbol_a_ascii,                    # Convierte el arbol a dibujo ASCII con ramas / y \
    contar_nodos_arbol_json,          # Cuenta todos los nodos del arbol recursivamente
    altura_arbol_json,                # Calcula la altura (niveles) del arbol
    recorrido_inorden_json,           # Recorre el arbol en inorden (menor a mayor)
    contar_elementos_representados_arbol, # Suma las frecuencias guardadas en el arbol
)

from medicion_memoria import (        # Utilidades separadas para estimacion y medicion de memoria.
    iniciar_medicion_memoria,
    obtener_memoria_actual_y_pico,
    detener_medicion_memoria,
    estimar_memoria_estructuras,
)


# ==============================================================================
# VISUALIZADOR GRAFICO DEL ARBOL
# ==============================================================================
# Responsabilidad: dibujar graficamente el arbol BST en un Canvas con scroll.
# ==============================================================================

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


# ==============================================================================
# CLASE PRINCIPAL DE LA INTERFAZ GRAFICA
# ==============================================================================
# Responsabilidad: construir la GUI y manejar los eventos del usuario.
# ==============================================================================

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

    # ==========================================================================
    # ESTILOS VISUALES DE TKINTER
    # ==========================================================================

    def _estilos(self):
        """Configura el tema visual de todos los widgets ttk."""
        s = ttk.Style()                         # Objeto que permite personalizar widgets ttk.
        s.theme_use("clam")                     # Tema base compatible con configuracion de colores.
        s.configure("Main.TFrame",   background="#f4f6f9") # Fondo principal.
        s.configure("Header.TFrame", background="#1f4e79") # Franja superior.
        s.configure("Header.TLabel",    background="#1f4e79", foreground="white",   font=("Segoe UI", 18, "bold"))
        s.configure("HeaderSub.TLabel", background="#1f4e79", foreground="#d9e8f5", font=("Segoe UI", 10))
        s.configure("Card.TLabelframe",       background="#ffffff", borderwidth=1, relief="solid")
        s.configure("Card.TLabelframe.Label", background="#f4f6f9", foreground="#1f4e79", font=("Segoe UI", 11, "bold"))
        s.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
        s.configure("TEntry", padding=6,             font=("Segoe UI", 10))
        s.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#1f4e79", foreground="white")
        s.map("Primary.TButton", background=[("active", "#173a5c")], foreground=[("active", "white")])
        s.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(12, 6))

    # ==========================================================================
    # CONSTRUCCION DE WIDGETS DE LA INTERFAZ
    # ==========================================================================

    def _construir_ui(self):
        """Crea y posiciona todos los widgets de la ventana principal."""

        principal = ttk.Frame(self, style="Main.TFrame") # Contenedor raiz de toda la interfaz.
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
        ttk.Button(top, text="Generar matriz A y A3", # Boton que inicia todo el procesamiento.
                   style="Primary.TButton",
                   command=self.generar).pack(side="left", padx=10)
        tk.Label(top, text="(Si n > 20 se muestra vista previa y se guarda en .txt)",
                 bg="#f4f6f9", fg="#666666", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # Botones secundarios
        bf = ttk.Frame(principal, style="Main.TFrame")
        bf.pack(fill="x", padx=20, pady=(0, 10))
        ttk.Button(bf, text="Abrir TXT A",       command=lambda: self._abrir("matriz_A.txt")).pack(side="left",  padx=5) # Abre salida de A.
        ttk.Button(bf, text="Abrir TXT A3",      command=lambda: self._abrir("matriz_A3.txt")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver JSON Arbol A",  command=lambda: self._abrir("arbol_A.json")).pack(side="left",  padx=5)
        ttk.Button(bf, text="Ver Arbol A",  command=lambda: self._mostrar_grafico_arbol("Visualizacion Arbol A",  self.arbol_A)).pack(side="left",  padx=5)
        ttk.Button(bf, text="Ver JSON Arbol A3", command=lambda: self._abrir("arbol_A3.json")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver Arbol A3", command=lambda: self._mostrar_grafico_arbol("Visualizacion Arbol A3", self.arbol_A3)).pack(side="left", padx=5)
        # Panel de busqueda
        pf = tk.LabelFrame(principal, text="Busqueda",
                            bg="#f4f6f9", fg="#333333", font=("Segoe UI", 9))
        pf.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(pf, text="Numero a buscar:", bg="#f4f6f9", fg="#222222",
                 font=("Segoe UI", 9)).pack(side="left", padx=(12, 5), pady=8)
        self.entry_buscado = tk.Entry(pf, width=10, font=("Segoe UI", 9),
                                       bg="white", fg="black", relief="solid", bd=1)
        self.entry_buscado.pack(side="left", padx=5)
        tk.Button(pf, text="Buscar en matriz y arbol", # Ejecuta la busqueda comparativa.
                  command=self.buscar,
                  font=("Segoe UI", 9), bg="#f5f5f5", fg="#111111",
                  activebackground="#e6e6e6", relief="raised",
                  bd=1, padx=8, pady=2, cursor="hand2").pack(side="left", padx=10)

        # Area central: matrices (izq) + resumen (der)
        centro = ttk.Frame(principal, style="Main.TFrame")
        centro.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        izq = ttk.LabelFrame(centro, text="Matrices generadas", style="Card.TLabelframe")
        izq.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.notebook = ttk.Notebook(izq)        # Pestañas para alternar entre A y A3.
        self.tab_A    = ttk.Frame(self.notebook)
        self.tab_A3   = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_A,  text="Matriz A")
        self.notebook.add(self.tab_A3, text="Matriz A3")
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)
        self.text_A  = self._text_scroll(self.tab_A)
        self.text_A3 = self._text_scroll(self.tab_A3)

        der = ttk.LabelFrame(centro, text="Resumen y analisis", style="Card.TLabelframe")
        der.pack(side="left", fill="both", expand=False)
        self.txt_result = tk.Text(der, width=50, height=24, wrap="word", # Panel de resumen textual.
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
        self.txt_arbol = tk.Text(af, height=10, wrap="none", # Panel para el arbol ASCII.
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

    # ==========================================================================
    # METODOS AUXILIARES DE WIDGETS
    # ==========================================================================

    def _text_scroll(self, parent):
        """Crea un widget Text con barras de scroll horizontal y vertical."""
        frame = ttk.Frame(parent)                # Contenedor del texto y sus barras.
        frame.pack(fill="both", expand=True)
        text = tk.Text(frame, wrap="none", font=("Consolas", 11), # Area de texto monoespaciada.
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
        ok = self.gestor.abrir_archivo(nombre_archivo) # Delegacion al gestor de archivos.
        if not ok:
            messagebox.showwarning("Archivo no encontrado",
                                   "Primero genera la matriz para crear el archivo.")

    def _mostrar_grafico_arbol(self, titulo, raiz_arbol):
        """Abre la ventana emergente con la visualizacion grafica del arbol."""
        if raiz_arbol is None:                   # Valida que el arbol ya haya sido construido.
            messagebox.showwarning("Sin datos", "Primero genera la matriz para construir el arbol.")
            return
        VisualizadorArbol(self, raiz_arbol, titulo)

    def _mat_to_str(self, M, lim=10):
        """Convierte la matriz M a texto para mostrar en pantalla.
        n > 20: vista previa lim x lim.
        n <= 20: muestra la matriz completa.
        Usa for, if y +=. Sin .join() ni str(lista).
        """
        n = len(M)                               # Dimension de la matriz.
        resultado = ""                           # Acumulador del texto a mostrar.

        if n > 20:                               # Para matrices grandes se muestra solo vista previa.
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

        for i in range(n):                       # Para matrices pequeñas se muestra completa.
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
        if nodo is None:                         # Caso base para ramas vacias.
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
        i = 0                                    # Avanza desde el inicio.
        while i < len(texto) and texto[i] == " ":
            i += 1
        j = len(texto) - 1                       # Retrocede desde el final.
        while j >= 0 and texto[j] == " ":
            j -= 1
        if i > j:
            return ""
        return texto[i:j + 1]

    def _es_entero(self, texto):
        """Verifica si un string es un numero entero valido sin int() previo.
        Recorre caracter a caracter comparando con '0' y '9'.
        """
        if len(texto) == 0:                      # Cadena vacia no es numero.
            return False
        inicio = 0
        if texto[0] == "-":                      # Permite signo negativo antes de validar digitos.
            inicio = 1
        if inicio == len(texto):
            return False
        i = inicio
        while i < len(texto):
            if texto[i] < "0" or texto[i] > "9":
                return False
            i += 1
        return True

    # ==========================================================================
    # ACCION PRINCIPAL: GENERAR MATRICES, ANALISIS Y ARBOLES
    # ==========================================================================

    def generar(self):
        """Genera A, calcula A3, analiza, construye arboles BST y muestra todo."""

        # Validar n
        texto_n = self._limpiar_texto(self.entry_n.get()) # Lee y limpia el valor escrito por el usuario.
        if not self._es_entero(texto_n):          # Valida que la entrada sea numerica.
            messagebox.showerror("Error", "Ingrese un valor entero para n.")
            return
        n = int(texto_n)                          # Convierte el texto validado a entero.

        if n < 4:                                 # Restriccion minima del enunciado.
            messagebox.showerror("Error", "n debe ser mayor o igual a 4.")
            return
        if n > MAX_N:                             # Limite para evitar consumo excesivo.
            messagebox.showerror("Error",
                "n supera el limite de " + str(MAX_N) +
                ". El calculo de A3 (O(n3)) consumiria demasiada RAM.")
            return
        if n > 20:                                # Advierte que se mostrara una vista previa.
            ok = messagebox.askyesno("Advertencia",
                "n es grande. Se mostrara vista previa y se guardaran archivos .txt. Continuar?")
            if not ok:
                return

        self.status.config(text="Estado: generando matriz y calculando A3...") # Actualiza barra de estado.
        self.update_idletasks()

        try:
            # Paso 1: crear A y calcular A3
            iniciar_medicion_memoria()            # Comienza medicion de memoria.
            self.A = crear_matriz(n)              # Genera la matriz A con el backend.

            A2 = None                             # Se conserva para el reporte detallado de memoria.
            if n > 100:                           # Ruta para matrices muy grandes.
                self.gestor.guardar_matriz("matriz_A.txt", self.A, "Matriz A")
                self.status.config(text="Estado: guardando A3 fila por fila...")
                self.update_idletasks()
                ruta_a3 = self.gestor.CARPETA + "\\" + "matriz_A3.txt"
                self.A3 = guardar_A3_directo_txt(self.A, ruta_a3) # Calcula y guarda A3.
            else:
                A2 = multiplicar_matrices(self.A, self.A) # Calcula A2 para medirla y construir A3.
                self.A3 = multiplicar_matrices(A2, self.A) # Calcula A3 en memoria.
                self.gestor.guardar_matriz("matriz_A.txt",  self.A,  "Matriz A")
                self.gestor.guardar_matriz("matriz_A3.txt", self.A3, "Matriz A3")

            # Paso 2: analizar
            analisis_A  = analizar_matriz(self.A)  # Clasifica los valores de A.
            analisis_A3 = analizar_matriz(self.A3) # Clasifica los valores de A3.

            # Paso 3: repeticiones
            rep_A  = contar_repeticiones(self.A)   # Frecuencias por valor en A.
            rep_A3 = contar_repeticiones(self.A3)  # Frecuencias por valor en A3.

            # Paso 4: construir BST
            lista_A  = frecuencias_a_json_ordenado(rep_A) # Convierte frecuencias a lista ordenada.
            self.arbol_A  = construir_arbol_json_equilibrado(lista_A,  0, len(lista_A)  - 1) # Arbol de A.
            lista_A3 = frecuencias_a_json_ordenado(rep_A3)
            self.arbol_A3 = construir_arbol_json_equilibrado(lista_A3, 0, len(lista_A3) - 1) # Arbol de A3.

            # Paso 5: vectores ordenados
            vec_A   = matriz_a_vector(self.A)      # Aplana A para ordenar.
            vec_A3  = matriz_a_vector(self.A3)     # Aplana A3 para ordenar.
            va_asc  = ordenar_ascendente(vec_A)    # Orden ascendente propio.
            va3_asc = ordenar_ascendente(vec_A3)
            va_desc = invertir_vector(va_asc)      # Orden descendente a partir del ascendente.
            va3_desc= invertir_vector(va3_asc)

            # Paso 6: mostrar matrices
            self._set_text(self.text_A,  self._mat_to_str(self.A))  # Muestra matriz A.
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
            mem_actual, mem_pico = obtener_memoria_actual_y_pico() # Lee memoria medida.
            detener_medicion_memoria()             # Detiene tracemalloc.
            estimacion = estimar_memoria_estructuras(
                A=self.A,
                A2=A2,
                A3=self.A3,
                vector={"A": vec_A, "A3": vec_A3},
                frecuencias={"A": rep_A, "A3": rep_A3},
                arbol={"A": self.arbol_A, "A3": self.arbol_A3}
            )
            validacion_A = {
                "elementos_matriz": n * n,         # Total de celdas de A.
                "elementos_arbol": contar_elementos_representados_arbol(self.arbol_A),
                "valores_unicos": len(lista_A),
                "nodos_arbol": contar_nodos_arbol_json(self.arbol_A),
                "altura": altura_arbol_json(self.arbol_A)
            }
            validacion_A3 = {
                "elementos_matriz": n * n,
                "elementos_arbol": contar_elementos_representados_arbol(self.arbol_A3),
                "valores_unicos": len(lista_A3),
                "nodos_arbol": contar_nodos_arbol_json(self.arbol_A3),
                "altura": altura_arbol_json(self.arbol_A3)
            }

            # Paso 9: resumen en el panel
            salida = self.constructor.construir_salida(
                analisis_A, analisis_A3, rep_A, rep_A3,
                va_asc, va_desc, va3_asc, va3_desc,
                mem_actual, mem_pico, estimacion,
                validacion_A, validacion_A3
            )
            self._set_text(self.txt_result, salida)

            # Paso 10: guardar JSON del arbol manualmente
            self.gestor.guardar_arbol_json("arbol_A.json",  self._arbol_a_dict(self.arbol_A),  "ArbolA") # JSON de A.
            self.gestor.guardar_arbol_json("arbol_A3.json", self._arbol_a_dict(self.arbol_A3), "ArbolA3")

            if n > 20:
                self.status.config(text="Estado: generado. Vista previa en pantalla. Archivos en /resultados.")
            else:
                self.status.config(text="Estado: generado correctamente. Ya puedes buscar un numero.")

        except Exception as e:                     # Captura errores para mostrarlos sin cerrar la app.
            messagebox.showerror("Error", "Ocurrio un problema al generar:\n" + str(e))
            self.status.config(text="Estado: error al generar.")

    # ==========================================================================
    # ACCION SECUNDARIA: BUSQUEDA COMPARATIVA
    # ==========================================================================

    def buscar(self):
        """Busca un numero en la matriz y en el arbol BST, mide tiempos y compara."""
        if self.A is None or self.A3 is None or self.arbol_A is None or self.arbol_A3 is None: # Requiere datos previos.
            messagebox.showwarning("Aviso", "Primero genera la matriz A y A3.")
            return

        texto_b = self._limpiar_texto(self.entry_buscado.get()) # Lee el numero a buscar.
        if not self._es_entero(texto_b):         # Valida entrada numerica.
            messagebox.showerror("Error", "Ingrese un numero entero para buscar.")
            return
        buscado = int(texto_b)                   # Numero entero que se buscara.

        self.status.config(text="Estado: buscando...")
        self.update_idletasks()

        repeticiones = 1000                      # Cantidad de ejecuciones para promediar tiempos.

        # Busquedas en A
        res_mat_A,  t_mat_A  = medir_tiempo_promedio(buscar_y_contar_en_matriz, self.A,        buscado, repeticiones) # Matriz A.
        enc_mat_A, cant_mat_A = res_mat_A
        res_arb_A,  t_arb_A  = medir_tiempo_promedio(buscar_en_arbol_json,      self.arbol_A,  buscado, repeticiones) # Arbol A.

        # Busquedas en A3
        res_mat_A3, t_mat_A3  = medir_tiempo_promedio(buscar_y_contar_en_matriz, self.A3,       buscado, repeticiones)
        enc_mat_A3, cant_mat_A3 = res_mat_A3
        res_arb_A3, t_arb_A3  = medir_tiempo_promedio(buscar_en_arbol_json,     self.arbol_A3,  buscado, repeticiones)

        if res_arb_A is not None:                # Si el arbol encontro el valor, lee su frecuencia.
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
        msg = "\n\nBUSQUEDA: " + str(buscado) + "\n" # Bloque que se agrega al resumen.
        msg += "-------------------\n"
        msg += "Repeticiones usadas para promedio: " + str(repeticiones) + "\n\n"
        msg += "Matriz A:\n"
        msg += "  En matriz   : " + txt_mat_A  + ", cantidad: " + str(cant_mat_A)  + ", tiempo promedio: " + str(t_mat_A)  + " ns\n"
        msg += "  En arbol BST: " + txt_arb_A  + ", cantidad: " + str(cant_arb_A)  + ", tiempo promedio: " + str(t_arb_A)  + " ns\n"
        msg += "  -> Mas rapido: " + rapido_A  + "\n\n"
        msg += "Matriz A3:\n"
        msg += "  En matriz   : " + txt_mat_A3 + ", cantidad: " + str(cant_mat_A3) + ", tiempo promedio: " + str(t_mat_A3) + " ns\n"
        msg += "  En arbol BST: " + txt_arb_A3 + ", cantidad: " + str(cant_arb_A3) + ", tiempo promedio: " + str(t_arb_A3) + " ns\n"
        msg += "  -> Mas rapido: " + rapido_A3 + "\n\n"
        msg += "ANALISIS AUTOMATICO\n"
        msg += "-------------------\n"
        msg += "La busqueda secuencial en matriz tiene costo O(n2), porque puede recorrer todas las posiciones. "
        msg += "La busqueda en el arbol equilibrado depende de la altura del arbol y, al estar construido con valores unicos y frecuencias, "
        msg += "tiene costo aproximado O(log u), donde u es la cantidad de valores unicos. "
        msg += "Para matrices pequenas, los tiempos pueden variar por la sobrecarga del sistema, por eso se usa un promedio de varias ejecuciones.\n"

        self._add_text(self.txt_result, msg)
        self.status.config(text="Estado: busqueda completada.")


# ================================================================
# PUNTO DE ENTRADA
# ================================================================

if __name__ == "__main__":
    app = App()        # Crea la ventana principal
    app.mainloop()     # Inicia el bucle de eventos de tkinter
