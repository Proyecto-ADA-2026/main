import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import shutil

MAX_N = 150

# tksheet es opcional. Solo se usa para mostrar matrices en forma de tabla.
# Si no está instalado, el programa sigue funcionando y permite abrir los archivos .txt.
try:
    import tksheet
    TKSHEET_DISPONIBLE = True
except ImportError:
    TKSHEET_DISPONIBLE = False


# =========================================================
# FRONTEND (INTERFAZ)
# =========================================================
# interfaz_grafica.py = interfaz/frontend
# proyecto_final.py = lógica algorítmica/backend

from Proyecto_final import (
    crear_matriz,
    calcular_A3,
    guardar_A3_directo_txt,
    analizar_matriz,
    contar_repeticiones,
    frecuencias_a_json_ordenado,
    matriz_a_vector,
    ordenar_ascendente,
    invertir_vector,
    construir_arbol_json_equilibrado,
    buscar_y_contar_en_matriz,
    buscar_en_arbol_json,
    medir_tiempo,
    arbol_a_ascii,
    exportar_arbol_dot,
    iniciar_medicion_memoria,
    obtener_memoria_actual_y_pico,
    detener_medicion_memoria,
    estimar_memoria_matriz,
    contar_nodos_arbol_json,
    altura_arbol_json,
    recorrido_inorden_json,
)


# =========================================================
# INTERFAZ GRÁFICA
# =========================================================


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Análisis de Matriz A, A³ y Árbol Binario")
        self.geometry("1280x820")
        self.minsize(1080, 720)
        self.configure(bg="#f4f6f9")

        self.A = None
        self.A3 = None
        self.arbol_A = None
        self.arbol_A3 = None

        self._configurar_estilos()
        self._build_ui()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Main.TFrame", background="#f4f6f9")
        style.configure("Header.TFrame", background="#1f4e79")

        style.configure(
            "Header.TLabel",
            background="#1f4e79",
            foreground="white",
            font=("Segoe UI", 18, "bold"),
        )

        style.configure(
            "HeaderSub.TLabel",
            background="#1f4e79",
            foreground="#d9e8f5",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Card.TLabelframe",
            background="#ffffff",
            borderwidth=1,
            relief="solid",
        )

        style.configure(
            "Card.TLabelframe.Label",
            background="#f4f6f9",
            foreground="#1f4e79",
            font=("Segoe UI", 11, "bold"),
        )

        style.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
        style.configure("TEntry", padding=6, font=("Segoe UI", 10))

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            background="#1f4e79",
            foreground="white",
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#173a5c")],
            foreground=[("active", "white")],
        )

        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 6),
        )

    def _build_ui(self):
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

        # Segunda fila de botones secundarios
        botones_frame = ttk.Frame(principal, style="Main.TFrame")
        botones_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.btn_abrir_A = ttk.Button(
            botones_frame,
            text="Abrir TXT Matriz A",
            command=lambda: self.abrir_archivo_resultado("matriz_A.txt"),
        )
        self.btn_abrir_A.pack(side="left", padx=5)

        self.btn_abrir_A3 = ttk.Button(
            botones_frame,
            text="Abrir TXT Matriz A³",
            command=lambda: self.abrir_archivo_resultado("matriz_A3.txt"),
        )
        self.btn_abrir_A3.pack(side="left", padx=5)

        self.btn_ver_grafico_A = ttk.Button(
            botones_frame,
            text="Ver gráfico Árbol A",
            command=lambda: self.generar_imagen_graphviz("arbol_A.dot", "arbol_A.png"),
        )
        self.btn_ver_grafico_A.pack(side="left", padx=5)

        self.btn_ver_grafico_A3 = ttk.Button(
            botones_frame,
            text="Ver gráfico Árbol A³",
            command=lambda: self.generar_imagen_graphviz("arbol_A3.dot", "arbol_A3.png"),
        )
        self.btn_ver_grafico_A3.pack(side="left", padx=5)

        self.btn_ver_tabla_A = ttk.Button(
            botones_frame,
            text="Ver tabla Matriz A",
            command=lambda: self.mostrar_matriz_en_tabla("Matriz A", self.A),
        )
        self.btn_ver_tabla_A.pack(side="left", padx=5)

        self.btn_ver_tabla_A3 = ttk.Button(
            botones_frame,
            text="Ver tabla Matriz A³",
            command=lambda: self.mostrar_matriz_en_tabla("Matriz A³", self.A3),
        )
        self.btn_ver_tabla_A3.pack(side="left", padx=5)

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

    def _text_scroll(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        text = tk.Text(
            frame,
            wrap="none",
            font=("Consolas", 11),
            bg="#fbfbfb",
            fg="#1f1f1f",
            relief="flat",
            padx=10,
            pady=10,
        )

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        text.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        text.config(state="disabled")
        return text

    def _set_text(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.config(state="disabled")

    def _append_text(self, widget, content):
        widget.config(state="normal")
        widget.insert("end", content)
        widget.see("end")
        widget.config(state="disabled")

    def guardar_matriz_en_txt(self, nombre_archivo, matriz, titulo):
        # Guarda en la carpeta resultados para mantener los archivos organizados.
        carpeta_resultados = "resultados"
        os.makedirs(carpeta_resultados, exist_ok=True)
        ruta_completa = os.path.join(carpeta_resultados, nombre_archivo)
        n = len(matriz)
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(f"{titulo}\n")
            f.write(f"Tamaño: {n}x{n}\n")
            f.write("=" * 60 + "\n\n")
            for fila in matriz:
                f.write("   ".join(f"{v:10}" for v in fila) + "\n")

    def _mat_to_str(self, M, vista_previa_dim=10):
        n = len(M)

        # Vista previa si es grande
        if n > 20:
            limite = min(vista_previa_dim, n)
            lineas = []
            for i in range(limite):
                lineas.append("   ".join(f"{v:6}" for v in M[i][:limite]))
            return (
                "\n".join(lineas)
                + f"\n\n( Vista previa: {limite}x{limite} de la matriz {n}x{n} )"
            )

        # Pequeña: toda
        lineas = []
        for fila in M:
            lineas.append("   ".join(f"{v:6}" for v in fila))
        return "\n".join(lineas)

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
                
                # Calcula y guarda A³ de forma optimizada (fila por fila, sin guardar todo en memoria antes)
                self.A3 = guardar_A3_directo_txt(self.A, os.path.join("resultados", "matriz_A3.txt"))
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

            rep_A = contar_repeticiones(self.A)
            lista_json_A = frecuencias_a_json_ordenado(rep_A)
            self.arbol_A = construir_arbol_json_equilibrado(lista_json_A, 0, len(lista_json_A) - 1)

            rep_A3 = contar_repeticiones(self.A3)
            lista_json_A3 = frecuencias_a_json_ordenado(rep_A3)
            self.arbol_A3 = construir_arbol_json_equilibrado(lista_json_A3, 0, len(lista_json_A3) - 1)

            # Paso 5: vectores ordenados
            vec_A   = matriz_a_vector(self.A)
            vec_A3  = matriz_a_vector(self.A3)
            va_asc  = ordenar_ascendente(vec_A)
            va3_asc = ordenar_ascendente(vec_A3)
            va_desc = invertir_vector(va_asc)
            va3_desc= invertir_vector(va3_asc)

            # UI: vista previa o matriz completa
            self._set_text(self.text_A, self._mat_to_str(self.A))
            self._set_text(self.text_A3, self._mat_to_str(self.A3))

            # Mostrar ASCII del árbol solo si el árbol JSON no es demasiado grande
            if len(lista_json_A) <= 63:
                ascii_arbol_A = arbol_a_ascii(self.arbol_A)
            else:
                ascii_A = "Arbol A generado (" + str(len(lista_json_A)) + " nodos). Busqueda disponible."
            if len(lista_json_A3) <= 63:
                ascii_A3 = arbol_a_ascii(self.arbol_A3)
            else:
                ascii_A3 = "Arbol A3 generado (" + str(len(lista_json_A3)) + " nodos). Busqueda disponible."
            self._set_text(self.txt_arbol,
                           "ARBOL A:\n" + ascii_A + "\n\nARBOL A3:\n" + ascii_A3)

            # Paso 8: memoria
            mem_actual, mem_pico = obtener_memoria_actual_y_pico()
            detener_medicion_memoria()
            estimacion = estimar_memoria_matriz(n)

            def resumen_analisis(nombre, analisis):
                return (
                    f"{nombre}\n"
                    f"{'-' * len(nombre)}\n"
                    f"Pares: {analisis['pares']['cantidad']}\n"
                    f"Impares: {analisis['impares']['cantidad']}\n"
                    f"Primos: {analisis['primos']['cantidad']}\n"
                    f"Perfectos: {analisis['perfectos']['cantidad']}\n"
                    f"Cuadrados perfectos: {analisis['cuadrados']['cantidad']}\n"
                )

            salida = []
            salida.append(resumen_analisis("RESUMEN MATRIZ A", analisis_A))
            salida.append("\nRepeticiones A:\n")
            # Usar nuestro propio ordenamiento para las claves (evitar sorted())
            if rep_A:
                claves_A = ordenar_ascendente(list(rep_A.keys()))
                salida.append(
                    ", ".join(f"{k}: {rep_A[k]}" for k in claves_A)
                )
            else:
                salida.append("Sin datos")

            salida.append("\n\n")
            salida.append(resumen_analisis("RESUMEN MATRIZ A³", analisis_A3))
            salida.append("\nRepeticiones A³:\n")
            if rep_A3:
                claves_A3 = ordenar_ascendente(list(rep_A3.keys()))
                salida.append(
                    ", ".join(f"{k}: {rep_A3[k]}" for k in claves_A3)
                )
            else:
                salida.append("Sin datos")

            salida.append("\n\nVECTORES ORDENADOS\n")
            salida.append("------------------\n")

            salida.append("A ascendente:\n")
            texto_A = str(va_asc)
            salida.append(texto_A[:1200] + ("..." if len(texto_A) > 1200 else ""))

            salida.append("\n\nA descendente:\n")
            texto_A_desc = str(va_desc)
            salida.append(texto_A_desc[:1200] + ("..." if len(texto_A_desc) > 1200 else ""))

            salida.append("\n\nA³ ascendente:\n")
            texto_A3 = str(va3_asc)
            salida.append(texto_A3[:1200] + ("..." if len(texto_A3) > 1200 else ""))

            salida.append("\n\nA³ descendente:\n")
            texto_A3_desc = str(va3_desc)
            salida.append(texto_A3_desc[:1200] + ("..." if len(texto_A3_desc) > 1200 else ""))
            salida.append("\n\nMEMORIA\n")
            salida.append("------\n")
            salida.append(f"Estimación A: {estimacion} bytes\n")
            salida.append(f"Memoria actual: {mem_actual // 1024} KB\n")
            salida.append(f"Memoria pico: {mem_pico // 1024} KB\n")
            self._set_text(self.txt_result, "".join(salida))

            if n > 20:
                self.status.config(
                    text="Estado: matriz generada. Vista previa en interfaz y .txt guardados (matriz_A.txt, matriz_A3.txt)."
                )
            else:
                self.status.config(text="Estado: matriz generada correctamente. Ya puedes buscar un número.")

            # Exportar DOT para árboles pequeños y generar un mensaje para los grandes.
            nodos_A = self.contar_nodos_arbol(self.arbol_A)
            nodos_A3 = self.contar_nodos_arbol(self.arbol_A3)

            if nodos_A <= 100:
                contenido_A = exportar_arbol_dot(self.arbol_A, "ArbolA")
            else:
                contenido_A = (
                    "// El árbol fue generado correctamente, pero no se exporta completo "
                    "porque tiene demasiados nodos.\n"
                    f"Nodos: {nodos_A}\n"
                )

            if nodos_A3 <= 100:
                contenido_A3 = exportar_arbol_dot(self.arbol_A3, "ArbolA3")
            else:
                contenido_A3 = (
                    "// El árbol fue generado correctamente, pero no se exporta completo "
                    "porque tiene demasiados nodos.\n"
                    f"Nodos: {nodos_A3}\n"
                )

            self.guardar_texto_en_archivo("arbol_A.dot", contenido_A)
            self.guardar_texto_en_archivo("arbol_A3.dot", contenido_A3)

        except Exception as error:
            messagebox.showerror("Error", f"Ocurrió un problema al generar la matriz:\n{error}")
            self.status.config(text="Estado: ocurrió un error al generar la matriz.")

    def buscar(self):
        if (
            self.A is None
            or self.A3 is None
            or self.arbol_A is None
            or self.arbol_A3 is None
        ):
            messagebox.showwarning("Aviso", "Primero genera la matriz A y A³.")
            return

        texto_b = self._limpiar_texto(self.entry_buscado.get())
        if not self._es_entero(texto_b):
            messagebox.showerror("Error", "Ingrese un numero entero para buscar.")
            return
        buscado = int(texto_b)

        self.status.config(text="Estado: buscando...")
        self.update_idletasks()

        resultado_matriz_A, tiempo_matriz_A = medir_tiempo(buscar_y_contar_en_matriz, self.A, buscado)
        encontrado_matriz_A, cantidad_matriz_A = resultado_matriz_A
        resultado_arbol_A, tiempo_arbol_A = medir_tiempo(buscar_en_arbol_json, self.arbol_A, buscado)

        resultado_matriz_A3, tiempo_matriz_A3 = medir_tiempo(buscar_y_contar_en_matriz, self.A3, buscado)
        encontrado_matriz_A3, cantidad_matriz_A3 = resultado_matriz_A3
        resultado_arbol_A3, tiempo_arbol_A3 = medir_tiempo(buscar_en_arbol_json, self.arbol_A3, buscado)

        cantidad_arbol_A = resultado_arbol_A["cantidad"] if resultado_arbol_A is not None else 0
        cantidad_arbol_A3 = resultado_arbol_A3["cantidad"] if resultado_arbol_A3 is not None else 0

        mensaje = (
            "\n\nBÚSQUEDA DEL VALOR " + str(buscado) + "\n"
            "-------------------\n"
            "Matriz A:\n"
            f"En matriz: {'encontrado' if encontrado_matriz_A else 'no encontrado'}, cantidad: {cantidad_matriz_A}, tiempo: {tiempo_matriz_A} ns\n"
            f"En árbol JSON: {'encontrado' if resultado_arbol_A is not None else 'no encontrado'}, cantidad: {cantidad_arbol_A}, tiempo: {tiempo_arbol_A} ns\n"
            f"Más rápido: {'árbol JSON' if tiempo_arbol_A < tiempo_matriz_A else ('matriz' if tiempo_matriz_A < tiempo_arbol_A else 'empate')}\n\n"
            "Matriz A³:\n"
            f"En matriz: {'encontrado' if encontrado_matriz_A3 else 'no encontrado'}, cantidad: {cantidad_matriz_A3}, tiempo: {tiempo_matriz_A3} ns\n"
            f"En árbol JSON: {'encontrado' if resultado_arbol_A3 is not None else 'no encontrado'}, cantidad: {cantidad_arbol_A3}, tiempo: {tiempo_arbol_A3} ns\n"
            f"Más rápido: {'árbol JSON' if tiempo_arbol_A3 < tiempo_matriz_A3 else ('matriz' if tiempo_matriz_A3 < tiempo_arbol_A3 else 'empate')}\n"
        )

        self._append_text(self.txt_result, mensaje)
        self.status.config(text="Estado: búsqueda completada.")

    def generar_imagen_graphviz(self, archivo_dot, archivo_salida):
        # Reemplazado: ahora se busca el ejecutable 'dot' y se usa su ruta completa
        ruta_dot = os.path.join("resultados", archivo_dot)
        ruta_salida = os.path.join("resultados", archivo_salida)

        # Verificar si el archivo DOT existe
        if not os.path.exists(ruta_dot):
            messagebox.showwarning(
                "Archivo no encontrado",
                "Primero genera la matriz para crear el árbol."
            )
            return

        # Verificar contenido por indicación de árbol grande (si aplica)
        try:
            with open(ruta_dot, "r", encoding="utf-8") as f:
                contenido = f.read()
                if "demasiados nodos" in contenido:
                    messagebox.showinfo(
                        "Árbol muy grande",
                        "El árbol fue generado, pero no se visualiza completo porque tiene demasiados nodos. "
                        "Use n pequeño (por ejemplo 4 a 8) para ver el árbol visual."
                    )
                    return
        except Exception:
            pass

        # Localizar ejecutable 'dot'
        dot_exec = self.find_dot_executable()
        if not dot_exec:
            messagebox.showerror(
                "Graphviz no encontrado",
                "Graphviz no está instalado o no está agregado al PATH.\n\n"
                "Instale Graphviz desde https://graphviz.org/download/ y verifique con:\n"
                "  dot -V"
            )
            return

        # Ejecutar Graphviz usando la ruta completa encontrada
        try:
            subprocess.run([dot_exec, "-Tpng", ruta_dot, "-o", ruta_salida], check=True, capture_output=True)
            os.startfile(ruta_salida)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error al generar imagen", f"No se pudo generar la imagen del árbol.\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

    def find_dot_executable(self):
        """
        Busca el ejecutable 'dot' de Graphviz únicamente en el PATH.

        Graphviz se usa solo para visualizar el árbol en imagen.
        No construye el árbol ni reemplaza ningún algoritmo del proyecto.
        """
        try:
            return shutil.which("dot")
        except Exception:
            return None

    def guardar_texto_en_archivo(self, nombre_archivo, contenido):
        carpeta_resultados = "resultados"
        os.makedirs(carpeta_resultados, exist_ok=True)
        ruta_completa = os.path.join(carpeta_resultados, nombre_archivo)
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def abrir_archivo_resultado(self, nombre_archivo):
        ruta_archivo = os.path.join("resultados", nombre_archivo)

        if not os.path.exists(ruta_archivo):
            messagebox.showwarning(
                "Archivo no encontrado",
                "Primero genera la matriz para crear el archivo."
            )
            return

        try:
            os.startfile(ruta_archivo)
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el archivo:\n{error}"
            )

    def abrir_archivo_txt(self, nombre_archivo):
        self.abrir_archivo_resultado(nombre_archivo)

    def contar_nodos_arbol(self, raiz):
        if raiz is None:
            return 0
        return 1 + self.contar_nodos_arbol(raiz.izquierda) + self.contar_nodos_arbol(raiz.derecha)

    def mostrar_matriz_en_tabla(self, titulo, matriz):
        if matriz is None:
            messagebox.showwarning(
                "Matriz no generada",
                "Primero genera la matriz para poder mostrarla."
            )
            return

        if not TKSHEET_DISPONIBLE:
            messagebox.showinfo(
                "tksheet no disponible",
                "Para ver la tabla instala tksheet o abre el archivo .txt."
            )
            return

        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("900x600")

        hoja = tksheet.Sheet(ventana, data=matriz)
        hoja.pack(fill="both", expand=True)

        hoja.enable_bindings(
            ("single_select", "row_select", "column_width_resize", "arrowkeys", "right_click_popup_menu")
        )
# MAIN
# =========================================================

if __name__ == "__main__":
    app = App()        # Crea la ventana principal
    app.mainloop()     # Inicia el bucle de eventos de tkinter
