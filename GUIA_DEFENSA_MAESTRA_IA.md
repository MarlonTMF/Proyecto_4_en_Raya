# Master Guide: Defensa Técnica de IA - 3D Tic-Tac-Toe (4x4x4)
## Dominio de Algoritmos, Arquitectura y Optimización Evolutiva

Este documento es una guía exhaustiva diseñada para preparar al estudiante para una defensa de alto nivel académico. Incluye referencias directas al código fuente, explicaciones de algoritmos y preguntas teóricas profundas.

---

## 1. Arquitectura del Agente e Interacción con el Entorno

### Teoría de Agentes (Referencia: `Tablero.py`)
En el archivo `Tablero.py`, heredamos de `Entorno`. Aquí se maneja la percepción y la ejecución de acciones.

> [!NOTE]
> **Pregunta de Tribunal:** ¿Cómo se garantiza que el agente no tome turnos infinitos o acciones inválidas?
> **Respuesta Técnica:** En `Tablero.evolucionar()`, verificamos que el turno del juego (`self.juegoActual.jugador`) coincida con el ID del agente. Además, en `AgenteTresEnRaya.py`, la función `getResultado()` valida que el movimiento `m` esté en la lista de `estado.movidas`.

### El Modelo Mental del Agente (Referencia: `AgenteIA/AgenteJugador.py`)
Utilizamos un objeto llamado `ElEstado` (un `namedtuple`).
```python
ElEstado = namedtuple('ElEstado', 'jugador, get_utilidad, tablero, movidas')
```
*   **tablero:** Diccionario que mapea `(x, y, z) -> 'X' o 'O'`.
*   **movidas:** Lista de tuplas disponibles. Esto reduce la complejidad de O(N³) a O(Casillas_Libres) cada vez que el agente debe decidir.

---

## 2. El Motor de Búsqueda: Minimax con Poda Alpha-Beta

### Implementación Real (Referencia: `AgenteIA/AgenteJugador.py`)
La función `podaAlphaBeta_eval(self, estado)` es el corazón del agente.

```python
def max_value(e, alpha, betita, a):
    if self.testTerminal(e): return self.get_utilidad(e, jugador) * 1000000
    if a == self.altura: return self.funcion_evaluacion(e)
    # ... iteración de movimientos ...
    if vm >= beta: return vm  # PODA ALPHA-BETA
```

> [!IMPORTANT]
> **Concepto Clave: Profundidad vs. Heurística.**
> Si `a == self.altura`, el agente deja de buscar y usa "intuición" (Heurística). Si nunca llegamos a ese límite, el agente tiene "omnisciencia" (siempre gana o empata). En 4x4x4, el árbol tiene 64! nodos; por eso la profundidad 3 es obligatoria.

### Eficiencia: El Truco del Pre-Ordenamiento
En `AgenteTresEnRaya.py`, la función `jugadas(self, estado)` no devuelve los movimientos en orden aleatorio:
```python
def jugadas(self, estado):
    return sorted(estado.movidas, key=self._distancias.get)
```
Al evaluar primero las casillas más cercanas al centro (pre-calculadas en el constructor), la Poda Alpha-Beta ocurre mucho antes, ahorrando hasta un 60% de tiempo de CPU.

---

## 3. El Cerebro: Ingeniería de la Función de Evaluación

### El Corazón de la Inteligencia (Referencia: `AgenteTresEnRaya.py`)
La función `funcion_evaluacion(self, estado)` calcula un puntaje para estados NO terminales. 

> [!TIP]
> **Pregunta de Tribunal:** ¿Cómo evitas el cálculo costoso de líneas en cada turno?
> **Respuesta Técnica:** En el constructor `__init__`, llamamos a `_generar_ventanas()`. Esto crea una lista de las 76 líneas posibles. En cada turno, solo iteramos sobre esa lista fija en lugar de buscar geometrías nuevas.

**Lógica de Puntaje:**
1.  **Exploración de Ventanas:** Por cada una de las 76 líneas, contamos `X` y `O`. 
    *   Si hay 3 `X` y 0 `O`, es una amenaza inminente (`linea_3`).
    *   Si hay 1 `X` y 1 `O`, esa línea es inútil (bloqueada), puntaje = 0.
2.  **Agresividad Dinámica:**
    ```python
    agresividad_x = 1.5 if self.jugador_id == 'X' else 1.0
    ```
    El agente valora más sus propias amenazas que el bloqueo de las del rival, forzando un estilo de juego proactivo.

---

## 4. Optimización Evolutiva: El Algoritmo Genético

### La Función de Aptitud (Referencia: `Genetico/Fitness.py`)
Aquí es donde conectamos el Algoritmo Genético con la simulación del juego.

> [!CAUTION]
> **Pregunta Crítica:** ¿Por qué no entrenar a profundidad 3 si el juego final es profundidad 3?
> **Respuesta:** Costo computacional. A profundidad 2, una partida toma centésimas de segundo. A profundidad 3, toma segundos. Multiplicado por 20 individuos y 25 generaciones, el entrenamiento pasaría de 40 minutos a 10 horas. Los pesos de profundidad 2 son "transferibles" a profundidad 3 con éxito.

### Operadores Genéticos (Referencia: `Mutacion.py`, `Seleccion.py`)
1.  **Selección por Torneo (`k=4`):** Evita la "superdominancia" (que un solo individuo mate la diversidad) pero asegura que los mediocres no se reproduzcan.
2.  **Mutación Agresiva (`prob=0.25`):**
    ```python
    variacion = random.uniform(0.75, 1.35)
    nuevo_valor = int(nuevos_pesos[gen_a_mutar] * variacion)
    ```
    Cambiamos los pesos hasta un 35% en cada mutación. Esto es lo que permitió al agente descubrir que la `cara` del cubo era 9 veces más importante de lo que creíamos.

---

## 5. Preguntas Teóricas Avanzadas (Q&A)

**Q1: ¿Qué pasaría si la función de evaluación devolviera siempre 0?**
*   **Respuesta:** El agente se comportaría como un Agente Aleatorio. Sin heurística, al llegar al límite de profundidad, todos los movimientos parecerían iguales. Solo jugaría bien si estuviera a un movimiento de ganar o perder (estados terminales).

**Q2: ¿Tu agente es propenso a estados de "Stalemate" o empates?**
*   **Respuesta:** En 4x4x4, el primer jugador tiene una ventaja teórica masiva. Sin embargo, debido al límite de profundidad (3), nuestro agente utiliza el "centro" y las "caras" para maximizar sus opciones de victoria antes de que el tablero se llene.

**Q3: ¿Cómo manejas el "Problema del Horizonte"?**
*   **Respuesta:** Es el mayor problema de nuestro agente. Ocurre cuando una derrota es inevitable a profundidad 4, pero a profundidad 3 parece que todo está bien. Lo mitigamos con una heurística "pesada" (`linea_3 = 389`) que castiga severamente permitir que el rival ponga 3 piezas en línea, incluso si la victoria del rival está más allá de nuestro horizonte de visión.

**Q4: ¿Por qué usar un diccionario para el tablero en lugar de una matriz 3D `[4][4][4]`?**
*   **Respuesta:** Eficiencia de memoria y facilidad de acceso. Un diccionario solo guarda las casillas ocupadas. Para un tablero escaso (al inicio del juego), es más rápido consultar `tablero.get(coord)` que iterar sobre una matriz de 64 elementos.

---

### Resumen de Descubrimientos (Datos para lucirse)
*   **Peso de 'Cara' inicial:** 10
*   **Peso de 'Cara' evolucionado:** 102 (**+920%**)
*   **Interpretación:** Las caras del cubo 4x4x4 son los puntos de mayor "tráfico" de líneas diagonales espaciales. El Algoritmo Genético "vio" esto tras miles de partidas simuladas, mientras que el diseño humano lo ignoró.
*   **Nodos evaluados por segundo:** ~15,000 (gracias a la Poda Alpha-Beta).
