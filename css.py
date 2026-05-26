from rich.console import Console
from rich.table import Table
from rich.tree import Tree

console = Console(width=120)


class Color:
    CYAN = "cyan"
    VERDE = "green"
    AMARILLO = "yellow"
    MAGENTA = "magenta"


def activar_colores():
    # Rich activa los colores automaticamente si la terminal los soporta.
    return None


def titulo(texto, color=Color.CYAN, ancho=45):
    print()
    console.print(f"[{color}]{texto.center(ancho)}[/{color}]")


def mostrar_matriz_bonita(matriz):
    tabla = Table(show_header=False)

    for i in range(len(matriz[0])):
        tabla.add_column()

    for fila in matriz:
        tabla.add_row(*[str(valor) for valor in fila])

    console.print(tabla)


def mostrar_vector_bonito(vector):
    console.print("[cyan][" + ", ".join(str(valor) for valor in vector) + "][/cyan]")


def mostrar_analisis_bonito(analisis=None):
    if analisis is None:
        return

    if isinstance(analisis, dict):
        for clave, datos in analisis.items():
            if isinstance(datos, dict):
                cantidad = datos["cantidad"]
                valores = datos["valores"]
                lista = ", ".join(str(valor) for valor in valores)
                if lista == "":
                    lista = "ninguno"

                console.print(f"[bold]{clave}:[/bold] {cantidad}")
                console.print("  [" + lista + "]", style="cyan", markup=False)
            else:
                console.print(f"{clave}: {datos}")


def mostrar_repeticiones_bonitas(frecuencias):
    for valor in sorted(frecuencias):
        console.print(f"{valor} aparece {frecuencias[valor]} veces")


def mostrar_arbol_bonito(raiz):
    if raiz is None:
        console.print("[red]Arbol vacio[/red]")
        return

    def inorden(nodo, valores):
        if nodo is not None:
            inorden(nodo.izquierda, valores)
            valores.append(nodo.valor)
            inorden(nodo.derecha, valores)

    def crear_rama(nodo, etiqueta="Raiz"):
        color = "cyan"
        if etiqueta == "Izq":
            color = "green"
        elif etiqueta == "Der":
            color = "orange3"

        rama = Tree(
            f"[{color}]{etiqueta}[/{color}] [bold blue]({nodo.valor})[/bold blue]",
            guide_style="bright_blue"
        )

        if nodo.izquierda is not None:
            rama.add(crear_rama(nodo.izquierda, "Izq"))

        if nodo.derecha is not None:
            rama.add(crear_rama(nodo.derecha, "Der"))

        return rama

    console.print(crear_rama(raiz))

    valores = []
    inorden(raiz, valores)
    recorrido = ", ".join(str(valor) for valor in valores)
    console.print("[bold blue]Recorrido Inorden ordenado:[/bold blue]")
    console.print("[" + recorrido + "]", style="green", markup=False)


def mostrar_resultados_busqueda(
    encontrado_matriz,
    tiempo_matriz,
    encontrado_arbol,
    tiempo_arbol
):
    print()
    console.print("[magenta]RESULTADOS DE BUSQUEDA[/magenta]")

    if encontrado_matriz:
        print("Encontrado en matriz: Si")
    else:
        print("Encontrado en matriz: No")

    print("Tiempo matriz:", tiempo_matriz, "ns")

    if encontrado_arbol:
        print("Encontrado en arbol: Si")
    else:
        print("Encontrado en arbol: No")

    print("Tiempo arbol:", tiempo_arbol, "ns")
