import tkinter as tk
from tkinter import ttk, messagebox
import random
import time


# =========================================================
# LÓGICA
# =========================================================

def crear_matriz(n):
    matriz = []

    for _ in range(n):
        fila = []

        for _ in range(n):
            fila.append(random.randint(0, 9))

        matriz.append(fila)

    return matriz


def multiplicar_matrices(x, y):
    n = len(x)
    resultado = []

    for i in range(n):
        fila_resultado = []

        for j in range(n):
            suma = 0

            for k in range(n):
                suma = suma + x[i][k] * y[k][j]

            fila_resultado.append(suma)

        resultado.append(fila_resultado)

    return resultado


def calcular_A3(A):
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)
    return A3


def es_primo(numero):
    if numero < 2:
        return False

    divisor = 2

    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False

        divisor += 1

    return True


def es_perfecto(numero):
    if numero <= 0:
        return False

    suma_divisores = 0

    for divisor in range(1, numero):
        if numero % divisor == 0:
            suma_divisores += divisor

    return suma_divisores == numero


def es_cuadrado_perfecto(numero):
    if numero < 0:
        return False

    raiz = 0

    while raiz * raiz <= numero:
        if raiz * raiz == numero:
            return True

        raiz += 1

    return False


def analizar_matriz(matriz):
    pares = []
    impares = []
    primos = []
    perfectos = []
    cuadrados = []

    for fila in matriz:
        for valor in fila:
            if valor % 2 == 0:
                pares.append(valor)
            else:
                impares.append(valor)

            if es_primo(valor):
                primos.append(valor)

            if es_perfecto(valor):
                perfectos.append(valor)

            if es_cuadrado_perfecto(valor):
                cuadrados.append(valor)

    return {
        "pares": {"cantidad": len(pares), "valores": pares},
        "impares": {"cantidad": len(impares), "valores": impares},
        "primos": {"cantidad": len(primos), "valores": primos},
        "perfectos": {"cantidad": len(perfectos), "valores": perfectos},
        "cuadrados": {"cantidad": len(cuadrados), "valores": cuadrados},
    }


def contar_repeticiones(matriz):
    frecuencias = {}

    for fila in matriz:
        for valor in fila:
            frecuencias[valor] = frecuencias.get(valor, 0) + 1

    return frecuencias


def matriz_a_vector(matriz):
    vector = []

    for fila in matriz:
        for valor in fila:
            vector.append(valor)

    return vector


def insertion_sort_ascendente(vector):
    for i in range(1, len(vector)):
        actual = vector[i]
        j = i - 1

        while j >= 0 and vector[j] > actual:
            vector[j + 1] = vector[j]
            j -= 1

        vector[j + 1] = actual

    return vector


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


def construir_arbol_equilibrado(vector, inicio, fin):
    if inicio > fin:
        return None

    mitad = (inicio + fin) // 2

    raiz = Nodo(vector[mitad])
    raiz.izquierda = construir_arbol_equilibrado(vector, inicio, mitad - 1)
    raiz.derecha = construir_arbol_equilibrado(vector, mitad + 1, fin)

    return raiz


def buscar_en_arbol(raiz, buscado):
    if raiz is None:
        return False

    if buscado == raiz.valor:
        return True

    if buscado < raiz.valor:
        return buscar_en_arbol(raiz.izquierda, buscado)

    return buscar_en_arbol(raiz.derecha, buscado)


def buscar_en_matriz(matriz, buscado):
    for fila in matriz:
        for valor in fila:
            if valor == buscado:
                return True

    return False


def medir_tiempo(funcion, estructura, buscado):
    inicio = time.perf_counter_ns()
    encontrado = funcion(estructura, buscado)
    fin = time.perf_counter_ns()

    return encontrado, fin - inicio


# =========================================================
# DIBUJO DEL ÁRBOL EN TEXTO
# =========================================================

def arbol_a_ascii(raiz):
    if raiz is None:
        return "Árbol vacío"

    def display_aux(nodo):
        # Caso hoja
        if nodo.izquierda is None and nodo.derecha is None:
            linea = str(nodo.valor)
            ancho = len(linea)
            alto = 1
            centro = ancho // 2
            return [linea], ancho, alto, centro

        # Caso solo hijo izquierdo
        if nodo.derecha is None:
            lineas, ancho, alto, centro = display_aux(nodo.izquierda)
            valor = str(nodo.valor)
            ancho_valor = len(valor)

            primera = (
                " " * (centro + 1)
                + "_" * (ancho - centro - 1)
                + valor
            )

            segunda = (
                " " * centro
                + "/"
                + " " * (ancho - centro - 1 + ancho_valor)
            )

            lineas_movidas = [linea + " " * ancho_valor for linea in lineas]

            return (
                [primera, segunda] + lineas_movidas,
                ancho + ancho_valor,
                alto + 2,
                ancho + ancho_valor // 2
            )

        # Caso solo hijo derecho
        if nodo.izquierda is None:
            lineas, ancho, alto, centro = display_aux(nodo.derecha)
            valor = str(nodo.valor)
            ancho_valor = len(valor)

            primera = (
                valor
                + "_" * centro
                + " " * (ancho - centro)
            )

            segunda = (
                " " * (ancho_valor + centro)
                + "\\"
                + " " * (ancho - centro - 1)
            )

            lineas_movidas = [" " * ancho_valor + linea for linea in lineas]

            return (
                [primera, segunda] + lineas_movidas,
                ancho + ancho_valor,
                alto + 2,
                ancho_valor // 2
            )

        # Caso con dos hijos
        izquierda, ancho_izq, alto_izq, centro_izq = display_aux(nodo.izquierda)
        derecha, ancho_der, alto_der, centro_der = display_aux(nodo.derecha)

        valor = str(nodo.valor)
        ancho_valor = len(valor)

        primera = (
            " " * (centro_izq + 1)
            + "_" * (ancho_izq - centro_izq - 1)
            + valor
            + "_" * centro_der
            + " " * (ancho_der - centro_der)
        )

        segunda = (
            " " * centro_izq
            + "/"
            + " " * (ancho_izq - centro_izq - 1 + ancho_valor + centro_der)
            + "\\"
            + " " * (ancho_der - centro_der - 1)
        )

        if alto_izq < alto_der:
            izquierda += [" " * ancho_izq] * (alto_der - alto_izq)
        elif alto_der < alto_izq:
            derecha += [" " * ancho_der] * (alto_izq - alto_der)

        lineas = [primera, segunda]

        for linea_izq, linea_der in zip(izquierda, derecha):
            lineas.append(linea_izq + " " * ancho_valor + linea_der)

        return (
            lineas,
            ancho_izq + ancho_valor + ancho_der,
            max(alto_izq, alto_der) + 2,
            ancho_izq + ancho_valor // 2
        )

    lineas, _, _, _ = display_aux(raiz)

    if not lineas:
        return "Árbol vacío"

    ancho_maximo = max(len(linea) for linea in lineas)
    lineas_centradas = []

    for linea in lineas:
        lineas_centradas.append(linea.center(ancho_maximo + 8))

    return "\n".join(lineas_centradas)


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
            font=("Segoe UI", 18, "bold")
        )

        style.configure(
            "HeaderSub.TLabel",
            background="#1f4e79",
            foreground="#d9e8f5",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Card.TLabelframe",
            background="#ffffff",
            borderwidth=1,
            relief="solid"
        )

        style.configure(
            "Card.TLabelframe.Label",
            background="#f4f6f9",
            foreground="#1f4e79",
            font=("Segoe UI", 11, "bold")
        )

        style.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
        style.configure("TEntry", padding=6, font=("Segoe UI", 10))

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            background="#1f4e79",
            foreground="white"
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#173a5c")],
            foreground=[("active", "white")]
        )

        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 6)
        )

    def _build_ui(self):
        principal = ttk.Frame(self, style="Main.TFrame")
        principal.pack(fill="both", expand=True)

        # =====================================================
        # ENCABEZADO
        # =====================================================
        header = ttk.Frame(principal, style="Header.TFrame")
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Matriz A, A³ y Árbol Binario",
            style="Header.TLabel"
        ).pack(anchor="w", padx=20, pady=(14, 2))

        ttk.Label(
            header,
            text="Generación, análisis, ordenamiento y búsqueda comparativa",
            style="HeaderSub.TLabel"
        ).pack(anchor="w", padx=20, pady=(0, 14))

        # =====================================================
        # CONTROLES SUPERIORES
        # =====================================================
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
            command=self.generar
        )
        self.btn_generar.pack(side="left", padx=10)

        ttk.Label(
            top,
            text="Usa valores entre 4 y 12 para evitar que el programa se congele.",
            foreground="#666666"
        ).pack(side="left", padx=10)

        # =====================================================
        # BÚSQUEDA - COMO EN TU IMAGEN
        # =====================================================
        buscar_frame = tk.LabelFrame(
            principal,
            text="Búsqueda",
            bg="#f4f6f9",
            fg="#333333",
            font=("Segoe UI", 9)
        )
        buscar_frame.pack(fill="x", padx=20, pady=(0, 10))

        lbl_buscar = tk.Label(
            buscar_frame,
            text="Número a buscar:",
            bg="#f4f6f9",
            fg="#222222",
            font=("Segoe UI", 9)
        )
        lbl_buscar.pack(side="left", padx=(12, 5), pady=8)

        self.entry_buscado = tk.Entry(
            buscar_frame,
            width=10,
            font=("Segoe UI", 9),
            bg="white",
            fg="black",
            relief="solid",
            bd=1
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
            cursor="hand2"
        )
        self.btn_buscar.pack(side="left", padx=10)

        # =====================================================
        # CUERPO PRINCIPAL
        # =====================================================
        centro = ttk.Frame(principal, style="Main.TFrame")
        centro.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # ================= MATRICES =================
        left = ttk.LabelFrame(
            centro,
            text="Matrices generadas",
            style="Card.TLabelframe"
        )
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.notebook = ttk.Notebook(left)

        self.tab_A = ttk.Frame(self.notebook)
        self.tab_A3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_A, text="Matriz A")
        self.notebook.add(self.tab_A3, text="Matriz A³")

        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.text_A = self._crear_texto_scroll(self.tab_A)
        self.text_A3 = self._crear_texto_scroll(self.tab_A3)

        # ================= RESUMEN =================
        right = ttk.LabelFrame(
            centro,
            text="Resumen y análisis",
            style="Card.TLabelframe"
        )
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
            pady=10
        )

        scroll_result = ttk.Scrollbar(
            right,
            orient="vertical",
            command=self.txt_result.yview
        )

        self.txt_result.configure(yscrollcommand=scroll_result.set)

        self.txt_result.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0),
            pady=8
        )

        scroll_result.pack(
            side="right",
            fill="y",
            padx=(0, 8),
            pady=8
        )

        self.txt_result.insert(
            "1.0",
            "Aquí aparecerá el resumen del análisis.\n\nPrimero genera la matriz."
        )
        self.txt_result.config(state="disabled")

        # =====================================================
        # ÁRBOL
        # =====================================================
        arbol_frame = ttk.LabelFrame(
            principal,
            text="Árbol binario de búsqueda construido desde la matriz A",
            style="Card.TLabelframe"
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
            pady=10
        )

        scroll_arbol_y = ttk.Scrollbar(
            arbol_frame,
            orient="vertical",
            command=self.txt_arbol.yview
        )

        scroll_arbol_x = ttk.Scrollbar(
            arbol_frame,
            orient="horizontal",
            command=self.txt_arbol.xview
        )

        self.txt_arbol.configure(
            yscrollcommand=scroll_arbol_y.set,
            xscrollcommand=scroll_arbol_x.set
        )

        self.txt_arbol.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(8, 0),
            pady=(8, 0)
        )

        scroll_arbol_y.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 8),
            pady=(8, 0)
        )

        scroll_arbol_x.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(8, 0),
            pady=(0, 8)
        )

        arbol_frame.rowconfigure(0, weight=1)
        arbol_frame.columnconfigure(0, weight=1)

        self.txt_arbol.insert(
            "1.0",
            "Aquí se mostrará el árbol binario.\n\nEjemplo visual:\n\n      ___4___\n     /       \\\n   _2_       _7_\n  /   \\     /   \\\n 0     3   6     9"
        )
        self.txt_arbol.config(state="disabled")

        # =====================================================
        # ESTADO
        # =====================================================
        self.status = ttk.Label(
            principal,
            text="Estado: esperando datos...",
            anchor="w",
            background="#e8eef3",
            foreground="#333333",
            font=("Segoe UI", 10, "bold")
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
            pady=10
        )

        scroll_y = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=text.yview
        )

        scroll_x = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=text.xview
        )

        text.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

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

    def _mat_to_str(self, M):
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

        # Validación estricta del rango permitido.
        if n < 4 or n > 12:
            messagebox.showerror(
                "Error",
                "El valor de n debe estar estrictamente entre 4 y 12 para garantizar un tiempo de ejecución aceptable."
            )
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

            # Ordenar sin usar copias (mantener simplicidad académica).
            vector_A_asc = insertion_sort_ascendente(list(vector_A))
            vector_A3_asc = insertion_sort_ascendente(list(vector_A3))


            self.arbol_A = construir_arbol_equilibrado(
                vector_A_asc,
                0,
                len(vector_A_asc) - 1
            )

            self._set_text(self.text_A, self._mat_to_str(self.A))
            self._set_text(self.text_A3, self._mat_to_str(self.A3))

            ascii_arbol = arbol_a_ascii(self.arbol_A)
            self._set_text(self.txt_arbol, ascii_arbol)

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
            salida.append(
                ", ".join(f"{k}: {rep_A[k]}" for k in sorted(rep_A))
                if rep_A
                else "Sin datos"
            )

            salida.append("\n\n")
            salida.append(resumen_analisis("RESUMEN MATRIZ A³", analisis_A3))
            salida.append("\nRepeticiones A³:\n")
            salida.append(
                ", ".join(f"{k}: {rep_A3[k]}" for k in sorted(rep_A3))
                if rep_A3
                else "Sin datos"
            )

            salida.append("\n\nVECTORES ORDENADOS\n")
            salida.append("------------------\n")

            salida.append("A ascendente:\n")
            texto_A = str(vector_A_asc)
            salida.append(texto_A[:1200] + ("..." if len(texto_A) > 1200 else ""))

            salida.append("\n\nA³ ascendente:\n")
            texto_A3 = str(vector_A3_asc)
            salida.append(texto_A3[:1200] + ("..." if len(texto_A3) > 1200 else ""))

            self._set_text(self.txt_result, "".join(salida))

            self.status.config(
                text="Estado: matriz generada correctamente. Ya puedes buscar un número."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Ocurrió un problema al generar la matriz:\n{error}"
            )
            self.status.config(text="Estado: ocurrió un error al generar la matriz.")

    def buscar(self):
        if self.A is None or self.arbol_A is None:
            messagebox.showwarning(
                "Aviso",
                "Primero genera la matriz A y A³."
            )
            return

        try:
            buscado = int(self.entry_buscado.get().strip())
        except Exception:
            messagebox.showerror(
                "Error",
                "Ingrese un número entero para buscar."
            )
            return

        self.status.config(text="Estado: buscando número...")
        self.update_idletasks()

        encontrado_matriz, tiempo_matriz = medir_tiempo(
            buscar_en_matriz,
            self.A,
            buscado
        )

        encontrado_arbol, tiempo_arbol = medir_tiempo(
            buscar_en_arbol,
            self.arbol_A,
            buscado
        )

        mensaje = (
            "\n\nRESULTADOS DE BÚSQUEDA\n"
            "----------------------\n"
            f"Número buscado: {buscado}\n\n"
            f"En matriz A: {'Sí' if encontrado_matriz else 'No'}\n"
            f"Tiempo matriz: {tiempo_matriz} ns\n\n"
            f"En árbol binario: {'Sí' if encontrado_arbol else 'No'}\n"
            f"Tiempo árbol: {tiempo_arbol} ns\n"
        )

        self._append_text(self.txt_result, mensaje)

        self.status.config(text="Estado: búsqueda completada.")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()