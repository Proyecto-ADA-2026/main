# ==============================================================================
# INTERFAZ GRAFICA DEL PROYECTO
# ==============================================================================
# Este archivo construye toda la ventana con Tkinter.
# Tkinter es la libreria grafica incluida en Python; no requiere instalacion.
#
# ESTRUCTURA DE LA VENTANA:
#   Header azul     -> titulo y subtitulo del proyecto
#   Fila superior   -> campo "n" + boton "Generar"
#   Botones         -> abrir TXT / JSON / ver arbol grafico
#   Panel busqueda  -> campo numerico + boton buscar
#   Centro izq      -> pestanas con la vista de Matriz A y A3 (widget Text + Notebook)
#   Centro der      -> panel de resumen y analisis (widget Text)
#   Panel inferior  -> arbol ASCII (widget Text con scroll horizontal)
#   Barra de estado -> texto de estado en la parte inferior
#
# SEPARACION DE RESPONSABILIDADES:
#   - La interfaz solo llama funciones del backend (proyecto_final.py).
#   - GestorArchivos y ConstructorTexto (gestor_txt.py) manejan archivos y texto.
#   - medicion_memoria.py mide y estima la memoria.
# ==============================================================================


# ==============================================================================
# IMPORTACIONES
# ==============================================================================

import tkinter as tk                 # Modulo principal de Tkinter para crear ventanas.
from tkinter import ttk, messagebox  # ttk: widgets con estilos modernos. messagebox: dialogos emergentes.
from gestor_txt import GestorArchivos, ConstructorTexto  # Clases de apoyo para archivos y texto.

MAX_N = 50  # Limite maximo de n que acepta la interfaz.
            # A3 se calcula con dos multiplicaciones de matrices: costo O(n^3).
            # Para n=50: 50^3 = 125000 operaciones, aceptable.
            # Para n=100: 100^3 = 1000000, puede tardar varios segundos y usar mucha RAM.

from proyecto_final import (         # Importa exactamente las funciones que usa la interfaz.
    crear_matriz,                    # Genera la matriz A con valores aleatorios 0-9.
    multiplicar_matrices,            # Multiplica matrices para calcular A2 y A3.
    guardar_A3_directo_txt,          # Alternativa de bajo consumo de RAM para n > 100.
    analizar_matriz,                 # Clasifica cada elemento en par/impar/primo/perfecto/cuadrado.
    contar_repeticiones,             # Cuenta cuantas veces aparece cada valor (tabla de frecuencias).
    frecuencias_a_json_ordenado,     # Convierte la tabla de frecuencias a lista ordenada de dicts.
    matriz_a_vector,                 # Aplana la matriz n*n en un vector de n^2 elementos.
    ordenar_ascendente,              # Ordenamiento propio: insertion sort (<=64) o merge sort (>64).
    invertir_vector,                 # Invierte el vector para obtener orden descendente.
    construir_arbol_json_equilibrado, # Construye BST equilibrado desde lista ordenada.
    buscar_y_contar_en_matriz,       # Busqueda lineal O(n^2) con conteo de apariciones.
    buscar_en_arbol_json,            # Busqueda binaria O(log n) en el BST.
    medir_tiempo_promedio,           # Ejecuta la busqueda N veces y retorna el promedio en ns.
    arbol_a_ascii,                   # Genera el dibujo ASCII del arbol con ramas / y \.
    contar_nodos_arbol_json,         # Cuenta nodos del arbol para validacion.
    altura_arbol_json,               # Calcula la altura del arbol para validacion.
    recorrido_inorden_json,          # Recorrido inorden (produce valores en orden ascendente).
    contar_elementos_representados_arbol, # Suma las frecuencias del arbol para validacion.
)

from medicion_memoria import (       # Funciones de medicion de memoria (tracemalloc + estimacion).
    iniciar_medicion_memoria,        # Llama tracemalloc.start() para comenzar a rastrear.
    obtener_memoria_actual_y_pico,   # Llama tracemalloc.get_traced_memory() -> (actual, pico).
    detener_medicion_memoria,        # Llama tracemalloc.stop() para dejar de rastrear.
    estimar_memoria_estructuras,     # Recorre objetos recursivamente con sys.getsizeof().
)


# ==============================================================================
# CLASE: VISUALIZADOR GRAFICO DEL ARBOL (VENTANA EMERGENTE)
# ==============================================================================

class VisualizadorArbol(tk.Toplevel):
    """Ventana emergente que dibuja el BST graficamente con circulos y lineas.

    Hereda de tk.Toplevel (no de tk.Tk) porque es una ventana secundaria
    que depende de la ventana principal (App). Si se cerrara App, esta
    tambien se cierra gracias a transient().

    Los nodos se dibujan en un Canvas de Tkinter con:
      - Circulos azules oscuros (ovales) para cada nodo.
      - Texto blanco con el valor y la frecuencia dentro del circulo.
      - Lineas grises que conectan padre con hijos.
      - Efecto hover (mouse encima): el nodo cambia a verde y la barra muestra info.
    """

    def __init__(self, padre, raiz, titulo):
        super().__init__(padre)          # Llama al constructor de tk.Toplevel con la ventana padre.
        self.title(titulo)               # Titulo de la ventana emergente.
        self.geometry("1100x750")        # Tamaño inicial: ancho x alto en pixeles.
        self.configure(bg="#121214")     # Fondo oscuro (casi negro).
        self.minsize(800, 600)           # Impide que la ventana sea mas pequena que esto.

        self.transient(padre)            # Hace que esta ventana sea "hija" de padre (siempre encima).

        self.raiz = raiz                 # Referencia a la raiz del BST que se va a dibujar.
        self.nodos_ovales = {}           # Dict {id(nodo): id_oval_canvas} para cambiar colores en hover.
        self.nodos_datos = {}            # Dict {id(nodo): dato} para mostrar info en la barra al hacer hover.

        # Contenedor principal con scrollbars (el arbol puede ser mas ancho/alto que la ventana).
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        sb_y = ttk.Scrollbar(frame, orient="vertical")   # Barra de scroll vertical.
        sb_x = ttk.Scrollbar(frame, orient="horizontal") # Barra de scroll horizontal.

        self.canvas = tk.Canvas(         # Canvas: superficie de dibujo de Tkinter.
            frame,
            bg="#121214",
            xscrollcommand=sb_x.set,     # Vincula el scroll horizontal al canvas.
            yscrollcommand=sb_y.set,     # Vincula el scroll vertical al canvas.
            highlightthickness=0         # Sin borde visible alrededor del canvas.
        )

        sb_y.config(command=self.canvas.yview) # El scrollbar llama canvas.yview para desplazar.
        sb_x.config(command=self.canvas.xview)

        sb_y.pack(side="right", fill="y")   # Scrollbar vertical a la derecha, ocupa toda la altura.
        sb_x.pack(side="bottom", fill="x")  # Scrollbar horizontal abajo, ocupa todo el ancho.
        self.canvas.pack(side="left", fill="both", expand=True) # Canvas ocupa el espacio restante.

        # Barra de informacion en la parte inferior de la ventana.
        self.lbl_info = tk.Label(
            self,
            text="Pasa el mouse sobre un nodo para ver mas informacion. Usa las barras para desplazarte.",
            bg="#1c1c1f",
            fg="#a1a1aa",
            font=("Segoe UI", 10, "bold"),
            pady=8
        )
        self.lbl_info.pack(fill="x")  # Ocupa todo el ancho de la ventana.

        self.graficar()  # Calcula posiciones y dibuja el arbol en el canvas.

    def _calcular_altura(self, nodo):
        """Calcula la altura del arbol de forma recursiva sin usar max().

        Se necesita la altura para calcular el alto total del canvas (scrollregion).
        """
        if nodo is None:
            return 0
        h_izq = self._calcular_altura(nodo.izquierda) # Desciende por la rama izquierda.
        h_der = self._calcular_altura(nodo.derecha)   # Desciende por la rama derecha.
        if h_izq > h_der:                             # Toma la mayor de las dos alturas.
            return h_izq + 1
        return h_der + 1                              # +1 cuenta el nodo actual.

    def _calcular_posiciones(self, nodo, depth, coordenadas, contador):
        """Calcula la posicion (x, y) de cada nodo usando recorrido INORDEN.

        ESTRATEGIA: El recorrido inorden visita los nodos de izquierda a derecha
        en el arbol. Al asignar x = 60 + contador * 90, cada nodo queda
        separado 90 pixeles del anterior en el eje X, sin solapamientos.
        La profundidad 'depth' determina la posicion Y (cada nivel 90 pixeles mas abajo).

        PARAMETROS:
          nodo: nodo actual del recorrido.
          depth: nivel del nodo (raiz = 0, hijos = 1, nietos = 2, ...).
          coordenadas: dict {id(nodo): (x, y)} que se va llenando.
          contador: posicion horizontal actual (se incrementa con cada nodo visitado).
        """
        if nodo is None:
            return contador                   # Caso base: nodo vacio, retorna el contador sin cambios.
        # 1. Visita el subarbol izquierdo primero (inorden: izq -> raiz -> der).
        contador = self._calcular_posiciones(nodo.izquierda, depth + 1, coordenadas, contador)

        # 2. Asigna la posicion al nodo actual.
        x = 60 + contador * 90               # Posicion horizontal: 60px de margen + 90px por nodo previo.
        y = 60 + depth * 90                  # Posicion vertical: 60px de margen + 90px por nivel.
        coordenadas[id(nodo)] = (x, y)       # Guarda las coordenadas con el id del nodo como clave.
        self.nodos_datos[id(nodo)] = nodo.dato # Guarda el dato del nodo para usarlo en hover.
        contador += 1                        # Incrementa para el siguiente nodo del inorden.

        # 3. Visita el subarbol derecho.
        contador = self._calcular_posiciones(nodo.derecha, depth + 1, coordenadas, contador)
        return contador

    def _dibujar(self, nodo, coordenadas):
        """Dibuja recursivamente lineas y nodos (circulos + texto) en el canvas.

        ORDEN DE DIBUJO IMPORTANTE:
          1. Primero se dibujan las LINEAS de conexion (hijos).
          2. Despues se dibuja el CIRCULO del nodo padre.
        Esto asegura que el circulo quede encima de las lineas y no se vea cortado.
        """
        if nodo is None:
            return
        x, y = coordenadas[id(nodo)]         # Posicion del nodo actual.

        # 1. Dibuja lineas hacia los hijos (si existen) ANTES de dibujar el circulo del nodo.
        if nodo.izquierda is not None:
            x_izq, y_izq = coordenadas[id(nodo.izquierda)]
            self.canvas.create_line(x, y, x_izq, y_izq, fill="#3f3f46", width=2) # Linea gris oscura.
            self._dibujar(nodo.izquierda, coordenadas) # Dibuja recursivamente el subarbol izquierdo.

        if nodo.derecha is not None:
            x_der, y_der = coordenadas[id(nodo.derecha)]
            self.canvas.create_line(x, y, x_der, y_der, fill="#3f3f46", width=2)
            self._dibujar(nodo.derecha, coordenadas)   # Dibuja recursivamente el subarbol derecho.

        # 2. Dibuja el circulo del nodo (ENCIMA de las lineas).
        r = 24                               # Radio del circulo en pixeles.
        oval_id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,     # Bounding box del circulo: (x1,y1,x2,y2).
            fill="#1e3a8a",                  # Azul oscuro (relleno del circulo).
            outline="#3b82f6",               # Azul claro (borde del circulo).
            width=2.5                        # Grosor del borde.
        )
        self.nodos_ovales[id(nodo)] = oval_id # Guarda el id del oval para poder cambiar su color en hover.

        # 3. Dibuja el texto del valor y la frecuencia DENTRO del circulo.
        valor = nodo.dato["valor"]
        cant = nodo.dato["cantidad"]
        texto = str(valor) + "\n(" + str(cant) + ")" # Dos lineas: valor arriba, frecuencia abajo entre parentesis.
        text_id = self.canvas.create_text(
            x, y,                            # Centrado en el mismo punto que el circulo.
            text=texto,
            fill="#f8fafc",                  # Texto blanco.
            font=("Segoe UI", 9, "bold"),
            justify="center"
        )

        # 4. Vincula los eventos de mouse a AMBOS elementos (oval y texto) para que el hover funcione.
        self.canvas.tag_bind(oval_id,  "<Enter>", lambda e, nid=id(nodo): self.al_entrar(nid))
        self.canvas.tag_bind(oval_id,  "<Leave>", lambda e, nid=id(nodo): self.al_salir(nid))
        self.canvas.tag_bind(text_id,  "<Enter>", lambda e, nid=id(nodo): self.al_entrar(nid))
        self.canvas.tag_bind(text_id,  "<Leave>", lambda e, nid=id(nodo): self.al_salir(nid))

    def al_entrar(self, nid):
        """Evento: el mouse entro al circulo del nodo. Cambia a verde y muestra info."""
        oval_id = self.nodos_ovales[nid]
        self.canvas.itemconfig(oval_id, fill="#047857", outline="#34d399") # Verde esmeralda.

        dato = self.nodos_datos[nid]
        val = dato["valor"]
        cant = dato["cantidad"]
        self.lbl_info.config(
            text="Nodo enfocado -> Valor: " + str(val) + " | Repeticiones en la matriz: " + str(cant),
            fg="#34d399"  # Texto verde que coincide con el color del nodo.
        )

    def al_salir(self, nid):
        """Evento: el mouse salio del circulo del nodo. Restaura el color azul original."""
        oval_id = self.nodos_ovales[nid]
        self.canvas.itemconfig(oval_id, fill="#1e3a8a", outline="#3b82f6") # Vuelve al azul oscuro.

        self.lbl_info.config(
            text="Pasa el mouse sobre un nodo para ver mas informacion. Usa las barras para desplazarte.",
            fg="#a1a1aa"  # Texto gris neutral.
        )

    def graficar(self):
        """Orquesta el calculo de posiciones, el dibujo y la configuracion del scrollregion.

        scrollregion define el area total del canvas (incluyendo la parte que esta fuera
        de la ventana visible y a la que se accede con las barras de scroll).
        """
        if self.raiz is None:
            self.canvas.create_text(
                200, 100,
                text="El arbol esta vacio. Primero genera la matriz.",
                fill="#f8fafc",
                font=("Segoe UI", 12)
            )
            return

        coordenadas = {}  # Dict que se llenara con {id(nodo): (x, y)}.

        def contar(n):
            """Cuenta el total de nodos para calcular el ancho necesario del canvas."""
            if n is None:
                return 0
            return 1 + contar(n.izquierda) + contar(n.derecha)

        total_nodos = contar(self.raiz)          # Total de nodos del arbol.
        altura = self._calcular_altura(self.raiz) # Altura del arbol para calcular el alto del canvas.

        self._calcular_posiciones(self.raiz, 0, coordenadas, 0) # Llena el dict de coordenadas.
        self._dibujar(self.raiz, coordenadas)    # Dibuja todo en el canvas.

        # Configura el area desplazable del canvas segun el tamaño real del dibujo.
        ancho = 120 + total_nodos * 90           # Cada nodo ocupa 90px de ancho + margen.
        alto = 120 + altura * 90                 # Cada nivel ocupa 90px de alto + margen.
        self.canvas.config(scrollregion=(0, 0, ancho, alto)) # (x1, y1, x2, y2) del area total.


# ==============================================================================
# CLASE PRINCIPAL: VENTANA DE LA APLICACION
# ==============================================================================

class App(tk.Tk):
    """Ventana principal de la aplicacion.

    Hereda de tk.Tk (no de tk.Frame ni tk.Toplevel) porque ES la ventana raiz.
    Solo debe existir UNA instancia de tk.Tk en un programa Tkinter.
    Todas las demas ventanas deben ser tk.Toplevel (como VisualizadorArbol).
    """

    def __init__(self):
        """Constructor: inicializa la ventana, los objetos auxiliares y construye la UI."""
        super().__init__()  # Inicializa la ventana raiz de Tkinter (llama a tk.Tk.__init__).

        self.title("Analisis de Matriz A, A3 y Arbol Binario") # Texto de la barra de titulo.
        self.geometry("1280x820")   # Tamaño inicial de la ventana en pixeles.
        self.minsize(1080, 720)     # Tamaño minimo: impide que el usuario la encoja demasiado.
        self.configure(bg="#f4f6f9") # Color de fondo gris muy claro.

        # --- VARIABLES DE ESTADO ---
        # Se inicializan en None y se asignan cuando el usuario hace clic en "Generar".
        self.A        = None  # Matriz A generada (lista de listas n*n).
        self.A3       = None  # Matriz A^3 calculada (lista de listas n*n, valores mayores).
        self.arbol_A  = None  # Raiz del BST construido a partir de frecuencias de A (NodoJSON).
        self.arbol_A3 = None  # Raiz del BST construido a partir de frecuencias de A3 (NodoJSON).

        # --- OBJETOS AUXILIARES ---
        # Se crean una sola vez y se reutilizan en cada llamada a generar() y buscar().
        self.gestor      = GestorArchivos()   # Maneja la carpeta resultados y los archivos.
        self.constructor = ConstructorTexto() # Construye el texto del panel de resumen.

        self._estilos()      # Configura los colores y fuentes de los widgets ttk.
        self._construir_ui() # Crea y posiciona todos los widgets de la ventana.

    # ==========================================================================
    # ESTILOS VISUALES (ttk.Style)
    # ==========================================================================

    def _estilos(self):
        """Configura el tema visual de todos los widgets ttk con colores corporativos.

        ttk.Style permite personalizar la apariencia de widgets ttk como botones,
        frames y labels. El tema "clam" es compatible con configuracion de colores
        en Windows, Mac y Linux (los temas "default" y "vista" no respetan configure()).
        """
        s = ttk.Style()               # Objeto de estilos: existe uno por aplicacion.
        s.theme_use("clam")           # Establece el tema base que permite personalizar colores.

        # Estilos de frames (contenedores).
        s.configure("Main.TFrame",   background="#f4f6f9") # Fondo principal gris muy claro.
        s.configure("Header.TFrame", background="#1f4e79") # Franja superior azul oscuro.

        # Estilos de etiquetas en el header.
        s.configure("Header.TLabel",    background="#1f4e79", foreground="white",   font=("Segoe UI", 18, "bold"))
        s.configure("HeaderSub.TLabel", background="#1f4e79", foreground="#d9e8f5", font=("Segoe UI", 10))

        # Estilo de los paneles con borde (LabelFrame).
        s.configure("Card.TLabelframe",       background="#ffffff", borderwidth=1, relief="solid")
        s.configure("Card.TLabelframe.Label", background="#f4f6f9", foreground="#1f4e79", font=("Segoe UI", 11, "bold"))

        # Estilos de labels y entries genericos.
        s.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
        s.configure("TEntry", padding=6, font=("Segoe UI", 10))

        # Estilo del boton principal (azul oscuro).
        s.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=8,
                    background="#1f4e79", foreground="white")
        s.map("Primary.TButton",
              background=[("active", "#173a5c")],  # Color cuando el mouse esta encima.
              foreground=[("active", "white")])

        # Estilo de las pestanas del Notebook.
        s.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(12, 6))

    # ==========================================================================
    # CONSTRUCCION DE WIDGETS
    # ==========================================================================

    def _construir_ui(self):
        """Crea y posiciona todos los widgets de la ventana principal.

        JERARQUIA DE WIDGETS (de arriba a abajo):
          principal (Frame raiz)
            header (Frame azul)    -> titulo + subtitulo
            top (Frame)            -> campo n + boton Generar
            bf (Frame)             -> botones secundarios (Abrir, Ver)
            pf (LabelFrame)        -> panel de busqueda
            centro (Frame)
              izq (LabelFrame)     -> Notebook con pestanas A y A3
              der (LabelFrame)     -> panel de resumen
            af (LabelFrame)        -> arbol ASCII
            status (Label)         -> barra de estado
        """

        # Contenedor raiz que ocupa toda la ventana.
        principal = ttk.Frame(self, style="Main.TFrame")
        principal.pack(fill="both", expand=True) # fill=both: ocupa ancho y alto. expand=True: crece con la ventana.

        # ---- HEADER (banda azul oscuro en la parte superior) ----
        header = ttk.Frame(principal, style="Header.TFrame")
        header.pack(fill="x")  # Solo ocupa el ancho, no crece verticalmente.
        ttk.Label(header, text="Matriz A, A3 y Arbol Binario",
                  style="Header.TLabel").pack(anchor="w", padx=20, pady=(14, 2))  # Alineado a la izquierda.
        ttk.Label(header, text="Generacion, analisis, ordenamiento y busqueda comparativa",
                  style="HeaderSub.TLabel").pack(anchor="w", padx=20, pady=(0, 14))

        # ---- FILA SUPERIOR: campo n + boton Generar ----
        top = ttk.Frame(principal, style="Main.TFrame")
        top.pack(fill="x", padx=20, pady=(14, 6))
        ttk.Label(top, text="Tamano n (n >= 4):").pack(side="left") # Etiqueta a la izquierda.
        self.entry_n = ttk.Entry(top, width=10)                      # Campo de texto para ingresar n.
        self.entry_n.pack(side="left", padx=8)
        self.entry_n.insert(0, "4")                                  # Valor inicial del campo.
        ttk.Button(top, text="Generar matriz A y A3",
                   style="Primary.TButton",
                   command=self.generar).pack(side="left", padx=10)  # Llama a self.generar() al hacer clic.
        tk.Label(top, text="(Si n > 20 se muestra vista previa y se guarda en .txt)",
                 bg="#f4f6f9", fg="#666666", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # ---- BOTONES SECUNDARIOS (abrir archivos y ver arboles) ----
        bf = ttk.Frame(principal, style="Main.TFrame")
        bf.pack(fill="x", padx=20, pady=(0, 10))
        ttk.Button(bf, text="Abrir TXT A",
                   command=lambda: self._abrir("matriz_A.txt")).pack(side="left", padx=5)
        ttk.Button(bf, text="Abrir TXT A3",
                   command=lambda: self._abrir("matriz_A3.txt")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver JSON Arbol A",
                   command=lambda: self._abrir("arbol_A.json")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver Arbol A",
                   command=lambda: self._mostrar_grafico_arbol("Visualizacion Arbol A", self.arbol_A)).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver JSON Arbol A3",
                   command=lambda: self._abrir("arbol_A3.json")).pack(side="left", padx=5)
        ttk.Button(bf, text="Ver Arbol A3",
                   command=lambda: self._mostrar_grafico_arbol("Visualizacion Arbol A3", self.arbol_A3)).pack(side="left", padx=5)

        # ---- PANEL DE BUSQUEDA ----
        pf = tk.LabelFrame(principal, text="Busqueda",
                            bg="#f4f6f9", fg="#333333", font=("Segoe UI", 9))
        pf.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(pf, text="Numero a buscar:", bg="#f4f6f9", fg="#222222",
                 font=("Segoe UI", 9)).pack(side="left", padx=(12, 5), pady=8)
        self.entry_buscado = tk.Entry(pf, width=10, font=("Segoe UI", 9),
                                       bg="white", fg="black", relief="solid", bd=1)
        self.entry_buscado.pack(side="left", padx=5)
        tk.Button(pf, text="Buscar en matriz y arbol",
                  command=self.buscar,                   # Llama a self.buscar() al hacer clic.
                  font=("Segoe UI", 9), bg="#f5f5f5", fg="#111111",
                  activebackground="#e6e6e6", relief="raised",
                  bd=1, padx=8, pady=2, cursor="hand2").pack(side="left", padx=10)

        # ---- AREA CENTRAL: matrices a la izquierda, resumen a la derecha ----
        centro = ttk.Frame(principal, style="Main.TFrame")
        centro.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Panel izquierdo: Notebook con dos pestanas (Matriz A y Matriz A3).
        izq = ttk.LabelFrame(centro, text="Matrices generadas", style="Card.TLabelframe")
        izq.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.notebook = ttk.Notebook(izq)  # Notebook: contenedor con pestanas.
        self.tab_A    = ttk.Frame(self.notebook)  # Frame para la pestana "Matriz A".
        self.tab_A3   = ttk.Frame(self.notebook)  # Frame para la pestana "Matriz A3".
        self.notebook.add(self.tab_A,  text="Matriz A")  # Agrega la pestana al notebook.
        self.notebook.add(self.tab_A3, text="Matriz A3")
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)
        self.text_A  = self._text_scroll(self.tab_A)  # Crea el widget Text con scroll en la pestana A.
        self.text_A3 = self._text_scroll(self.tab_A3)

        # Panel derecho: resumen y analisis.
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
        self.txt_result.config(state="disabled") # Deshabilita la edicion manual por el usuario.

        # ---- PANEL DEL ARBOL ASCII (con scroll horizontal) ----
        af = ttk.LabelFrame(principal, text="Arbol binario de busqueda (A y A3)",
                             style="Card.TLabelframe")
        af.pack(fill="both", expand=False, padx=20, pady=(0, 10))
        self.txt_arbol = tk.Text(af, height=10, wrap="none",  # wrap="none": sin ajuste de linea, necesario para el ASCII.
                                  font=("Consolas", 12), bg="#fbfbfb", fg="#1e1e1e",
                                  relief="flat", padx=10, pady=10)
        sb_ay = ttk.Scrollbar(af, orient="vertical",   command=self.txt_arbol.yview)
        sb_ax = ttk.Scrollbar(af, orient="horizontal", command=self.txt_arbol.xview)
        self.txt_arbol.configure(yscrollcommand=sb_ay.set, xscrollcommand=sb_ax.set)
        # Se usa .grid() (en lugar de .pack()) para posicionar el texto y las dos barras.
        self.txt_arbol.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=(8, 0))
        sb_ay.grid(row=0, column=1, sticky="ns",  padx=(0, 8), pady=(8, 0))
        sb_ax.grid(row=1, column=0, sticky="ew",  padx=(8, 0), pady=(0, 8))
        af.rowconfigure(0, weight=1)     # La fila 0 (el texto) crece verticalmente.
        af.columnconfigure(0, weight=1)  # La columna 0 (el texto) crece horizontalmente.
        self.txt_arbol.insert("1.0", "Aqui se mostrara el arbol binario.\n(primero A, luego A3).")
        self.txt_arbol.config(state="disabled")

        # ---- BARRA DE ESTADO (fila inferior) ----
        self.status = tk.Label(principal, text="Estado: esperando datos...",
                               anchor="w",        # Texto alineado a la izquierda.
                               bg="#e8eef3",       # Fondo azul muy claro.
                               fg="#333333",
                               font=("Segoe UI", 10, "bold"))
        self.status.pack(fill="x", padx=20, pady=(0, 12), ipady=6) # ipady: padding interno vertical.

    # ==========================================================================
    # METODOS AUXILIARES DE WIDGETS
    # ==========================================================================

    def _text_scroll(self, parent):
        """Crea un widget Text con barras de scroll vertical y horizontal.

        Se usa grid() en lugar de pack() para posicionar el texto y las barras
        porque grid permite alinear el scroll vertical a la derecha del texto
        y el scroll horizontal abajo, sin que se superpongan.

        sticky="nsew": el widget se estira en las cuatro direcciones (norte, sur, este, oeste).
        """
        frame = ttk.Frame(parent)          # Contenedor del texto y sus barras.
        frame.pack(fill="both", expand=True)
        text = tk.Text(frame, wrap="none", font=("Consolas", 11),
                       bg="#fbfbfb", fg="#1f1f1f", relief="flat", padx=10, pady=10)
        sby = ttk.Scrollbar(frame, orient="vertical",   command=text.yview)   # Scroll vertical.
        sbx = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)   # Scroll horizontal.
        text.configure(yscrollcommand=sby.set, xscrollcommand=sbx.set)
        text.grid(row=0, column=0, sticky="nsew")  # El texto ocupa la celda (0,0).
        sby.grid(row=0, column=1, sticky="ns")     # El scroll vertical ocupa la celda (0,1).
        sbx.grid(row=1, column=0, sticky="ew")     # El scroll horizontal ocupa la celda (1,0).
        frame.rowconfigure(0, weight=1)            # La fila 0 se estira verticalmente.
        frame.columnconfigure(0, weight=1)         # La columna 0 se estira horizontalmente.
        text.config(state="disabled")              # El usuario no puede escribir en el widget.
        return text

    def _set_text(self, widget, contenido):
        """Reemplaza TODO el contenido de un widget Text con texto nuevo.

        Los widgets Text de Tkinter estan en modo "disabled" por defecto para
        que el usuario no los edite. Para escribir desde codigo se debe
        cambiar a "normal", escribir, y volver a "disabled".
        """
        widget.config(state="normal")        # Habilita el widget para escritura.
        widget.delete("1.0", "end")          # Borra todo desde la posicion 1.0 (fila 1, col 0) hasta el final.
        widget.insert("1.0", contenido)      # Inserta el nuevo contenido desde el principio.
        widget.config(state="disabled")      # Vuelve a deshabilitar la edicion.

    def _add_text(self, widget, contenido):
        """Agrega texto al final de un widget Text SIN borrar el contenido existente.

        Se usa para agregar los resultados de busqueda al panel de resumen
        sin borrar el resumen general que ya estaba ahi.
        see("end") hace scroll automatico hasta el final para que se vea el nuevo texto.
        """
        widget.config(state="normal")
        widget.insert("end", contenido)      # "end" es la posicion despues del ultimo caracter.
        widget.see("end")                    # Desplaza el scroll para mostrar el texto recien agregado.
        widget.config(state="disabled")

    def _abrir(self, nombre_archivo):
        """Abre un archivo de la carpeta resultados con la aplicacion predeterminada del SO."""
        ok = self.gestor.abrir_archivo(nombre_archivo) # Delega la apertura al gestor.
        if not ok:
            messagebox.showwarning("Archivo no encontrado",
                                   "Primero genera la matriz para crear el archivo.")

    def _mostrar_grafico_arbol(self, titulo, raiz_arbol):
        """Abre la ventana emergente VisualizadorArbol si el arbol ya fue construido."""
        if raiz_arbol is None:               # El arbol se crea al hacer clic en Generar.
            messagebox.showwarning("Sin datos", "Primero genera la matriz para construir el arbol.")
            return
        VisualizadorArbol(self, raiz_arbol, titulo) # Crea y muestra la ventana emergente.

    def _mat_to_str(self, M, lim=10):
        """Convierte la matriz M a texto para mostrar en el widget Text.

        - n <= 20: muestra la matriz COMPLETA con formato de columnas alineadas.
        - n > 20: muestra solo una vista previa de lim x lim con aviso del tamaño real.
          Esto evita cargar un widget Text con cientos de miles de caracteres.

        Formato por celda: ancho 6 caracteres (f"{valor:6}"), separados por "   ".
        """
        n = len(M)                           # Dimension de la matriz cuadrada.
        resultado = ""                       # Acumulador del texto a mostrar.

        if n > 20:                           # Vista previa para matrices grandes.
            l = lim if lim < n else n        # El limite no puede superar n.
            for i in range(l):
                for j in range(l):
                    resultado += f"{M[i][j]:6}"   # Ancho fijo de 6 para alinear columnas.
                    if j < l - 1:
                        resultado += "   "
                if i < l - 1:
                    resultado += "\n"
            resultado += "\n\n( Vista previa: " + str(l) + "x" + str(l)
            resultado += " de " + str(n) + "x" + str(n) + " )"
            return resultado

        for i in range(n):                   # Muestra la matriz completa.
            for j in range(n):
                resultado += f"{M[i][j]:6}"
                if j < n - 1:
                    resultado += "   "
            if i < n - 1:
                resultado += "\n"
        return resultado

    def _arbol_a_dict(self, nodo):
        """Convierte el arbol BST (de NodoJSON) a un diccionario Python anidado.

        La funcion guardar_arbol_json de GestorArchivos recibe un dict (no un NodoJSON)
        para mantener el gestor desacoplado de la clase NodoJSON.
        Esta funcion hace la conversion de forma recursiva.

        Retorna None para nodos inexistentes (que se convertiran a "null" en JSON).
        """
        if nodo is None:                     # Rama vacia => None en Python => null en JSON.
            return None
        return {
            "valor":     nodo.dato["valor"],
            "cantidad":  nodo.dato["cantidad"],
            "izquierda": self._arbol_a_dict(nodo.izquierda),  # Recursion por la izquierda.
            "derecha":   self._arbol_a_dict(nodo.derecha),    # Recursion por la derecha.
        }

    def _limpiar_texto(self, texto):
        """Elimina espacios al inicio y al final del string sin usar .strip().

        ALGORITMO:
          1. Avanza desde el inicio mientras el caracter sea espacio.
          2. Retrocede desde el final mientras el caracter sea espacio.
          3. Retorna el substring entre los dos punteros.
        Se implementa manualmente para cumplir la restriccion de no usar metodos
        de string avanzados como .strip(), .lstrip() o .rstrip().
        """
        i = 0                                # Puntero que avanza desde el inicio.
        while i < len(texto) and texto[i] == " ":
            i += 1                           # Salta los espacios del inicio.
        j = len(texto) - 1                   # Puntero que retrocede desde el final.
        while j >= 0 and texto[j] == " ":
            j -= 1                           # Salta los espacios del final.
        if i > j:                            # Todo el string era espacios.
            return ""
        return texto[i:j + 1]                # Substring sin espacios en los extremos.

    def _es_entero(self, texto):
        """Verifica si un string representa un numero entero valido sin usar int() primero.

        ALGORITMO: Recorre cada caracter y verifica que este en el rango '0'-'9'.
        Permite un signo negativo opcional al inicio.
        Retorna False si hay cualquier caracter que no sea digito (o signo al inicio).

        Por que sin int() primero: int("abc") lanza una excepcion que habria que
        capturar con try/except. Esta version es mas explicita y no usa excepciones
        para control de flujo.
        """
        if len(texto) == 0:                  # String vacio no es un entero.
            return False
        inicio = 0
        if texto[0] == "-":                  # Permite el signo negativo (ej: "-5").
            inicio = 1
        if inicio == len(texto):             # Solo el signo, sin digitos (ej: "-").
            return False
        i = inicio
        while i < len(texto):
            if texto[i] < "0" or texto[i] > "9":  # Caracter fuera del rango '0'-'9'.
                return False
            i += 1
        return True                          # Todos los caracteres son digitos (o hay signo al inicio).

    # ==========================================================================
    # ACCION PRINCIPAL: GENERAR MATRICES, ANALISIS Y ARBOLES
    # ==========================================================================

    def generar(self):
        """Ejecuta el flujo completo cuando el usuario hace clic en 'Generar'.

        PASOS EN ORDEN:
          1. Valida el valor de n ingresado por el usuario.
          2. Crea la matriz A y calcula A3.
          3. Analiza ambas matrices (pares, impares, primos, etc.).
          4. Cuenta repeticiones de cada valor.
          5. Construye los arboles BST equilibrados de frecuencias.
          6. Crea los vectores ordenados (ascendente y descendente).
          7. Muestra las matrices en los widgets Text.
          8. Genera el dibujo ASCII de los arboles.
          9. Mide y estima la memoria.
          10. Construye el texto del panel de resumen.
          11. Guarda los archivos JSON de los arboles.
        """

        # --- VALIDACION DE ENTRADA ---
        texto_n = self._limpiar_texto(self.entry_n.get()) # Lee el texto del campo y quita espacios.
        if not self._es_entero(texto_n):          # Verifica que sea un numero entero.
            messagebox.showerror("Error", "Ingrese un valor entero para n.")
            return                                # Detiene la ejecucion si la entrada no es valida.
        n = int(texto_n)                          # Convierte el texto validado a entero.

        if n < 4:                                 # Restriccion minima: una matriz 4x4 es el minimo util.
            messagebox.showerror("Error", "n debe ser mayor o igual a 4.")
            return
        if n > MAX_N:                             # Restriccion maxima: evita calculos que consumen demasiado.
            messagebox.showerror("Error",
                "n supera el limite de " + str(MAX_N) +
                ". El calculo de A3 (O(n3)) consumiria demasiada RAM.")
            return
        if n > 20:                                # Para n > 20 el archivo puede ser grande, se avisa.
            ok = messagebox.askyesno("Advertencia",
                "n es grande. Se mostrara vista previa y se guardaran archivos .txt. Continuar?")
            if not ok:
                return                            # El usuario eligio No: cancela.

        self.status.config(text="Estado: generando matriz y calculando A3...")
        self.update_idletasks()  # Fuerza la actualizacion de la interfaz AHORA (sin esperar al mainloop).

        try:
            # ---- PASO 1: CREAR A Y CALCULAR A3 ----
            iniciar_medicion_memoria()            # Inicia tracemalloc ANTES de crear las estructuras.
            self.A = crear_matriz(n)              # Genera matriz A con n*n valores aleatorios 0-9.

            A2 = None                             # Se calcula solo para matrices pequenas (para medicion de memoria).
            if n > 100:                           # Para n > 100, calcula y guarda A3 sin cargar todo en RAM.
                self.gestor.guardar_matriz("matriz_A.txt", self.A, "Matriz A")
                self.status.config(text="Estado: guardando A3 fila por fila...")
                self.update_idletasks()
                ruta_a3 = self.gestor.CARPETA + "\\" + "matriz_A3.txt"
                self.A3 = guardar_A3_directo_txt(self.A, ruta_a3)
            else:                                 # Para n <= 100, calcula A3 en memoria y guarda ambas.
                A2 = multiplicar_matrices(self.A, self.A) # A2 = A * A (se guarda para medir su memoria).
                self.A3 = multiplicar_matrices(A2, self.A) # A3 = A2 * A.
                self.gestor.guardar_matriz("matriz_A.txt",  self.A,  "Matriz A")
                self.gestor.guardar_matriz("matriz_A3.txt", self.A3, "Matriz A3")

            # ---- PASO 2: ANALIZAR MATRICES ----
            analisis_A  = analizar_matriz(self.A)  # Clasifica elementos de A en pares, impares, etc.
            analisis_A3 = analizar_matriz(self.A3) # Clasifica elementos de A3.

            # ---- PASO 3: CONTAR REPETICIONES ----
            rep_A  = contar_repeticiones(self.A)   # Dict {valor: frecuencia} para A.
            rep_A3 = contar_repeticiones(self.A3)  # Dict {valor: frecuencia} para A3.

            # ---- PASO 4: CONSTRUIR ARBOLES BST EQUILIBRADOS ----
            lista_A  = frecuencias_a_json_ordenado(rep_A) # Lista ordenada [{"valor":v,"cantidad":c}, ...].
            self.arbol_A  = construir_arbol_json_equilibrado(lista_A,  0, len(lista_A)  - 1) # BST de A.
            lista_A3 = frecuencias_a_json_ordenado(rep_A3)
            self.arbol_A3 = construir_arbol_json_equilibrado(lista_A3, 0, len(lista_A3) - 1) # BST de A3.

            # ---- PASO 5: VECTORES ORDENADOS ----
            vec_A   = matriz_a_vector(self.A)      # Aplana A en un vector de n^2 elementos.
            vec_A3  = matriz_a_vector(self.A3)
            va_asc  = ordenar_ascendente(vec_A)    # Ordena de menor a mayor.
            va3_asc = ordenar_ascendente(vec_A3)
            va_desc = invertir_vector(va_asc)      # Invierte para obtener orden descendente.
            va3_desc= invertir_vector(va3_asc)

            # ---- PASO 6: MOSTRAR MATRICES EN LA INTERFAZ ----
            self._set_text(self.text_A,  self._mat_to_str(self.A))   # Actualiza el widget Text de la pestana A.
            self._set_text(self.text_A3, self._mat_to_str(self.A3))

            # ---- PASO 7: DIBUJO ASCII DE LOS ARBOLES ----
            if len(lista_A) <= 63:               # Limite de 63 nodos para que el ASCII no sea demasiado ancho.
                ascii_A = arbol_a_ascii(self.arbol_A)
            else:
                ascii_A = "Arbol A generado (" + str(len(lista_A)) + " nodos). Busqueda disponible."
            if len(lista_A3) <= 63:
                ascii_A3 = arbol_a_ascii(self.arbol_A3)
            else:
                ascii_A3 = "Arbol A3 generado (" + str(len(lista_A3)) + " nodos). Busqueda disponible."
            self._set_text(self.txt_arbol,
                           "ARBOL A:\n" + ascii_A + "\n\nARBOL A3:\n" + ascii_A3)

            # ---- PASO 8: MEDICION DE MEMORIA ----
            mem_actual, mem_pico = obtener_memoria_actual_y_pico() # Lee memoria actual y pico de tracemalloc.
            detener_medicion_memoria()             # Detiene tracemalloc.
            estimacion = estimar_memoria_estructuras( # Estimacion profunda de cada estructura.
                A=self.A,
                A2=A2,
                A3=self.A3,
                vector={"A": vec_A, "A3": vec_A3},
                frecuencias={"A": rep_A, "A3": rep_A3},
                arbol={"A": self.arbol_A, "A3": self.arbol_A3}
            )

            # ---- VALIDACION: verifica que el arbol representa la matriz correctamente ----
            validacion_A = {
                "elementos_matriz": n * n,          # Total de celdas de la matriz (n^2).
                "elementos_arbol": contar_elementos_representados_arbol(self.arbol_A), # Suma de frecuencias del arbol.
                "valores_unicos": len(lista_A),     # Cuantos valores distintos tiene A.
                "nodos_arbol": contar_nodos_arbol_json(self.arbol_A), # Cuantos nodos tiene el BST.
                "altura": altura_arbol_json(self.arbol_A) # Cuantos niveles tiene el BST.
            }
            validacion_A3 = {
                "elementos_matriz": n * n,
                "elementos_arbol": contar_elementos_representados_arbol(self.arbol_A3),
                "valores_unicos": len(lista_A3),
                "nodos_arbol": contar_nodos_arbol_json(self.arbol_A3),
                "altura": altura_arbol_json(self.arbol_A3)
            }

            # ---- PASO 9: CONSTRUIR Y MOSTRAR EL RESUMEN EN EL PANEL DERECHO ----
            salida = self.constructor.construir_salida(
                analisis_A, analisis_A3, rep_A, rep_A3,
                va_asc, va_desc, va3_asc, va3_desc,
                mem_actual, mem_pico, estimacion,
                validacion_A, validacion_A3
            )
            self._set_text(self.txt_result, salida) # Actualiza el widget Text del panel de resumen.

            # ---- PASO 10: GUARDAR JSON DE LOS ARBOLES ----
            self.gestor.guardar_arbol_json("arbol_A.json",  self._arbol_a_dict(self.arbol_A),  "ArbolA")
            self.gestor.guardar_arbol_json("arbol_A3.json", self._arbol_a_dict(self.arbol_A3), "ArbolA3")

            if n > 20:
                self.status.config(text="Estado: generado. Vista previa en pantalla. Archivos en /resultados.")
            else:
                self.status.config(text="Estado: generado correctamente. Ya puedes buscar un numero.")

        except Exception as e:                     # Captura cualquier error del backend para mostrarlo sin cerrar la app.
            messagebox.showerror("Error", "Ocurrio un problema al generar:\n" + str(e))
            self.status.config(text="Estado: error al generar.")

    # ==========================================================================
    # ACCION SECUNDARIA: BUSQUEDA COMPARATIVA
    # ==========================================================================

    def buscar(self):
        """Ejecuta la busqueda comparativa entre matriz y arbol BST al hacer clic en 'Buscar'.

        FLUJO:
          1. Valida que existan datos (se haya generado antes).
          2. Valida el numero ingresado.
          3. Busca el numero en la MATRIZ A y en el ARBOL A (con medicion de tiempo promedio).
          4. Busca el numero en la MATRIZ A3 y en el ARBOL A3.
          5. Determina cual metodo fue mas rapido en cada caso.
          6. Agrega el resultado al panel de resumen (sin borrar el resumen anterior).

        MEDICION DE TIEMPO:
          Se ejecutan 1000 repeticiones y se calcula el promedio para suavizar
          las variaciones de tiempo causadas por el sistema operativo.
        """
        if self.A is None or self.A3 is None or self.arbol_A is None or self.arbol_A3 is None:
            messagebox.showwarning("Aviso", "Primero genera la matriz A y A3.")
            return

        texto_b = self._limpiar_texto(self.entry_buscado.get()) # Lee y limpia el numero a buscar.
        if not self._es_entero(texto_b):
            messagebox.showerror("Error", "Ingrese un numero entero para buscar.")
            return
        buscado = int(texto_b)           # Numero entero que se buscara en A, A3, arbol_A y arbol_A3.

        self.status.config(text="Estado: buscando...")
        self.update_idletasks()

        repeticiones = 1000              # Promedio sobre 1000 ejecuciones para resultados estables.

        # ---- BUSQUEDAS EN A ----
        # buscar_y_contar_en_matriz retorna (encontrado, cantidad); medir_tiempo_promedio retorna (resultado, tiempo_ns).
        res_mat_A,  t_mat_A  = medir_tiempo_promedio(buscar_y_contar_en_matriz, self.A,       buscado, repeticiones)
        enc_mat_A, cant_mat_A = res_mat_A  # Desempaqueta la tupla del resultado de buscar_y_contar.
        res_arb_A,  t_arb_A  = medir_tiempo_promedio(buscar_en_arbol_json,      self.arbol_A, buscado, repeticiones)
        # buscar_en_arbol_json retorna el dict {"valor":v,"cantidad":c} si encontro, None si no.

        # ---- BUSQUEDAS EN A3 ----
        res_mat_A3, t_mat_A3  = medir_tiempo_promedio(buscar_y_contar_en_matriz, self.A3,        buscado, repeticiones)
        enc_mat_A3, cant_mat_A3 = res_mat_A3
        res_arb_A3, t_arb_A3  = medir_tiempo_promedio(buscar_en_arbol_json,      self.arbol_A3,  buscado, repeticiones)

        # Extrae la cantidad del resultado del arbol (si se encontro).
        if res_arb_A is not None:
            cant_arb_A = res_arb_A["cantidad"]  # Frecuencia almacenada en el nodo del arbol.
        else:
            cant_arb_A = 0                       # No encontrado => frecuencia 0.

        if res_arb_A3 is not None:
            cant_arb_A3 = res_arb_A3["cantidad"]
        else:
            cant_arb_A3 = 0

        # ---- DETERMINACION DE METODO MAS RAPIDO ----
        # Se usan if/else en lugar del operador ternario (restriccion academica).
        if enc_mat_A:
            txt_mat_A = "encontrado"
        else:
            txt_mat_A = "no encontrado"
        if res_arb_A is not None:
            txt_arb_A = "encontrado"
        else:
            txt_arb_A = "no encontrado"
        if t_arb_A < t_mat_A:            # El arbol fue mas rapido.
            rapido_A = "arbol BST"
        elif t_mat_A < t_arb_A:          # La matriz fue mas rapida (puede ocurrir con n muy pequeno).
            rapido_A = "matriz"
        else:
            rapido_A = "empate"          # Tiempos identicos (raro pero posible).

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

        # ---- CONSTRUCCION DEL MENSAJE DE RESULTADO ----
        msg = "\n\nBUSQUEDA: " + str(buscado) + "\n"
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

        self._add_text(self.txt_result, msg) # Agrega el resultado al panel sin borrar el resumen.
        self.status.config(text="Estado: busqueda completada.")


# ==============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==============================================================================

if __name__ == "__main__":
    # Este bloque solo se ejecuta si se corre este archivo directamente:
    #   python interfaz_grafica.py
    # Si se importa desde otro modulo (como medir_memoria_componentes.py),
    # este bloque NO se ejecuta.
    app = App()        # Crea la ventana principal (llama a __init__ que construye toda la UI).
    app.mainloop()     # Inicia el bucle de eventos de Tkinter: espera interacciones del usuario.
                       # mainloop() solo termina cuando el usuario cierra la ventana.
