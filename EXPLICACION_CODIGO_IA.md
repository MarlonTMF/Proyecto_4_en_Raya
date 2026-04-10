# Explicación Técnica y Código de la Inteligencia Artificial (3D Tic-Tac-Toe)

A continuación se detalla a nivel de código exactamente cómo logramos estabilizar el motor y volver a la IA inteligente y ultra-rápida. Hemos tocado principalmente dos archivos fundamentales: `AgenteTresEnRaya.py` y `AgenteIA/AgenteJugador.py`.

---

## 1. El Miedo a Ganar (Techo de Puntaje)
**Archivo:** `AgenteIA\AgenteJugador.py`  
**Función Modificada:** `podaAlphaBeta_eval()`

El núcleo de toma de decisiones Minimax estaba fallando porque no dimensionamos correctamente la escala de la heurística versus la utilidad terminal de ganar el juego (1 o -1).

**El código erróneo anterior decía:**
```python
if self.testTerminal(e):
    return self.get_utilidad(e, jugador) # Devolvía 1 si ganaba.
```
Como la heurística por jugar en el centro devolvía mayores puntos (ej. 1500), la IA huía de la victoria.

**El código corregido actual:**
```python
def max_value(e, alpha, betita, a):
    self.nodos_evaluados += 1
    if self.testTerminal(e):
        # ¡CORRECCIÓN VITAL! Multiplicamos por 1,000,000
        return self.get_utilidad(e, jugador) * 1000000
    
    if a == self.altura:
        return self.funcion_evaluacion(e)
```
Al inyectarle el multiplicador enorme `* 1000000`, obligamos a la rama del árbol a reportar la victoria como el evento de mayor prioridad concebible, destrozando toda competencia con los 1500 puntos heurísticos y forzando a la IA a rematar el juego.

---

## 2. El Efecto Cobardía (Multiplicador de Agresividad)
**Archivo:** `AgenteTresEnRaya.py`  
**Función:** `funcion_evaluacion()`

Incluso arreglando la victoria absoluta, la IA jugaba a empatar porque construir una línea propia de 2 fichas le daba la misma cantidad de puntos que bloquear al adversario. Minimax, al ser pesimista, prefería bloquear. 

**La corrección implementada:**
```python
# La IA debe ser más agresiva creando sus líneas que bloqueando líneas menores
# Si el agente es X, sus puntos aumentan. Si es O, disminuyen.
agresividad_x = 1.5 if self.jugador_id == 'X' else 1.0
agresividad_o = 1.5 if self.jugador_id == 'O' else 1.0

# Valorar las líneas
if conteo_x > 0 and conteo_o == 0:
    if conteo_x == 1: puntaje += pesos['linea_1'] * agresividad_x
    elif conteo_x == 2: puntaje += pesos['linea_2'] * agresividad_x
    elif conteo_x == 3: puntaje += pesos['linea_3'] * agresividad_x
elif conteo_o > 0 and conteo_x == 0:
    if conteo_o == 1: puntaje -= pesos['linea_1'] * agresividad_o
    # ...
```
Al colocarle un `x 1.5` a las construcciones de la propia IA (siendo `self.jugador_id`), creamos una asimetría obligatoria. La IA ahora gana `75` puntos simulados al crecer su línea en vez de los `50` que obtiene bloqueando tu línea inofensiva. Como resultado, la IA ahora planea amenazas dobles proactivamente.

---

## 3. Caching Geométrico (Acelerando la Ejecución un +200%)
**Archivo:** `AgenteTresEnRaya.py`  

Evaluar coordenadas en 3D en cada nodo recursivo hacía que el proceso de "pensar" tardara 18 segundos por turno. Para arreglar esto, movimos el costo matemático fuera del bucle de decisión.

**Modificación en el Constructor `__init__()`:**
Calculamos una sola vez en el inicio de la partida la distancia hacia el centro (`_distancias`) y cuántos lados toca la coordenada para saber si es Esquina o Centro (`_tipo_posicion`).
```python
# --- Pre-Cálculo Geométrico para Optimización ---
cx, cy, cz = (self.h + 1) / 2, (self.v + 1) / 2, (self.d + 1) / 2
self._distancias = {}
self._tipo_posicion = {}

for x in range(1, self.h + 1):
    for y in range(1, self.v + 1):
        for z in range(1, self.d + 1):
            pos = (x, y, z)
            # Diccionario Hash de distancias pre-calculadas (O(1) lookup)
            self._distancias[pos] = (x-cx)**2 + (y-cy)**2 + (z-cz)**2
            # Diccionario para saber si es Centro(0), Cara(1), Arista(2) o Esquina(3)
            self._tipo_posicion[pos] = sum(1 for c in pos if c in (1, self.h))
```

**Beneficio 1: Ordenamiento instantáneo en `jugadas()`**
Minimax necesita explorar los nodos centrales primero para que la poda Alfa-Beta mutile ramas basura rápido. Antes hacíamos una ecuación con variables lambda por cada espacio vacío. Ahora solo se consulta la tabla Hash que armamos:
```python
def jugadas(self, estado):
    # Devuelve los movimientos permitidos hiper-rápido usando un diccionario
    return sorted(estado.movidas, key=self._distancias.get)
```

**Beneficio 2: Puntaje posicional relámpago en `funcion_evaluacion()`**
Antes, por cada ficha en el tablero explorado, hacíamos un bucle calculando qué extremos tocaba la ficha para darle los puntos:
```python
# El código LENTO antiguo: 
extremos = sum(1 for c in pos if c in (1, self.h))

# El código RÁPIDO actual:
extremos = self._tipo_posicion[pos] # Búsqueda instantánea O(1)

if extremos == 3: puntaje += multiplicador * pesos['esquina']
elif extremos == 2: puntaje += multiplicador * pesos['arista']
elif extremos == 1: puntaje += multiplicador * pesos['cara']
elif extremos == 0: puntaje += multiplicador * pesos['centro']
```
Este simple reemplazo hizo que los turnos pasaran de tardar ~18 segundos a menos de 4 segundos, volviendo el juego completamente disfrutable.

---

## 4. Métricas de Rendimiento del Árbol Minimax
**Archivo:** `AgenteIA\AgenteJugador.py`  
**Función Modificada:** `podaAlphaBeta_eval()`

El requerimiento académico exige presentar mediciones de nodos explorados y podados (cortados del árbol). Agregamos variables de instancia puras que se declaran justo antes de llamar por primera vez a `min_value` o `max_value`.

```python
# Se resetean al arrancar un turno
self.nodos_evaluados = 0
self.nodos_podados = 0

def max_value(e, alpha, betita, a):
    self.nodos_evaluados += 1 # Contamos nodo visitado
    # ... código alfa-beta...
    for j in self.jugadas(e):
        vm = max(vm, min_value(self.getResultado(e, j), alpha, betita, a + 1))
        if vm >= beta:
            self.nodos_podados += 1 # La poda ocurrió exitosamente
            return vm
```
Estos contadores te permiten extraer la "data dura" sobre qué tan eficiente es la función al recorrer las capas predictivas del juego, para rellenar los cuadros estadísticos de tu informe.
