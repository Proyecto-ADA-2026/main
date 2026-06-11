# Proyecto Final ADA - Rama sin memoria ni TXT

Esta rama `consola-sin-memoria-sin-txt` mantiene la ejecucion desde la interfaz grafica, pero elimina la medicion de memoria y la generacion de archivos `.txt`.

## Ejecucion

```bash
python interfaz_grafica.py
```

## Que conserva esta rama

- Interfaz grafica con Tkinter.
- Generacion de matriz `A`.
- Calculo de `A2 = A x A`.
- Calculo de `A3 = A2 x A`.
- Analisis de pares, impares, primos, perfectos y cuadrados perfectos.
- Conteo de repeticiones.
- Vectores ordenados.
- Arboles binarios de busqueda equilibrados.
- Visualizacion del arbol desde la interfaz.
- Panel ASCII del arbol.
- Busqueda comparativa en matriz y arbol.

## Que se desactivo en esta rama

- Medicion de memoria.
- `tracemalloc`.
- `medicion_memoria.py`.
- Reportes de memoria en el resumen.
- Generacion de archivos `.txt`.
- Botones para abrir TXT.
- Funciones de guardado de matrices en TXT.

## Archivos principales

```text
proyecto_final.py    -> Backend principal / logica algoritmica
interfaz_grafica.py  -> Interfaz grafica de ejecucion
gestor_txt.py        -> Guardado y apertura de JSON de arboles
README.md            -> Documentacion de esta rama
```

## Archivos generados

Esta rama no genera matrices en `.txt`. La matriz `A` y la matriz `A3` se muestran en pantalla. Para arboles, se conserva el guardado JSON:

```text
resultados/arbol_A.json
resultados/arbol_A3.json
```

## Justificacion

La rama sirve como alternativa academica para ejecutar el proyecto desde la interfaz grafica sin incluir mediciones de memoria ni archivos `.txt`. La logica principal de matrices, analisis, ordenamiento, arboles y busqueda se conserva.

El calculo de `A3` se realiza con dos multiplicaciones:

```text
A2 = A x A
A3 = A2 x A
```

Por eso el limite `MAX_N = 50` se mantiene en `proyecto_final.py`.
