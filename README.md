# Proyecto Final ADA - Matriz A, A³ y Árbol Binario

Este proyecto corresponde al taller final de Análisis y Diseño de Algoritmos.

El sistema permite generar una matriz `n x n` con números aleatorios entre `0` y `9`, calcular la matriz `A³`, analizar sus valores, ordenar sus elementos, contar repeticiones y construir árboles binarios de búsqueda equilibrados para comparar tiempos de búsqueda.

---

## Integrantes

- Luz Amelia Ibarguen
- Katherine Lopez Unas
- Diego Unas

---

## Estructura del proyecto

```text
proyecto_final.py    -> Backend principal / lógica algorítmica
interfaz_grafica.py  -> Frontend / interfaz gráfica
gestor_txt.py        -> Generación de texto y guardado de archivos
medicion_memoria.py  -> Estimación detallada y medición real de memoria
README.md            -> Documentación del proyecto
```

### `proyecto_final.py`

Contiene la lógica algorítmica principal:

- Generación de la matriz `A`.
- Multiplicación manual de matrices.
- Cálculo de `A³`.
- Análisis de pares, impares, primos, perfectos y cuadrados perfectos.
- Conteo de repeticiones.
- Conversión de matriz a vector.
- Ordenamiento ascendente y descendente con algoritmos propios.
- Construcción de árboles binarios de búsqueda equilibrados.
- Búsqueda en matriz y en árbol.
- Medición de tiempos y memoria.
- Generación de una representación ASCII del árbol para la interfaz.

### `interfaz_grafica.py`

Contiene la interfaz gráfica desarrollada con Tkinter. Desde la interfaz se puede:

- Ingresar el tamaño `n`.
- Generar la matriz `A`.
- Calcular `A³`.
- Ver el análisis de ambas matrices.
- Buscar un número en matriz y árbol.
- Abrir los archivos `.txt` de matrices.
- Abrir los archivos `.json` de árboles.
- Ver la visualización del árbol desde la interfaz gráfica.

El proyecto se ejecuta con:

```bash
python interfaz_grafica.py
```

### `gestor_txt.py`

Contiene los helpers para generar texto legible y guardar archivos en la carpeta `resultados/`.

Este módulo guarda:

- matrices en archivos `.txt`,
- árboles en archivos `.json`.

### `medicion_memoria.py`

Contiene las funciones de medición y estimación de memoria:

- estimación profunda por estructura con `sys.getsizeof`,
- conversión de bytes a KB y MB,
- reporte detallado de memoria para la interfaz,
- medición real de memoria actual y pico con `tracemalloc`.

---

## Requisitos del taller

### 1. Matriz A y cálculo de A³

El programa permite construir una matriz `n x n`, donde `n >= 4`.

La matriz se llena aleatoriamente con números entre `0` y `9`.

Luego se calcula:

```text
A² = A × A
A³ = A² × A
```

La multiplicación de matrices está implementada manualmente, sin librerías matemáticas externas.

### 2. Análisis numérico

Para cada matriz generada se calcula:

- cantidad de números pares,
- cantidad de números impares,
- cantidad de números primos,
- cantidad de números perfectos,
- cantidad de números cuadrados perfectos.

El análisis se hace para la matriz `A` y para la matriz `A³`.

### 3. Vector unidimensional ordenado

Los elementos de cada matriz se pasan a un vector unidimensional y luego se ordenan de forma ascendente usando algoritmos propios:

- Insertion Sort para vectores pequeños.
- Merge Sort para vectores grandes.

No se usa `sorted()` ni `.sort()`.

### 4. Conteo de repeticiones

El programa cuenta cuántas veces aparece cada número en:

- matriz `A`,
- matriz `A³`.

### 5. Árbol binario de búsqueda equilibrado

El programa construye árboles binarios de búsqueda equilibrados para:

- matriz `A`,
- matriz `A³`.

Luego permite buscar un mismo número en:

- matriz `A`,
- árbol `A`,
- matriz `A³`,
- árbol `A³`.

También mide los tiempos de ejecución y muestra cuál búsqueda fue más rápida.

---

## Justificación algorítmica

El cálculo de `A³` se realiza en dos pasos:

```text
A² = A × A
A³ = A² × A
```

Por lo tanto, calcular `A³` implica dos multiplicaciones de matrices. Cada multiplicación de matrices cuadradas tiene costo `O(n³)`, así que el costo real aproximado del cálculo completo es `2·O(n³)`. En análisis asintótico se eliminan las constantes, por eso se expresa como `O(n³)`.

La generación de la matriz `A` recorre sus `n²` posiciones, por eso cuesta `O(n²)`. Mostrar una matriz completa también cuesta `O(n²)`; por esa razón, cuando `n > 20`, la interfaz muestra una vista previa y guarda los archivos completos en `resultados/`.

El análisis de pares, impares, primos, perfectos y cuadrados perfectos también recorre los `n²` elementos de cada matriz. La búsqueda secuencial en matriz puede recorrer todas las posiciones, así que su costo es `O(n²)`.

La búsqueda en el árbol equilibrado depende de la altura del árbol. Como el árbol se construye con valores únicos y queda balanceado, su costo aproximado es `O(log u)`, donde `u` es la cantidad de valores únicos almacenados.

---

## Tipo de árbol seleccionado

En este proyecto se usa un Árbol Binario de Búsqueda Equilibrado de Frecuencias. Cada nodo almacena un diccionario JSON de la forma:

```json
{"valor": 5, "cantidad": 3}
```

`valor` corresponde al número encontrado en la matriz y `cantidad` indica cuántas veces aparece.

El árbol no guarda un nodo por cada celda de la matriz. Guarda un nodo por cada valor único encontrado, y ese nodo conserva dos datos: el `valor` y la `cantidad` de apariciones. No se pierde información porque la suma de las cantidades de todos los nodos debe ser igual a `n²`.

Por ejemplo, si la matriz tiene 16 posiciones, el árbol puede tener menos de 16 nodos porque agrupa valores repetidos. Aun así, la suma de sus frecuencias debe seguir dando 16. Esto reduce nodos repetidos y permite comparar la búsqueda secuencial en matriz contra la búsqueda en árbol.

La comparación entre nodos se realiza usando únicamente el valor numérico almacenado en `"valor"`. Si el dato buscado es menor, la búsqueda continúa por el subárbol izquierdo. Si es mayor, continúa por el subárbol derecho. Si es igual, el dato fue encontrado y se retorna el diccionario con su frecuencia.

---

## Restricciones del sistema

- `n` debe ser mayor o igual a 4.
- `n` tiene un máximo definido en el programa: `MAX_N = 50`.
- El cálculo de `A³` requiere dos multiplicaciones de matrices.
- La multiplicación de matrices tiene costo `O(n³)`.
- La matriz `A`, `A²` y `A³` pueden consumir bastante memoria.
- Para matrices grandes se muestra una vista previa y se guardan archivos `.txt`.
- El árbol se construye con valores únicos y frecuencias para reducir nodos repetidos.
- El sistema mide memoria actual y memoria pico usando herramientas estándar de Python.

---

## Ubicación del límite máximo de n

El límite máximo `MAX_N` está definido en `proyecto_final.py`, porque corresponde a una restricción algorítmica del backend y no a una regla visual de la interfaz. La interfaz `interfaz_grafica.py` importa `MAX_N` desde el backend y solo lo consulta para validar la entrada del usuario.

Esta decisión evita duplicar valores entre archivos y separa correctamente la lógica algorítmica de la interfaz gráfica. El límite existe porque calcular `A³` implica dos multiplicaciones de matrices (`A² = A × A` y luego `A³ = A² × A`), lo que tiene costo cúbico y puede consumir mucho tiempo y memoria.

---

## Construcción del árbol binario equilibrado

Para construir el árbol binario de búsqueda equilibrado, primero se obtiene la frecuencia de cada valor de la matriz. Luego esas frecuencias se convierten a una lista de diccionarios JSON ordenada por valor.

Después se toma el elemento central como raíz del árbol. Los elementos de la mitad izquierda forman el subárbol izquierdo y los elementos de la mitad derecha forman el subárbol derecho. Este proceso se repite recursivamente hasta insertar todos los valores únicos.

Al quedar equilibrado, la búsqueda depende de la altura del árbol y se acerca a `O(log u)`, donde `u` es la cantidad de valores únicos. Buscar directamente en la matriz requiere recorrer hasta `n²` elementos en el peor caso, por eso tiene costo `O(n²)`.

---

## Operaciones soportadas por el árbol

- Construcción del árbol equilibrado desde diccionarios JSON ordenados.
- Búsqueda de un valor y retorno del diccionario JSON con su frecuencia.
- Retorno de la cantidad de repeticiones.
- Recorrido inorden.
- Cálculo de altura.
- Conteo de nodos.
- Visualización del árbol desde la interfaz gráfica.
- Guardado del árbol en archivo `.json`.

---

## Análisis de memoria

La memoria se presenta con dos mediciones:

- una estimación detallada por estructura,
- una medición real del programa con `tracemalloc`.

La función anterior solo estimaba la matriz `A`. Para un análisis más completo, se implementó una medición que considera las principales estructuras generadas durante la ejecución:

- la matriz `A`,
- la matriz `A²` durante el cálculo,
- la matriz `A³`,
- los vectores generados,
- los diccionarios JSON de frecuencia,
- los nodos del árbol.

La medición detallada está separada en `medicion_memoria.py` para mantener el backend algorítmico enfocado en matrices, búsquedas, ordenamientos y árboles.

El árbol de frecuencias usa menos nodos que un árbol con todos los elementos repetidos, porque si un número aparece muchas veces solo se crea un nodo y se almacena su cantidad.

---

## Análisis de costos principales

| Operación | Costo |
|---|---|
| Generar matriz A | O(n²) |
| Mostrar matriz A | O(n²) |
| Multiplicar dos matrices | O(n³) |
| Calcular A³ | O(n³) |
| Analizar pares, impares, primos, perfectos y cuadrados perfectos | O(n²) |
| Pasar matriz a vector | O(n²) |
| Ordenar vector con insertion sort | O(m²), donde m = n² |
| Ordenar vector con merge sort | O(m log m), donde m = n² |
| Contar repeticiones | O(n²) |
| Construir árbol equilibrado desde valores únicos | O(u), donde u = valores únicos |
| Buscar en matriz | O(n²) |
| Buscar en árbol equilibrado de frecuencias | O(log u), donde u = valores únicos |

---

## Archivos generados

El programa crea automáticamente una carpeta llamada:

```text
resultados/
```

Dentro de esta carpeta se generan:

```text
matriz_A.txt
matriz_A3.txt
arbol_A.json
arbol_A3.json
```

### Archivos `.txt`

Contienen las matrices completas:

```text
resultados/matriz_A.txt
resultados/matriz_A3.txt
```

Estos archivos sirven especialmente cuando la matriz es grande y no conviene mostrarla completa dentro de la interfaz.

### Archivos `.json`

Contienen la estructura de los árboles binarios de búsqueda equilibrados:

```text
resultados/arbol_A.json
resultados/arbol_A3.json
```

Cada archivo incluye el nombre del árbol, una descripción y la estructura con `valor`, `cantidad`, `izquierda` y `derecha`.

---

## Instalación y ejecución

Clonar el repositorio:

```bash
git clone https://github.com/Proyecto-ADA-2026/main.git
```

Entrar a la carpeta:

```bash
cd main
```

Ejecutar el proyecto:

```bash
python interfaz_grafica.py
```

## Restricción de sistema operativo

El proyecto está pensado para ejecutarse en Windows. La interfaz usa Tkinter para la ventana principal y `os.startfile` para abrir automáticamente los archivos generados desde la carpeta `resultados/`.

Si la apertura automática no funciona, los archivos pueden abrirse manualmente desde:

```text
resultados/
```

Esta decisión no afecta la lógica algorítmica del proyecto; solo corresponde a la forma de abrir archivos desde la interfaz.

El proyecto usa librerías estándar de Python:

- `tkinter`
- `random`
- `time`
- `os`
- `sys`
- `tracemalloc`

---

## Uso del programa

1. Ejecutar `python interfaz_grafica.py`.
2. Ingresar el valor de `n`.
3. Presionar `Generar matriz A y A³`.
4. Revisar las matrices, el resumen, las repeticiones, los vectores ordenados y los árboles.
5. Usar el campo de búsqueda para comparar búsqueda en matriz y en árbol.

Ejemplos recomendados:

- `n = 4`
- `n = 8`
- `n = 20`
- `n = 21`

---

## Botones de la interfaz

- `Generar matriz A y A³`: genera la matriz principal, calcula `A³`, analiza ambas matrices y construye los árboles.
- `Abrir TXT A`: abre `resultados/matriz_A.txt`.
- `Abrir TXT A3`: abre `resultados/matriz_A3.txt`.
- `Ver JSON Arbol A`: abre `resultados/arbol_A.json`.
- `Ver JSON Arbol A3`: abre `resultados/arbol_A3.json`.
- `Ver Arbol A`: abre la visualización del árbol `A` desde la interfaz.
- `Ver Arbol A3`: abre la visualización del árbol `A³` desde la interfaz.
- `Buscar en matriz y arbol`: busca el número ingresado en las matrices y en los árboles.

---

## Matrices grandes

Cuando `20 < n <= 50`, el programa muestra una advertencia. Para evitar que la interfaz se sature:

- se muestra una vista previa en pantalla,
- se guarda la matriz completa en `.txt`,
- se construye el árbol,
- se guarda el árbol en `.json`,
- se permite buscar en matriz y árbol.

Esto no significa que el árbol no se construya. El árbol sí se genera y se usa para la búsqueda.

---

## Árboles grandes

Para matrices pequeñas, por ejemplo `n = 4`, `n = 5` o `n = 8`, el árbol puede visualizarse mejor.

Para matrices grandes, el árbol contiene demasiados nodos, por eso la visualización puede ser menos cómoda. La búsqueda en el árbol sigue funcionando normalmente.

---

## Decisiones algorítmicas

### Multiplicación de matrices

La multiplicación se implementa manualmente. Para mejorar el rendimiento, se transpone la segunda matriz y así se recorren columnas como filas.

### Ordenamiento

Se usa un enfoque híbrido:

- vectores pequeños: Insertion Sort,
- vectores grandes: Merge Sort.

Merge Sort aplica la técnica de Divide y Vencerás.

### Números perfectos

Se revisan divisores hasta la raíz cuadrada del número para evitar recorridos innecesarios.

### Cuadrados perfectos

Se usa búsqueda binaria.

### Caché

Durante el análisis numérico se usa caché para evitar recalcular propiedades de valores repetidos.

---

## Restricciones respetadas

El proyecto no usa librerías externas para resolver la lógica algorítmica.

No se usa:

- NumPy
- pandas
- `collections.Counter`
- `sorted()`
- `list.sort()`

Los algoritmos principales fueron implementados manualmente.

---

## Validación operativa sugerida

Validar la ejecución principal con:

- `n = 4`
- `n = 8`
- `n = 20`
- `n = 21`

Validar la búsqueda con:

- un número que exista,
- un número que no exista.

---

## Evidencias recomendadas para la entrega

Antes de entregar, se recomienda anexar capturas de:

- ejecución con `n = 4`,
- matriz `A` generada,
- matriz `A³` generada,
- resumen de análisis,
- árbol `A`,
- árbol `A³`,
- búsqueda comparativa en matriz y árbol,
- archivos `.txt` y `.json` generados en la carpeta `resultados`.

---

## Recomendación

El proyecto se separó en partes claras. `proyecto_final.py` contiene la lógica algorítmica del taller, `interfaz_grafica.py` contiene la interfaz gráfica, `gestor_txt.py` maneja la generación de texto y el guardado de archivos, y `medicion_memoria.py` concentra la estimación y medición de memoria. El sistema genera la matriz `A`, calcula `A³`, analiza ambas matrices, ordena sus elementos, cuenta repeticiones y construye árboles binarios equilibrados para comparar tiempos de búsqueda.

Para matrices grandes, el árbol sí se construye, pero no siempre es cómodo visualizarlo completo. La búsqueda en el árbol sigue funcionando normalmente, y su estructura queda guardada en archivos `.json`.
