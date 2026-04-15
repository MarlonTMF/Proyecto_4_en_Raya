# Guía de Preparación: Defensa de Proyecto de Sistemas Inteligentes
## Proyecto: 3D Tic-Tac-Toe (4x4x4) Optimizado con Algoritmo Genético

Esta guía contiene preguntas y respuestas técnicas de nivel avanzado para la defensa ante tribunales de Inteligencia Artificial, cubriendo desde la teoría de agentes hasta la optimización evolutiva aplicada.

---

### I. Teoría de Agentes y Entornos

**1. Define el modelo PEAS para tu agente y describe el tipo de entorno del juego.**
*   **Respuesta:** 
    *   **P (Performance/Desempeño):** Maximizar victorias, minimizar movimientos para ganar, maximizar el puntaje de la función heurística.
    *   **E (Environment/Entorno):** Tablero cúbico de 4x4x4. Es un entorno **competitivo**, **determinista**, **estático**, **discreto** y de **información perfecta**.
    *   **A (Actuators/Actuadores):** El "brazo" virtual que coloca una ficha (X o O) en una de las 64 coordenadas `(x, y, z)`.
    *   **S (Sensors/Sensores):** La lectura del estado actual de la clase `ElEstado` (diccionario de posiciones ocupadas y lista de movimientos disponibles).
    *   **Tipo de Agente:** Es un **Agente basado en utilidad**, ya que utiliza una función heurística para medir qué tan "bueno" es un estado del tablero.

**2. ¿Por qué este problema no se puede resolver mediante una búsqueda simple (BFS o DFS) y requiere búsqueda adversaria?**
*   **Respuesta:** En BFS o DFS, el entorno es pasivo. En el Tres en Raya 3D, existe un **oponente racional** que intenta minimizar nuestra utilidad mientras nosotros intentamos maximizarla. La búsqueda adversaria (Minimax) modela esta interacción, asumiendo que el oponente siempre tomará la mejor decisión posible desde su perspectiva.

---

### II. Algoritmos de Búsqueda Adversaria (Minimax y Poda Alpha-Beta)

**3. Explica el funcionamiento del algoritmo Minimax en tu código.**
*   **Respuesta:** El algoritmo realiza una búsqueda recursiva en el árbol de juego. En los niveles "MAX", el agente elige el movimiento que maximiza el valor devuelto por los hijos. En los niveles "MIN" (turno del oponente), se elige el movimiento que devuelve el valor mínimo. La recursión se detiene al llegar a un **estado terminal** (ganador/empate) o a la **profundidad límite** (altura=3), donde se aplica la función de evaluación.

**4. ¿Qué es la Poda Alpha-Beta y qué beneficio real aportó a tu proyecto?**
*   **Respuesta:** Es una técnica de optimización para Minimax que elimina ramas del árbol de búsqueda que no afectarán la decisión final. 
    *   **Alpha:** Es el mejor valor que MAX ha encontrado hasta ahora.
    *   **Beta:** Es el mejor valor que MIN ha encontrado hasta ahora.
    *   **Beneficio:** Permite explorar el árbol mucho más rápido. En un tablero de 4x4x4 con 64 posiciones, el factor de ramificación es enorme. Sin la poda, el tiempo de respuesta sería inaceptable para una profundidad de 3. Con la poda, podemos ignorar miles de nodos irrelevantes.

**5. ¿Cómo influye el orden de los movimientos (`jugadas`) en la eficiencia de la Poda Alpha-Beta?**
*   **Respuesta:** La poda es más eficiente si encontramos los mejores movimientos primero. En nuestro código, usamos un pre-cálculo de distancias al centro. Al evaluar primero el centro del cubo (donde hay más líneas ganadoras), encontramos valores altos de Alpha (o bajos de Beta) rápidamente, permitiendo podar el resto de las ramas (como las aristas alejadas) mucho antes.

---

### III. Optimización Heurística y Algoritmo Genético (AG)

**6. ¿Por qué decidiste usar un Algoritmo Genético en lugar de definir los pesos manualmente?**
*   **Respuesta:** La intuición humana es limitada para espacios 3D. Un humano podría pensar que las esquinas son lo más importante, pero el AG descubrió que las **caras del cubo** y el **núcleo central** tienen muchísima más importancia estratégica en un sistema 4x4x4. El AG permite realizar una **búsqueda estocástica global** en el espacio de parámetros de la heurística.

**7. Describe el ciclo de vida de tu AG: Población, Selección, Cruce y Mutación.**
*   **Respuesta:**
    *   **Población:** 20 individuos, cada uno con un set de 7 pesos (parámetros).
    *   **Selección (Torneo k=4):** Se eligen 4 al azar y el más apto gana el derecho de reproducirse. Esto asegura presión selectiva.
    *   **Cruce (One-point Crossover):** Se mezclan los pesos de dos padres para crear hijos con características combinadas.
    *   **Mutación (25% prob):** Se altera el valor de los pesos aleatoriamente. Es vital para la **exploración** y para evitar caer en **óptimos locales**.

**8. Técnicamente, ¿qué es la "Función de Aptitud" (Fitness) en tu AG y por qué cambiaste el oponente de Minimax a Aleatorio?**
*   **Respuesta:** El Fitness es una medida de qué tan exitoso es un set de pesos. Se calcula haciendo que la IA juegue 6 partidas. El cambio al oponente aleatorio fue necesario para **generar varianza**. Si entrenamos Minimax contra Minimax a poca profundidad, casi siempre empatan (Fitness constante), lo que estanca la evolución. Contra un agente aleatorio, los pesos buenos ganan rápido y los malos pierden, permitiendo que el AG distinga quién es realmente mejor.

---

### IV. Análisis Crítico y Resultados

**9. ¿Cuál fue el descubrimiento más sorprendente del entrenamiento genético?**
*   **Respuesta:** El peso de las **caras del cubo** subió un 920% (`cara: 10 -> 102`). Esto indica que el control de los planos medios del cubo es tácticamente superior a las esquinas o aristas, algo que no es obvio en el Tic-Tac-Toe tradicional de 2D.

**10. ¿Qué limitaciones tiene tu implementación actual y cómo las mejorarías?**
*   **Respuesta:**
    *   **Limitación:** La profundidad de 3 es buena pero no imbatible para un experto.
    *   **Mejora:** Implementar **Tablas de Transposición** (memoización) para no re-evaluar estados ya vistos, permitiendo subir a profundidad 4 o 5.
    *   **Limitación:** Los pesos se optimizaron contra un agente aleatorio.
    *   **Mejora:** Realizar una fase final de entrenamiento de "ajuste fino" contra el propio agente Minimax una vez que ya tiene una base sólida para aprender a bloquear estrategias avanzadas.

---

### V. Dominio del Código (Preguntas "Trampa")

**11. En tu archivo `Tablero.py`, ¿por qué usas un `break` dentro del bucle `evolucionar`?**
*   **Respuesta:** Para evitar que un solo agente tome múltiples turnos en un mismo ciclo de actualización o para permitir que la interfaz gráfica (si existiera o se implementara) se refresque entre jugadas, manteniendo la lógica de turnos sincronizada.

**12. ¿Cómo manejas el problema de las 76 líneas ganadoras posibles sin que el programa sea lento?**
*   **Respuesta:** Usamos un **pre-cálculo geométrico**. En el constructor de `AgenteTresEnRaya`, generamos todas las "ventanas" (líneas de 4) posibles una sola vez. Durante el juego, la función heurística solo recorre esa lista pre-calculada en lugar de buscar líneas nuevas en cada nodo, optimizando masivamente el cálculo.
