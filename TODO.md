# TODO - Migración Graphviz -> JSON (Árbol Binario Equilibrado)

- [ ] Leer y proponer plan de cambios (ya disponible en el enunciado) y confirmar.
- [ ] Modificar `interfaz_grafica.py`:
  - [ ] Eliminar importaciones `subprocess` y `shutil`.
  - [ ] Eliminar/ dejar de usar `generar_imagen_graphviz` y `find_dot_executable`.
  - [ ] Eliminar botones “Ver gráfico Árbol A” y “Ver gráfico Árbol A³”.
  - [ ] Agregar botones “Abrir JSON Árbol A” y “Abrir JSON Árbol A³” que abran `resultados/arbol_A.json` y `resultados/arbol_A3.json`.
  - [ ] Actualizar mensaje/guardado en `generar()` para exportar `arbol_A.json` y `arbol_A3.json` usando la nueva función `arbol_a_json_texto`.
  - [ ] Mantener visualización ASCII en pantalla.
- [ ] Modificar `Proyecto_final.py`:
  - [ ] Verificar existencia de `arbol_json_a_diccionario` y `arbol_a_json_texto` (ya parecen existir) y asegurar que sean los usados.
  - [ ] Eliminar `exportar_arbol_dot` y cualquier referencia DOT/Graphviz.
- [ ] Actualizar `README.md`:
  - [ ] Eliminar menciones a Graphviz, `.dot` y `.png`.
  - [ ] Incluir sección sobre representación JSON y archivos `arbol_A.json` y `arbol_A3.json`.
- [ ] Verificar que el proyecto corre sin Graphviz:
  - [ ] `python interfaz_grafica.py`
  - [ ] Generar con `n=4` y comprobar que crea `resultados/arbol_A.json` y `resultados/arbol_A3.json`
  - [ ] Probar búsqueda en árbol.

