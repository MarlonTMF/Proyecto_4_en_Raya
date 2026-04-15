from AgenteIA.AgenteJugador import AgenteJugador
from AgenteIA.AgenteJugador import ElEstado


class AgenteTresEnRaya(AgenteJugador):

    def __init__(self, n=4, altura=3, jugador='O', pesos_heuristica=None):
        AgenteJugador.__init__(self, altura)
        self.h = n
        self.v = n
        self.d = n
        self.k = 4  # Jugamos a 4 en raya
        self._ventanas = self._generar_ventanas()
        self.jugador_id = jugador
        self.tecnica = "fun_eval"
        
        # Pesos por defecto si no son provistos por el Algoritmo Genético
        if pesos_heuristica is None:
            # --- PESOS MANUALES ORIGINALES (antes del AG) ---
            # 'linea_1': 5, 'linea_2': 50, 'linea_3': 500,
            # 'centro': 30, 'esquina': 25, 'cara': 10, 'arista': 5
            # -------------------------------------------------
            # PESOS EVOLUCIONADOS por Algoritmo Genético (Ronda 2 — Fitness: 33.25)
            # Descubrimientos clave: cara (+920%), centro (+210%), linea_2 (-74%)
            self.pesos = {
                'linea_1': 9,
                'linea_2': 13,
                'linea_3': 389,
                'centro':  93,
                'esquina': 15,
                'cara':    102,
                'arista':  7
            }
        else:
            self.pesos = pesos_heuristica
            
        # --- Pre-Cálculo Geométrico para Optimización ---
        cx, cy, cz = (self.h + 1) / 2, (self.v + 1) / 2, (self.d + 1) / 2
        self._distancias = {}
        self._tipo_posicion = {}
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                for z in range(1, self.d + 1):
                    pos = (x, y, z)
                    self._distancias[pos] = (x-cx)**2 + (y-cy)**2 + (z-cz)**2
                    self._tipo_posicion[pos] = sum(1 for c in pos if c in (1, self.h))

    def jugadas(self, estado):
        """Devuelve los movimientos permitidos, rapidísimo usando pre-cálculo de cercanía al centro."""
        # Ordenar movimientos usando la tabla hash pre-calculada
        return sorted(estado.movidas, key=self._distancias.get)

    def getResultado(self, estado, m):
        if m not in estado.movidas:
            return ElEstado(jugador=('O' if estado.jugador == 'X' else 'X'),
                            get_utilidad=self.computa_utilidad(estado.tablero, m, estado.jugador),
                            tablero=estado.tablero, movidas=estado.movidas)
        tablero = estado.tablero.copy()
        tablero[m] = estado.jugador
        movidas = list(estado.movidas)
        movidas.remove(m)
        return ElEstado(jugador=('O' if estado.jugador == 'X' else 'X'),
                        get_utilidad=self.computa_utilidad(tablero, m, estado.jugador),
                        tablero=tablero, movidas=movidas)

    def get_utilidad(self, estado, jugador):
        return estado.get_utilidad if jugador == 'X' else -estado.get_utilidad

    def testTerminal(self, estado):
        return estado.get_utilidad != 0 or len(estado.movidas) == 0

    def mostrar(self, estado):
        tablero = estado.tablero
        print("\nTablero 3D (4x4x4) - Capas Z=1 a Z=4")
        # Imprimir cabecera de capas
        for z in range(1, self.d + 1):
            print(f"  Capa {z}".ljust(12), end="")
        print()
        
        for x in range(1, self.h + 1):
            for z in range(1, self.d + 1):
                for y in range(1, self.v + 1):
                    val = tablero.get((x, y, z), '.')
                    print(val + " ", end="")
                print("    ", end="")
            print()
        print("-" * 50)

    def computa_utilidad(self, tablero, m, jugador):
        direcciones = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
            (0, 1, 1), (0, 1, -1),
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)
        ]
        for d in direcciones:
            if self.en_raya(tablero, m, jugador, d):
                return +1 if jugador == 'X' else -1
        return 0

    def _generar_ventanas(self):
        ventanas = []
        direcciones = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
            (0, 1, 1), (0, 1, -1),
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)
        ]
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                for z in range(1, self.d + 1):
                    for dx, dy, dz in direcciones:
                        if (1 <= x + dx * (self.k - 1) <= self.h and
                            1 <= y + dy * (self.k - 1) <= self.v and
                            1 <= z + dz * (self.k - 1) <= self.d):
                            ventana = []
                            for i in range(self.k):
                                ventana.append((x + dx * i, y + dy * i, z + dz * i))
                            ventanas.append(ventana)
        return ventanas

    def en_raya(self, tablero, m, jugador, delta_x_y_z):
        if not m or len(m) != 3:
            return False
        (dx, dy, dz) = delta_x_y_z
        x, y, z = m
        n = 0
        while tablero.get((x, y, z)) == jugador:
            n += 1
            x, y, z = x + dx, y + dy, z + dz
        x, y, z = m
        while tablero.get((x, y, z)) == jugador:
            n += 1
            x, y, z = x - dx, y - dy, z - dz
        n -= 1
        return n >= self.k
        
    def funcion_evaluacion(self, estado):
        if self.testTerminal(estado):
            # Victoria explosiva
            return self.get_utilidad(estado, 'X') * 1000000

        tablero = estado.tablero
        puntaje = 0
        pesos = self.pesos  # Cache local más rápida

        # Evaluar ventanas de conexión (líneas potenciales)
        for ventana_coords in self._ventanas:
            conteo_x = 0
            conteo_o = 0
            for coord in ventana_coords:
                ficha = tablero.get(coord, '.')
                if ficha == 'X':
                    conteo_x += 1
                elif ficha == 'O':
                    conteo_o += 1
            
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
                elif conteo_o == 2: puntaje -= pesos['linea_2'] * agresividad_o
                elif conteo_o == 3: puntaje -= pesos['linea_3'] * agresividad_o

        # Evaluar posiciones estratégicas con tabla hash pre-calculada
        for pos, ficha in tablero.items():
            if ficha == '.':
                continue
            
            multiplicador = 1 if ficha == 'X' else -1
            extremos = self._tipo_posicion[pos]
            
            if extremos == 3:
                puntaje += multiplicador * pesos['esquina']
            elif extremos == 2:
                puntaje += multiplicador * pesos['arista']
            elif extremos == 1:
                puntaje += multiplicador * pesos['cara']
            elif extremos == 0:
                puntaje += multiplicador * pesos['centro']

        return puntaje

    def programa(self):
        # Solo actuar si es nuestro turno ('O' por defecto)
        if self.estado and self.estado.jugador == self.jugador_id:
            super().programa()