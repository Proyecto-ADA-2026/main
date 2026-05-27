import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import shutil

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
    analizar_matriz,
    contar_repeticiones,
    matriz_a_vector,
    ordenar_ascendente,
    construir_arbol_equilibrado,
    buscar_en_matriz,
    buscar_en_arbol,
    medir_tiempo,
    arbol_a_ascii,
    exportar_arbol_dot,
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

        header = ttk.Frame(principal, style="Header.TFrame")
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Matriz A, A³ y Árbol Binario",
            style="Header.TLabel",
        ).pack(anchor="w", padx=20, pady=(14, 2))

        ttk.Label(
            header,
            text="Generación, análisis, ordenamiento y búsqueda comparativa",
            style="HeaderSub.TLabel",
        ).pack(anchor="w", padx=20, pady=(0, 14))

        top = ttk.Frame(principal, style="Main.TFrame")
        top.pack(fill="x", padx=20, pady=(14, 6))

        ttk.Label(top, text="Tamaño n (n ≥ 4):").pack(side="left")

        self.entry_n = ttk.Entry(top, width=10)
        self.entry_n.pack(side="left", padx=8)
        self.entry_n.insert(0, "4")

        self.btn_generar = ttk.Button(
            top,
            text="Generar matriz A y A³",
            style="Primary.TButton",
            command=self.generar,
        )
        self.btn_generar.pack(side="left", padx=10)

        tk.Label(
            top,
            text="(Si n > 20 se mostrará vista previa. Se guarda en .txt.)",
            bg="#f4f6f9",
            fg="#666666",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=10)

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

        buscar_frame = tk.LabelFrame(
            principal,
            text="Búsqueda",
            bg="#f4f6f9",
            fg="#333333",
            font=("Segoe UI", 9),
        )
        buscar_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(
            buscar_frame,
            text="Número a buscar:",
            bg="#f4f6f9",
            fg="#222222",
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(12, 5), pady=8)

        self.entry_buscado = tk.Entry(
            buscar_frame,
            width=10,
            font=("Segoe UI", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
        )
        self.entry_buscado.pack(side="left", padx=5)

        self.btn_buscar = tk.Button(
            buscar_frame,
            text="Buscar en matriz y árbol",
            command=self.buscar,
            font=("Segoe UI", 9),
            bg="#f5f5f5",
            fg="#111111",
            activebackground="#e6e6e6",
            activeforeground="#000000",
            relief="raised",
            bd=1,
            padx=8,
            pady=2,
            cursor="hand2",
        )
        self.btn_buscar.pack(side="left", padx=10)

        centro = ttk.Frame(principal, style="Main.TFrame")
        centro.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        left = ttk.LabelFrame(centro, text="Matrices generadas", style="Card.TLabelframe")
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.notebook = ttk.Notebook(left)
        self.tab_A = ttk.Frame(self.notebook)
        self.tab_A3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_A, text="Matriz A")
        self.notebook.add(self.tab_A3, text="Matriz A³")
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.text_A = self._crear_texto_scroll(self.tab_A)
        self.text_A3 = self._crear_texto_scroll(self.tab_A3)

        right = ttk.LabelFrame(centro, text="Resumen y análisis", style="Card.TLabelframe")
        right.pack(side="left", fill="both", expand=False)

        self.txt_result = tk.Text(
            right,
            width=48,
            height=24,
            wrap="word",
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#222222",
            relief="flat",
            padx=10,
            pady=10,
        )
        scroll_result = ttk.Scrollbar(right, orient="vertical", command=self.txt_result.yview)
        self.txt_result.configure(yscrollcommand=scroll_result.set)
        self.txt_result.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll_result.pack(side="right", fill="y", padx=(0, 8), pady=8)

        self.txt_result.insert("1.0", "Aquí aparecerá el resumen del análisis.\n\nPrimero genera la matriz.")
        self.txt_result.config(state="disabled")

        arbol_frame = ttk.LabelFrame(
            principal,
            text="Árbol binario de búsqueda (matriz A y A³)",
            style="Card.TLabelframe",
        )
        arbol_frame.pack(fill="both", expand=False, padx=20, pady=(0, 10))

        self.txt_arbol = tk.Text(
            arbol_frame,
            height=10,
            wrap="none",
            font=("Consolas", 12),
            bg="#fbfbfb",
            fg="#1e1e1e",
            relief="flat",
            padx=10,
            pady=10,
        )
        scroll_arbol_y = ttk.Scrollbar(arbol_frame, orient="vertical", command=self.txt_arbol.yview)
        scroll_arbol_x = ttk.Scrollbar(arbol_frame, orient="horizontal", command=self.txt_arbol.xview)
        self.txt_arbol.configure(yscrollcommand=scroll_arbol_y.set, xscrollcommand=scroll_arbol_x.set)

        self.txt_arbol.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=(8, 0))
        scroll_arbol_y.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=(8, 0))
        scroll_arbol_x.grid(row=1, column=0, sticky="ew", padx=(8, 0), pady=(0, 8))

        arbol_frame.rowconfigure(0, weight=1)
        arbol_frame.columnconfigure(0, weight=1)

        self.txt_arbol.insert(
            "1.0",
            "Aquí se mostrará el árbol binario.\n\n(primero se muestra el árbol de A, luego el árbol de A³).",
        )
        self.txt_arbol.config(state="disabled")

        self.status = tk.Label(
            principal,
            text="Estado: esperando datos...",
            anchor="w",
            bg="#e8eef3",
            fg="#333333",
            font=("Segoe UI", 10, "bold"),
        )
        self.status.pack(fill="x", padx=20, pady=(0, 12), ipady=6)

    def _crear_texto_scroll(self, parent):
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
        try:
            n = int(self.entry_n.get().strip())
        except Exception:
            messagebox.showerror("Error", "Ingrese un valor entero para n.")
            return

        if n < 4:
            messagebox.showerror("Error", "n debe ser mayor o igual a 4.")
            return

        if n > 20:
            continuar = messagebox.askyesno(
                "Advertencia",
                "El valor de n es grande. Se mostrará una vista previa en la interfaz, y se guardarán matrices completas en .txt. ¿Deseas continuar?",
            )
            if not continuar:
                return

        self.status.config(text="Estado: generando matriz y calculando A³...")
        self.update_idletasks()

        try:
            self.A = crear_matriz(n)
            self.A3 = calcular_A3(self.A)

            analisis_A = analizar_matriz(self.A)
            analisis_A3 = analizar_matriz(self.A3)

            rep_A = contar_repeticiones(self.A)
            rep_A3 = contar_repeticiones(self.A3)

            vector_A = matriz_a_vector(self.A)
            vector_A3 = matriz_a_vector(self.A3)

            vector_A_asc = ordenar_ascendente(list(vector_A))
            vector_A3_asc = ordenar_ascendente(list(vector_A3))

            self.arbol_A = construir_arbol_equilibrado(vector_A_asc, 0, len(vector_A_asc) - 1)
            self.arbol_A3 = construir_arbol_equilibrado(vector_A3_asc, 0, len(vector_A3_asc) - 1)

            # Guardado obligatorio para matrices grandes (y también siempre si se desea; aquí siempre se guarda)
            self.guardar_matriz_en_txt("matriz_A.txt", self.A, "Matriz A")
            self.guardar_matriz_en_txt("matriz_A3.txt", self.A3, "Matriz A³")

            # UI: vista previa o matriz completa
            self._set_text(self.text_A, self._mat_to_str(self.A))
            self._set_text(self.text_A3, self._mat_to_str(self.A3))

            # Mostrar ASCII del árbol solo si el vector ordenado no es demasiado grande
            if len(vector_A_asc) <= 63:
                ascii_arbol_A = arbol_a_ascii(self.arbol_A)
            else:
                ascii_arbol_A = (
                    "Árbol A generado correctamente.\n"
                    f"No se muestra porque tiene {len(vector_A_asc)} nodos.\n"
                    "La búsqueda en árbol sigue funcionando normalmente."
                )

            if len(vector_A3_asc) <= 63:
                ascii_arbol_A3 = arbol_a_ascii(self.arbol_A3)
            else:
                ascii_arbol_A3 = (
                    "Árbol A³ generado correctamente.\n"
                    f"No se muestra porque tiene {len(vector_A3_asc)} nodos.\n"
                    "La búsqueda en árbol sigue funcionando normalmente."
                )

            self._set_text(
                self.txt_arbol,
                "ARBOL A:\n" + ascii_arbol_A + "\n\nARBOL A³:\n" + ascii_arbol_A3,
            )

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
            texto_A = str(vector_A_asc)
            salida.append(texto_A[:1200] + ("..." if len(texto_A) > 1200 else ""))

            salida.append("\n\nA³ ascendente:\n")
            texto_A3 = str(vector_A3_asc)
            salida.append(texto_A3[:1200] + ("..." if len(texto_A3) > 1200 else ""))

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

        try:
            buscado = int(self.entry_buscado.get().strip())
        except Exception:
            messagebox.showerror("Error", "Ingrese un número entero para buscar.")
            return

        self.status.config(text="Estado: buscando número...")
        self.update_idletasks()

        encontrado_matriz_A, tiempo_matriz_A = medir_tiempo(buscar_en_matriz, self.A, buscado)
        encontrado_arbol_A, tiempo_arbol_A = medir_tiempo(buscar_en_arbol, self.arbol_A, buscado)

        encontrado_matriz_A3, tiempo_matriz_A3 = medir_tiempo(buscar_en_matriz, self.A3, buscado)
        encontrado_arbol_A3, tiempo_arbol_A3 = medir_tiempo(buscar_en_arbol, self.arbol_A3, buscado)

        # Comparación simple de tiempos
        # (si empatan, se reporta como empate)
        if tiempo_matriz_A <= tiempo_arbol_A:
            mas_rapida_A = "Matriz A" if tiempo_matriz_A < tiempo_arbol_A else "Empate (Matriz A y Árbol A)"
        else:
            mas_rapida_A = "Árbol A"

        if tiempo_matriz_A3 <= tiempo_arbol_A3:
            mas_rapida_A3 = "Matriz A³" if tiempo_matriz_A3 < tiempo_arbol_A3 else "Empate (Matriz A³ y Árbol A³)"
        else:
            mas_rapida_A3 = "Árbol A³"

        mensaje = (
            "\n\nRESULTADOS DE BÚSQUEDA\n"
            "----------------------\n"
            f"Número buscado: {buscado}\n\n"
            "[A]\n"
            f"Matriz A: {'Sí' if encontrado_matriz_A else 'No'} - Tiempo: {tiempo_matriz_A} ns\n"
            f"Árbol A:  {'Sí' if encontrado_arbol_A else 'No'} - Tiempo: {tiempo_arbol_A} ns\n"
            f"Más rápida para A: {mas_rapida_A}\n\n"
            "[A³]\n"
            f"Matriz A³: {'Sí' if encontrado_matriz_A3 else 'No'} - Tiempo: {tiempo_matriz_A3} ns\n"
            f"Árbol A³:  {'Sí' if encontrado_arbol_A3 else 'No'} - Tiempo: {tiempo_arbol_A3} ns\n"
            f"Más rápida para A³: {mas_rapida_A3}\n"
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
        """Busca el ejecutable 'dot' de Graphviz.

        Busca en:
        1. PATH (usando shutil.which)
        2. Rutas comunes de instalación en Program Files

        Retorna la ruta completa a 'dot.exe' o None si no se encuentra.
        No modifica el sistema.
        """
        # 1. Buscar en PATH
        try:
            dot = shutil.which("dot")
            if dot and os.path.exists(dot):
                return dot
        except Exception:
            pass

        # 2. Rutas comunes de instalación en Windows
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        pfx86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        
        rutas_comunes = [
            os.path.join(pf, "Graphviz", "bin", "dot.exe"),
            os.path.join(pf, "Graphviz-15.0.0", "bin", "dot.exe"),
            os.path.join(pf, "Graphviz-15.0.0-win32", "bin", "dot.exe"),
            os.path.join(pfx86, "Graphviz", "bin", "dot.exe"),
        ]
        
        for ruta in rutas_comunes:
            if os.path.exists(ruta):
                return ruta

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
    app = App()
    app.mainloop()

