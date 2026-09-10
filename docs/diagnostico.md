# Diagnóstico del pipeline

## Parte 1 — Diagnóstico

### 1.1 Los cuatro defectos

**Defecto 1 — Jobs sin dependencia entre sí**
- El job `publicar` no declara `needs: validar`, por lo que ambos jobs se
  ejecutan en paralelo, por lo que no existe quality gate. Un commit que falla las pruebas o el
  análisis de calidad genera igualmente un artefacto publicado, porque `publicar` no espera
  el resultado de `validar` ni depende de él.

**Defecto 2 — El artefacto publicado no es el que fue validado**

- `publicar` ejecuta `python -m build` en su propia máquina, construyendo el
  paquete desde cero en lugar de reutilizar lo que `validar` ya verificó. No hay garantía de que sean idénticos

**Defecto 3 — Instalación desde `requirements.txt` en lugar del archivo de bloqueo**

- Se instala con `pip install -r requirements.txt`, pese a que el repositorio
  incluye `requirements.lock` con versiones fijas. Por tanto, se pierde reproducibilidad.

**Defecto 4 — Sin caché de dependencias**

- `actions/setup-python` se usa sin el parámetro `cache`.
- Cada ejecución levanta una máquina limpia y descarga todas las
  dependencias desde el registro público, en los dos jobs. 

### 1.2 El defecto que explica la duración

El defecto 4 referido con la ausencia de caché es el que explica el tiempo registrado en
`docs/linea-base.md`.

Las tres ejecuciones de línea base promediaron entre 40-38seg, con la instalación de dependencias
concentrando la mayor parte de ese tiempo, pues cada job descarga los paquetes desde el registro
público porque la máquina virtual se destruye al terminar y el caché local de pip
(`~/.cache/pip`) no sobrevive entre ejecuciones. 

### 1.3 El vínculo con el caso transversal
Ataca la etapa de despliegue. En el caso de la sesión uno, una problemática era una persona que conocía del despliegue; sin embargo, el resto del equipo no lo ejecutaba. En este caso, se orienta en el mismo lugar, con la diferencia que este se remonta más a un apartado técnico que de una dependencia humana.


### 1.4 La métrica DORA

De las cuatro métricas DORA, las dos alcanzables son *lead time de cambios* y *tasa de fallos de cambio*.

Elegimos **lead time de cambios**. La corrección del defecto 4 reduce directamente el tiempo
que transcurre entre el commit y la retroalimentación automática, que es el tramo del lead
time que el pipeline controla. Una retroalimentación más rápida reduce además el costo de
corrección, porque el desarrollador conserva el contexto del cambio.

### 1.5 El proxy

Este sería la duración total del workflow, promedio de tres ejecuciones consecutivas
disparadas manualmente sin modificar archivos. se busca una meta de aproximadamente un 30% de reducción en cuanto al tiempo.

---

## Parte 4 — Resultados

### 4.1 Medición posterior
- 1: 1min, 12seg
- 2: 1 min, 30seg

Cabe aclarar, que en la anterior etapa, esto se debía puesto a que las etapas se realizaban de manera paralela. En este caso, es secuencial, y el punto de publicar artefacto es mucho más agul (13-14seg aprox) a comparación de las anetriores corridas con un aproximado de 37seg.

### 4.2 Justificación de la versión

**Versión declarada: [1.2.1]**

Se sube un número adicional al valor de patch, pues se ha corregido el .yaml del proyecto. No impacta directamente al cliente por lo que no es necesario enfocarse en el número alto y bajo.

### 4.3 Lo que no se resolvió

El artefacto publicado se construye por segunda vez, en una máquina distinta
de la que ejecutó las validaciones.**

Aunque se corrigió la dependencia entre jobs con `needs: validar`, el job `publicar` sigue ejecutando `python -m build` en su propio entorno. Lo que se publica es un binario reconstruido, no el mismo que fue sometido a pruebas y análisis de calidad.

Para resolverlo:

1. Que el job `validar` construya el paquete y lo suba con `actions/upload-artifact`.
2. Que el job `publicar` lo recupere en lugar de reconstruirlo.

De ese modo el artefacto validado y el artefacto publicado serían el mismo archivo, con una
única construcción por corrida.
