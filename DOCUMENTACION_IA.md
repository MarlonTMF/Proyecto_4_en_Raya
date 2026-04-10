# Arquitectura y Estrategias de la IA: 3D Tic-Tac-Toe (4x4x4)

Este documento detalla los desafíos algorítmicos, trampas lógicas y estrategias matemáticas empleadas para desarrollar un agente inteligente competitivo en un tablero 3D mediante el clásico algoritmo **Minimax con Poda Alfa-Beta**.

---

## 1. El Desafío del Espacio de Estados (4x4x4)

A diferencia del clásico "Tres en Raya" de 3x3 (donde existen 9 casillas), un cubo de 4x4x4 posee **64 posiciones posibles y 76 direcciones diferentes** para formar "líneas ganadoras" (horizontales, verticales, diagonales tridimensionales).

El factor de ramificación inicial es 64. Si usamos Minimax a una profundidad de 4 movimientos, el algoritmo debe explorar teóricamente millones de nodos (`64 * 63 * 62 * 61`), lo que resulta imposible en tiempo real sin optimizaciones agresivas.

---

## 2. Optimización de Rendimiento (Caching Geométrico)

**Problema Original**: La IA tardaba alrededor de **17.8 segundos** por turno.
En cada evaluación de nodo, la IA aplicaba iteraciones de Python complejas para calcular matemáticamente (con la ecuación de la esfera matemática euclidiana) qué tan cerca estaba cada casilla vacía del centro del cubo. Posteriormente, calculaba nuevamente qué nodos representaban las esquinas o centros para otorgarles puntos.

**Solución - Pre-cálculo mediante Tabla Hash**:
Se eliminó la matemática dinámica. Al instanciar el juego, la matriz 3D calcula la distancia y relevancia absoluta (Esquina, Centro de Cara, Arista, Centro Absoluto) de las 64 coordenadas geométricas *una sola vez*, almacenándolas en la RAM dentro de un diccionario Hash. Durante el paso intensivo de la Poda Alfa-Beta, el agente simplemente consulta estos valores, eliminando la sobrecarga computacional.
**Resultado:** Incremento masivo del rendimiento de la Inteligencia Artificial (Reducción dramática del tiempo a ~3 segundos).

---

## 3. Trampas del Algoritmo Minimax y sus Soluciones

Durante el desarrollo del agente, ocurrieron dos comportamientos "anómalos" fascinantes debido a que Minimax sigue reglas estrictamente matemáticas pero carece de "sentido común".

### 3.1. El Efecto "Techo de Puntaje" (El Miedo a Ganar)
**Síntoma**: Estando a un solo movimiento de realizar las 4 piezas en raya, la IA deliberadamente decidía colocar una ficha en otro lado y negarse a dar el golpe de gracia.
**Análisis**:
- Las evaluaciones a mitad de la partida otorgaban altos puntos por control territorial (ej. `1,500 puntos` por tener buenas posiciones centrales y una línea armada).
- La función de "Fin de Juego" (estado terminal) otorgaba la utilidad estricta y tradicional de Von Neumann: `+1` si ganaba, `-1` si perdía.
- La IA maximizadora, al ver sus opciones entre ganar (`+1 punto`) o simplemente dominar el centro del tablero sin ganar la partida (`+1500 puntos`), elegía lógicamente la opción de mayor valor.
**Solución**: Se escaló la utilidad del nodo terminal a valores apocalípticos (`± 1,000,000 de puntos`). Ahora la IA comprende que el "peso" de la victoria/derrota absoluta supera a cualquier beneficio estratégico temporal.

### 3.2. El Efecto "Cobardía" o Juego Espejo
**Síntoma**: El Agente se negaba a formular su propio ataque. Solo se dedicaba a bloquear permanentemente cualquier ficha colocada por el oponente, siempre forzando el juego al empate por hastío.
**Análisis**:
- Por simetría heurística, construir una línea ofensiva de 2 fichas daba matemáticamente el mismo puntaje (`50 puntos`) que bloquear la línea de 2 fichas del oponente (`50 puntos`).
- Dado que el algoritmo Minimax asume el peor resultado posible (asume que el humano siempre bloqueará cualquier ataque), destruir las estructuras del oponente se percibía como el camino más "seguro" de la recursión.
**Solución - Multiplicador de Agresividad**:
Se introdujo una constante de Agresividad en los pesos (`x 1.5`).
Si la IA logra establecer una línea de 2 piezas, se auto-premia con `75 puntos`. Si bloquea la del adversario, se conforma con `50 puntos`. 
Al romper la simetría, la IA cambia drásticamente de temperamento. En lugar de ser puramente reaccionaria, adopta el instinto de ataque buscando armar "Tenedores" (Double Threats directas) atacando en dos ángulos simultáneos. Si bien obedece a las prioridades defensivas si el humano amenaza con líneas de 3 (bloqueo vital), en estados neutrales intentará dominar al oponente sistemáticamente.

---

## 4. Evolución Numérica (El Algoritmo Genético)

A pesar de nuestra excelente lógica matemática estructural para premiar posiciones (`Centro`, `Esquina`, `Arista`), asignar los multiplicadores y prioridades "a ojo" (valores heurísticos hardcodeados o fijos) es muy limitante. ¿Qué vale más numéricamente: tener dos fichas en una esquina, o tener tres fichas pegadas a la pared y aisladas?

**Implementación del Algoritmo Genético**:
Se acopló un módulo simulador de cruce evolutivo genético en modo *Headless* (sin carga computacional de gráficos, ejecutado silenciosamente en consola).
1.  **Población**: Genera decenas de conjuntos aleatorios entre sí (cromosomas y pesos).
2.  **Fitness (Aptitud)**: Los enfrenta entre sí para evaluar qué pesos obtienen mayor porcentaje de victorias al usarse en combate. 
3.  **Hibridación e Iteración**: Tras `G` generaciones en las que los mejores se mezclan mediante Crossover de N-Puntos y sufren fluctuaciones Gaussianas (mutaciones numéricas de `+x%`), el resultado escupe el Fenotipo Definitivo: la serie de pesos numéricos teóricamente imbatibles para el juego de Tic-Tac-Toe en Tres Dimensiones.
