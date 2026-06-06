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

El proyecto está separado en dos partes:

```text
interfaz_grafica.py  -> Frontend / interfaz gráfica
Proyecto_final.py    -> Backend / lógica algorítmica
interfaz_grafica.py

Contiene la interfaz gráfica desarrollada con Tkinter.

Desde esta interfaz se puede:

Ingresar el tamaño n.
Generar la matriz A.
Calcular A³.
Ver el análisis de ambas matrices.
Buscar un número en matriz y árbol.
Abrir archivos .txt.
Abrir archivos .dot.
Ver las matrices en tabla si está instalada la librería opcional tksheet.

Proyecto_final.py

Contiene toda la lógica algorítmica del proyecto:

Generación de matriz.
Multiplicación de matrices.
Cálculo de A³.
Análisis de pares, impares, primos, perfectos y cuadrados perfectos.
Conteo de repeticiones.
Conversión de matriz a vector.
Ordenamiento.
Construcción de árbol binario equilibrado.
Búsqueda en matriz.
Búsqueda en árbol.
Medición de tiempos.
Exportación del árbol en formato DOT.
Requisitos del taller
1. Matriz A y cálculo de A³

El programa permite construir una matriz n x n, donde:

n >= 4

La matriz se llena aleatoriamente con números entre 0 y 9.

Luego se calcula:

A² = A × A
A³ = A² × A

La multiplicación de matrices está implementada manualmente, sin usar librerías matemáticas externas.

2. Análisis numérico

Para cada matriz generada se calcula:

Cantidad de números pares.
Cantidad de números impares.
Cantidad de números primos.
Cantidad de números perfectos.
Cantidad de números cuadrados perfectos.

El análisis se hace para:

Matriz A
Matriz A³
3. Vector unidimensional ordenado

Los elementos de cada matriz se pasan a un vector unidimensional.

Luego se ordenan de forma ascendente usando algoritmos propios:

Insertion Sort para vectores pequeños.
Merge Sort para vectores grandes.

No se usa sorted() ni .sort().

4. Conteo de repeticiones

El programa cuenta cuántas veces aparece cada número en:

Matriz A
Matriz A³
5. Árbol binario de búsqueda equilibrado

El programa construye árboles binarios de búsqueda equilibrados para:

Matriz A
Matriz A³

Luego permite buscar un mismo número en:

Matriz A
Árbol A
Matriz A³
Árbol A³

También mide los tiempos de ejecución y muestra cuál búsqueda fue más rápida.

## Tipo de árbol seleccionado

En este proyecto se usa un Árbol Binario de Búsqueda Equilibrado de Frecuencias. Se eligió este árbol porque permite representar los elementos de la matriz sin repetir nodos innecesariamente. Cada nodo almacena un diccionario JSON de la forma `{"valor": numero, "cantidad": frecuencia}`, donde `valor` corresponde al número encontrado en la matriz y `cantidad` indica cuántas veces aparece.

La comparación entre nodos se realiza usando únicamente el valor numérico almacenado en `"valor"`. Si el dato buscado es menor que este valor, la búsqueda continúa por el subárbol izquierdo. Si es mayor, continúa por el subárbol derecho. Si es igual, el dato fue encontrado y se retorna el diccionario con su frecuencia.

## Restricciones del sistema

- `n` debe ser mayor o igual a 4.
- `n` tiene un máximo definido en el programa (por ejemplo `MAX_N = 150`).
- El límite existe porque calcular `A³` requiere dos multiplicaciones de matrices.
- La multiplicación de matrices tiene costo `O(n³)`.
- La matriz `A`, `A²` y `A³` pueden consumir bastante memoria.
- Para matrices grandes se muestra una vista previa y se guardan archivos TXT.
- El árbol se construye con valores únicos y frecuencias para reducir nodos repetidos.
- El sistema mide memoria actual y memoria pico usando herramientas estándar de Python.

## Construcción del árbol binario equilibrado

Para construir el árbol binario de búsqueda equilibrado, primero se pasan los elementos de la matriz a un vector unidimensional. Luego el vector se ordena de forma ascendente usando algoritmos propios. Después se toma el elemento central como raíz del árbol. Los elementos de la mitad izquierda forman el subárbol izquierdo y los elementos de la mitad derecha forman el subárbol derecho. Este proceso se repite recursivamente hasta insertar todos los elementos.

Este procedimiento evita construir el árbol insertando los elementos en el orden original, ya que eso podría generar un árbol desbalanceado o similar a una lista. Al quedar equilibrado, la búsqueda depende de la altura del árbol y se acerca a O(log n), mientras que buscar directamente en la matriz requiere recorrer hasta n² elementos en el peor caso.

## Operaciones soportadas por el árbol

- Construcción del árbol equilibrado desde diccionarios JSON ordenados.
- Búsqueda de un valor y retorno del diccionario JSON con su frecuencia.
- Retorno de la cantidad de repeticiones.
- Recorrido inorden.
- Cálculo de altura.
- Conteo de nodos.
- Exportación a archivo DOT para visualización.

## Análisis de memoria

La memoria depende principalmente de:

- la matriz `A`,
- la matriz `A²` durante el cálculo,
- la matriz `A³`,
- los vectores generados,
- los diccionarios JSON de frecuencia,
- los nodos del árbol (cada uno almacena un diccionario).

El árbol de frecuencias usa menos nodos que un árbol con todos los elementos repetidos, porque si un número aparece muchas veces solo se crea un nodo y se almacena su cantidad en el diccionario `{"valor": numero, "cantidad": frecuencia}`.

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
| Construir árbol equilibrado desde vector ordenado | O(m), donde m = n² |
| Buscar en matriz | O(n²) |
| Buscar en árbol equilibrado | O(log m), donde m = n² |

Archivos generados

El programa crea automáticamente una carpeta llamada:

resultados/

Dentro de esta carpeta se generan archivos como:

matriz_A.txt
matriz_A3.txt
arbol_A.dot
arbol_A3.dot
Archivos .txt

Contienen las matrices completas.

Ejemplo:

resultados/matriz_A.txt
resultados/matriz_A3.txt

Estos archivos sirven especialmente cuando la matriz es grande y no conviene mostrarla completa dentro de la interfaz.

Archivos .dot

Contienen la representación del árbol en formato DOT.

Ejemplo:

resultados/arbol_A.dot
resultados/arbol_A3.dot

Estos archivos se pueden abrir con un visor de Graphviz para ver el árbol como gráfico.

Instalación y ejecución
1. Clonar el repositorio

git clone https://github.com/Proyecto-ADA-2026/main.git

Entrar a la carpeta:

cd main

2. Ejecutar el proyecto

python interfaz_grafica.py
Librerías usadas

El proyecto usa librerías estándar de Python:

tkinter
random
time
os

También puede usar opcionalmente:

tksheet

tksheet solo se usa para mostrar matrices como tabla en la interfaz.
No se usa para calcular, ordenar, buscar ni construir estructuras algorítmicas.

Instalación opcional de tksheet

Para usar los botones:

Ver tabla Matriz A
Ver tabla Matriz A³

instalar:

pip install tksheet

Si no se instala tksheet, el programa sigue funcionando, pero no se abrirá la vista tipo tabla.

Visualización de árboles con Graphviz

El programa exporta los árboles binarios en formato DOT:

- resultados/arbol_A.dot
- resultados/arbol_A3.dot

El archivo DOT es texto, por eso si se abre directamente se verá algo como:

```
digraph ArbolA { ... }
```

Para verlo como imagen se necesita Graphviz. Graphviz se usa únicamente para la parte gráfica/visual, no para construir el árbol ni para resolver algoritmos. La lógica del árbol sigue implementada manualmente en `Proyecto_final.py`.

Graphviz permite convertir:

- `resultados/arbol_A.dot` -> `resultados/arbol_A.png`
- `resultados/arbol_A3.dot` -> `resultados/arbol_A3.png`

Comando para verificar Graphviz:

```
dot -V
start resultados\arbol_A.png
```

Si `dot -V` no funciona, significa que Graphviz no está instalado o no está agregado al PATH.

Comando manual para generar una imagen:

```
dot -Tpng resultados/arbol_A.dot -o resultados/arbol_A.png
```

Comando para abrir la imagen en Windows:

```
start resultados\arbol_A.png
```

Graphviz no reemplaza ningún algoritmo del taller:

- No genera la matriz.
- No calcula A³.
- No construye el árbol.
- Solo dibuja el árbol ya generado por el programa.

Los árboles grandes no se grafican completos porque pueden tener demasiados nodos. Para ver el árbol visual se recomienda usar `n` pequeño, por ejemplo:

- n = 4
- n = 5
- n = 8

Los archivos PNG, DOT y TXT dentro de resultados son archivos generados por ejecución, por eso normalmente no se suben al repositorio.

Uso del programa
Ejecutar:
python interfaz_grafica.py
Ingresar el valor de n.

Ejemplos recomendados:

n = 4
n = 8
n = 20
n = 21
Presionar:
Generar matriz A y A³
El programa mostrará:
Matriz A.
Matriz A³.
Resumen de análisis.
Repeticiones.
Vectores ordenados.
Árboles, si el tamaño permite mostrarlos.
Archivos generados en resultados/.

Para buscar un número:
Escribir el número en el campo de búsqueda.
Presionar:
Buscar en matriz y árbol

El sistema buscará en:

Matriz A
Árbol A
Matriz A³
Árbol A³

y mostrará los tiempos de ejecución.

Botones de la interfaz
Generar matriz A y A³

Genera la matriz principal, calcula A³, analiza ambas matrices y construye los árboles.

Abrir TXT Matriz A

Abre:

resultados/matriz_A.txt

Abrir TXT Matriz A³

Abre:

resultados/matriz_A3.txt

Ver gráfico Árbol A

Abre:

resultados/arbol_A.dot

Ver gráfico Árbol A³

Abre:

resultados/arbol_A3.dot

Ver tabla Matriz A

Muestra la matriz A en una ventana tipo tabla si tksheet está instalado.

Ver tabla Matriz A³

Muestra la matriz A³ en una ventana tipo tabla si tksheet está instalado.

Matrices grandes

Cuando n > 20, el programa muestra una advertencia.

Para evitar que la interfaz se sature:

Se muestra una vista previa en pantalla.
Se guarda la matriz completa en .txt.
Se construye el árbol.
Se permite buscar en matriz y árbol.
No se dibuja el árbol completo si tiene demasiados nodos.

Esto no significa que el árbol no se construya.
El árbol sí se genera y se usa para la búsqueda.

Árboles grandes

Para matrices pequeñas, por ejemplo:

n = 4
n = 5
n = 8

el árbol puede visualizarse mejor.

Para matrices grandes, por ejemplo:

n = 20
n = 100
n = 200

el árbol contiene demasiados nodos, por eso no se muestra completo visualmente.

El programa evita dibujarlo completo para no congelar la interfaz.

Decisiones algorítmicas
Multiplicación de matrices

La multiplicación se implementa manualmente.

Para mejorar el rendimiento, se transpone la segunda matriz y así se recorren columnas como filas.

Ordenamiento

Se usa un enfoque híbrido:

Vectores pequeños -> Insertion Sort
Vectores grandes  -> Merge Sort

Merge Sort aplica la técnica de Divide y Vencerás.

Números perfectos

Se revisan divisores hasta la raíz cuadrada del número para evitar recorridos innecesarios.

Cuadrados perfectos

Se usa búsqueda binaria.

Caché

Durante el análisis numérico se usa caché para evitar recalcular propiedades de valores repetidos.

Restricciones respetadas

El proyecto no usa librerías externas para resolver la lógica algorítmica.

No se usa:

NumPy
pandas
collections.Counter
sorted()
list.sort()

Los algoritmos principales fueron implementados manualmente.

Recomendaciones para pruebas

Probar con:

n = 4
n = 8
n = 20
n = 21

Probar búsqueda con:

Un número que exista
Un número que no exista
Recomendación para sustentación

Se puede explicar así:

El proyecto se separó en dos capas. Proyecto_final.py contiene la lógica algorítmica del taller, mientras que interfaz_grafica.py contiene la interfaz gráfica. El sistema genera la matriz A, calcula A³, analiza ambas matrices, ordena sus elementos, cuenta repeticiones y construye árboles binarios equilibrados para comparar tiempos de búsqueda.

También se puede aclarar:

Para matrices grandes, el árbol sí se construye, pero no se dibuja completo porque visualmente sería demasiado grande. La búsqueda en el árbol sigue funcionando normalmente.
```

