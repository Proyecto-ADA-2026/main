# Proyecto Final ADA - Version por Consola

Esta rama `consola-sin-memoria` es una version alternativa del proyecto para ejecutar todo desde terminal, sin interfaz grafica, sin medicion de memoria y sin generar archivos externos.

## Ejecucion

```bash
python main_consola.py
```

El programa solicita el valor de `n` por consola y valida que:

- `n >= 4`
- `n <= MAX_N`

`MAX_N` esta definido en `proyecto_final.py`.

## Funcionalidades

- Crear matriz `A` de tamano `n x n` con numeros aleatorios entre `0` y `9`.
- Mostrar la matriz original `A`.
- Calcular y mostrar `A2 = A x A`.
- Calcular y mostrar `A3 = A2 x A`.
- Analizar pares, impares, primos, perfectos y cuadrados perfectos.
- Contar repeticiones.
- Ordenar vectores en forma ascendente y descendente.
- Construir arboles binarios de busqueda equilibrados para `A` y `A3`.
- Mostrar el arbol en texto cuando el numero de nodos es manejable.
- Comparar busqueda secuencial en matriz contra busqueda en arbol.
- Mostrar tiempos promedio de busqueda en nanosegundos.

## Cambios frente a la version principal

- La interfaz grafica esta desactivada.
- No se usa Tkinter.
- No se usa `os.startfile`.
- No se usa medicion de memoria.
- No se usa `tracemalloc`.
- No se crean archivos `.txt`.
- No se crean archivos `.json`.
- No se guardan resultados en la carpeta `resultados`.
- Todos los resultados se muestran directamente en consola.

## Archivos principales de esta rama

```text
main_consola.py     -> Punto de entrada por consola
proyecto_final.py   -> Backend con algoritmos y estructuras
README.md           -> Documentacion de esta rama
```

`interfaz_grafica.py` queda como aviso de compatibilidad: si se ejecuta, informa que la interfaz esta desactivada y que se debe usar `main_consola.py`.

## Justificacion algoritmica

El calculo de `A3` se realiza en dos multiplicaciones:

```text
A2 = A x A
A3 = A2 x A
```

Cada multiplicacion de matrices cuadradas cuesta `O(n3)`. El costo real aproximado de calcular `A3` es `2 * O(n3)`, que asintoticamente se expresa como `O(n3)`.

Generar y mostrar una matriz cuesta `O(n2)`. Analizar pares, impares, primos, perfectos y cuadrados perfectos tambien recorre los `n2` elementos. La busqueda secuencial en matriz cuesta `O(n2)`.

El arbol binario de busqueda se construye con valores unicos y frecuencias. La busqueda en el arbol equilibrado cuesta aproximadamente `O(log u)`, donde `u` es la cantidad de valores unicos.

## Comandos Git sugeridos

Para crear esta rama desde `main`:

```bash
git checkout main
git pull origin main
git checkout -b consola-sin-memoria
```

Para guardar y subir la rama:

```bash
git add .
git commit -m "Crear version por consola sin medicion de memoria"
git push origin consola-sin-memoria
```
