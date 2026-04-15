# Informe del Proyecto: Agentes Inteligentes en Tic-Tac-Toe 3D (4x4x4)

## 1. Explicación del problema que están resolviendo

El problema central que aborda este proyecto consiste en desarrollar agentes inteligentes (IA) capaces de jugar competitivamente y sin intervención humana al juego de **Tic-Tac-Toe en Tres Dimensiones (3D) con tablero de 4x4x4**, donde el objetivo es conseguir alinear 4 fichas consecutivas.

A diferencia del clásico 3x3 que posee solo 9 celdas y 8 posibles líneas ganadoras, la variante 3D propuesta introduce un incremento exponencial en la complejidad:
- **Espacio de Juego**: Un cubo formado por 64 casillas totales distribuidas en 4 capas espaciales (X, Y, Z).
- **Líneas Ganadoras**: Existen 76 formas diferentes de ganar (filas, columnas, diagonales planas, pilares tridimensionales y súper-diagonales que atraviesan todo el cubo).

Esta magnitud ocasiona que el árbol lógico contenga millones de ramas posibles tras apenas los 3 primeros movimientos. Matemáticamente, obliga a que una búsqueda exhaustiva del mejor movimiento cause saturación computacional. Por lo tanto, el reto es diseñar una Inteligencia Artificial que procese este espacio de estados titánico de manera rápida (en pocos segundos por turno) y que sus movimientos pasen de ser aleatorios a tácticos (priorizando dominar el centro y atacando agresivamente mediante tenedores/amenazas dobles).

---

## 2. Explicación de cada enfoque utilizado

Para resolver el problema planteado, en este proyecto se fusionaron las fortalezas de dos grandes paradigmas de Inteligencia Artificial Clásica: la Búsqueda Adversarial y los Algoritmos Evolutivos.

### Enfoque A: Minimax con Poda Alfa-Beta (Paradigma de Búsqueda Adversarial)

* **Idea Principal**: Minimax es un algoritmo recursivo que, ante un escenario oponente, "imagina" todos los movimientos futuros posibles y elige el camino que minimiza la máxima pérdida esperada. Además, utiliza un atajo lógico ("Poda Alfa-Beta") que le indica a la IA detener la exploración de ramas inútiles cuando ya ha descubierto una jugada que, debido a la óptima respuesta matemática del oponente, es inevitablemente trágica.
* **Cómo resuelve el problema**: Proporciona el "Motor de Decisión" principal al Agente. En cada turno, el Agente 3D traza un árbol predictivo de hasta 4 niveles de profundidad. Utiliza una evaluación heurística matemática (cálculos espaciales y de piezas en raya) para darle un puntaje teórico a tableros no terminados, logrando elegir el movimiento preciso (como bloquear el 3 en raya inminente del humano).
* **Por qué encaja con ese paradigma**: Tic-Tac-Toe 3D es el ejemplo clásico de este paradigma porque es un juego:
    * **Cero-Suma**: Lo que gana un jugador lo pierde el otro.
    * **De Información Perfecta**: No hay niebla de guerra ni azar de dados; ambos saben dónde están todas las fichas. Estas condiciones son matemáticamente ideales para algoritmos descendientes del teorema de Von Neumann, como Minimax.

### Enfoque B: Optimización Genética (Paradigma de Algoritmos Evolutivos / Metaheurísticas)

* **Idea Principal**: Emplear una arquitectura inspirada en la evolución biológica natural (Selección, Cruce, Mutación, Supervivencia) para optimizar aleatoriamente los parámetros numéricos o "pesos" exactos que necesita la heurística de Minimax.
* **Cómo resuelve el problema**: La evaluación heurística de Minimax en 3D necesita "saber" cuántos puntos dar a diferentes posiciones. ¿Qué vale más numéricamente: tener 2 fichas al centro o 3 fichas en el rincón? El Algoritmo Genético automatiza esta búsqueda: creamos un ecosistema "silencioso" (Headless Simulador) con cientos de IAs luchando entre ellas usando diferentes ponderaciones aleatorias de pesos (genes). Luego de múltiples generaciones, las IAs con pesos débiles (que perdieron por no defender bien) "mueren", y aquellas con atributos numéricos victoriosos se clonan y mutan, dejando tras el entrenamiento la matriz de pesos teórica perfecta, inyectable para el Agente Final y obteniendo los valores ganadores sin tener que deducirlos nosotros manualmente.
* **Por qué encaja con ese paradigma**: El espacio de variables ponderables (pesos de las líneas, de las caras del cubo, esquinas, y constantes de agresividad) es un dominio n-dimensional y continuo, casi imposible de afinar matemáticamente usando optimización determinista clásica o Fuerza Bruta. Los algoritmos genéticos operan de maravilla en espacios de búsqueda de estas características aportando diversidad con sus mutaciones y evitando quedarse atrapados en comportamientos sub-óptimos sin tener un conocimiento previo de las reglas de geometría del cubo.
