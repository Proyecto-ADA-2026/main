"""Mediciones separadas de memoria para backend, frontend y programa completo.

Este archivo usa psutil para consultar la memoria residente total del proceso
de Python. Es una herramienta de medicion para el informe, no participa en los
algoritmos principales del proyecto.
"""

import gc
import os
import sys
import time

try:
    import psutil
except ImportError:
    psutil = None

from proyecto_final import (
    crear_matriz,
    multiplicar_matrices,
    analizar_matriz,
    contar_repeticiones,
    frecuencias_a_json_ordenado,
    matriz_a_vector,
    ordenar_ascendente,
    invertir_vector,
    construir_arbol_json_equilibrado,
)


def obtener_rss_bytes():
    """Retorna la memoria residente total del proceso actual."""
    if psutil is None:
        raise RuntimeError("Instala psutil con: pip install psutil")

    proceso = psutil.Process(os.getpid())
    return proceso.memory_info().rss


def convertir_memoria(bytes_valor):
    """Convierte bytes a bytes, KB y MB."""
    kb = bytes_valor / 1024
    mb = kb / 1024
    return bytes_valor, kb, mb


def imprimir_medicion(nombre, inicial, final):
    """Imprime memoria inicial, final y diferencia aproximada."""
    diferencia = final - inicial
    b, kb, mb = convertir_memoria(diferencia)

    print("\n" + nombre)
    print("-" * len(nombre))
    print(f"Memoria inicial : {inicial / 1024 / 1024:.4f} MB")
    print(f"Memoria final   : {final / 1024 / 1024:.4f} MB")
    print(f"Consumo aprox.  : {b} bytes | {kb:.2f} KB | {mb:.4f} MB")


def medir_backend(n):
    """Mide estructuras y operaciones principales del backend."""
    gc.collect()
    memoria_inicial = obtener_rss_bytes()

    A = crear_matriz(n)
    A2 = multiplicar_matrices(A, A)
    A3 = multiplicar_matrices(A2, A)

    analisis_A = analizar_matriz(A)
    analisis_A3 = analizar_matriz(A3)

    frecuencias_A = contar_repeticiones(A)
    frecuencias_A3 = contar_repeticiones(A3)

    lista_A = frecuencias_a_json_ordenado(frecuencias_A)
    lista_A3 = frecuencias_a_json_ordenado(frecuencias_A3)

    arbol_A = construir_arbol_json_equilibrado(lista_A, 0, len(lista_A) - 1)
    arbol_A3 = construir_arbol_json_equilibrado(lista_A3, 0, len(lista_A3) - 1)

    vector_A = ordenar_ascendente(matriz_a_vector(A))
    vector_A3 = ordenar_ascendente(matriz_a_vector(A3))

    vector_A_desc = invertir_vector(vector_A)
    vector_A3_desc = invertir_vector(vector_A3)

    estructuras = (
        A, A2, A3,
        analisis_A, analisis_A3,
        frecuencias_A, frecuencias_A3,
        lista_A, lista_A3,
        arbol_A, arbol_A3,
        vector_A, vector_A3,
        vector_A_desc, vector_A3_desc,
    )

    memoria_final = obtener_rss_bytes()
    imprimir_medicion(f"BACKEND CON n = {n}", memoria_inicial, memoria_final)

    return estructuras


def medir_frontend():
    """Mide la interfaz creada, sin generar matrices."""
    from interfaz_grafica import App

    gc.collect()
    memoria_inicial = obtener_rss_bytes()

    app = App()
    app.update_idletasks()
    app.update()

    time.sleep(1)

    memoria_final = obtener_rss_bytes()
    imprimir_medicion("FRONTEND SIN DATOS", memoria_inicial, memoria_final)

    app.destroy()


def medir_programa_completo(n):
    """Mide la interfaz y luego ejecuta la generacion completa desde la GUI."""
    import tkinter.messagebox as messagebox
    import interfaz_grafica
    from interfaz_grafica import App

    if n > interfaz_grafica.MAX_N:
        print(
            "La interfaz tiene MAX_N = " + str(interfaz_grafica.MAX_N) +
            ". Para medir el programa completo usa n <= " +
            str(interfaz_grafica.MAX_N) + "."
        )
        return

    gc.collect()
    memoria_inicial = obtener_rss_bytes()

    askyesno_original = messagebox.askyesno
    messagebox.askyesno = lambda *args, **kwargs: True

    try:
        app = App()
        app.update_idletasks()

        app.entry_n.delete(0, "end")
        app.entry_n.insert(0, str(n))

        app.generar()
        app.update_idletasks()
        app.update()

        time.sleep(1)

        memoria_final = obtener_rss_bytes()
        imprimir_medicion(
            f"PROGRAMA COMPLETO CON n = {n}",
            memoria_inicial,
            memoria_final,
        )
    finally:
        messagebox.askyesno = askyesno_original
        try:
            app.destroy()
        except Exception:
            pass


def main():
    """Ejecuta una medicion segun los argumentos de consola."""
    if len(sys.argv) < 2:
        print("Uso:")
        print("python medir_memoria_componentes.py backend 50")
        print("python medir_memoria_componentes.py frontend")
        print("python medir_memoria_componentes.py completo 50")
        return

    tipo = sys.argv[1].lower()

    try:
        if tipo == "backend":
            if len(sys.argv) < 3:
                print("Falta n. Ejemplo: python medir_memoria_componentes.py backend 50")
                return
            n = int(sys.argv[2])
            medir_backend(n)
        elif tipo == "frontend":
            medir_frontend()
        elif tipo == "completo":
            if len(sys.argv) < 3:
                print("Falta n. Ejemplo: python medir_memoria_componentes.py completo 50")
                return
            n = int(sys.argv[2])
            medir_programa_completo(n)
        else:
            print("Tipo de prueba no valido.")
    except RuntimeError as error:
        print(error)


if __name__ == "__main__":
    main()
