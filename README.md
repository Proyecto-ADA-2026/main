# Proyecto Final ADA - Matriz A, A³ y Árbol Binario

Este proyecto corresponde al taller final de Análisis y Diseño de Algoritmos.  
El sistema permite generar una matriz `n x n` con valores aleatorios entre `0` y `9`, calcular la matriz `A³`, analizar sus valores, ordenar sus elementos, contar repeticiones y construir árboles binarios de búsqueda equilibrados para comparar tiempos de búsqueda.

---

## Integrantes

- Luz Amelia Ibarguen
- Katherine Lopez Unas 
- Diego Unas

---

## Descripción general

El proyecto está dividido en dos partes principales:

```text
interfaz_grafica.py  -> Frontend / interfaz gráfica
Proyecto_final.py    -> Backend / lógica algorítmica
```





---

## Graphviz (para ver los árboles)
La interfaz gráfica genera imágenes a partir de archivos **.dot** usando Graphviz (comando `dot`).



### 1) Verificación en Windows
En una terminal, ejecuta:
```bash
dot -V
```

- Si el comando **funciona**, Graphviz está instalado y el ejecutable `dot` está disponible en el **PATH**.
- Si **no funciona**, puede ser porque:
  - Graphviz **no está instalado**, o
  - `dot` **no está agregado al PATH**.

### 2) Instalar Graphviz y agregarlo al PATH
1. Instala Graphviz (descarga e instalación para Windows desde la página oficial de Graphviz).
2. Busca la carpeta `bin` donde se instala `dot` (típicamente algo como `C:\Program Files\Graphviz\bin`).
3. Agrega esa ruta al **PATH**:
   - Panel de control / Configuración del sistema → Variables de entorno
   - En **PATH**, agrega la ruta de `bin`
4. Cierra y abre nuevamente la terminal (o reinicia VSCode) y vuelve a probar:
   - `dot -V`

### 3) Visualización desde el programa
Luego de generar los árboles en la GUI, usa:
- **“Ver gráfico Árbol A”** o **“Ver gráfico Árbol A³”**


```text
interfaz_grafica.py  -> Frontend / interfaz gráfica
Proyecto_final.py    -> Backend / lógica algorítmica
```

## Estructura del proyecto
Proyecto Final Ada/
│
├── interfaz_grafica.py
├── Proyecto_final.py
├── README.md
│
└── resultados/
    ├── matriz_A.txt
    ├── matriz_A3.txt
    ├── arbol_A.dot
    └── arbol_A3.dot