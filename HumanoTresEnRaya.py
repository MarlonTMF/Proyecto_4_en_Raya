from AgenteTresEnRaya import AgenteTresEnRaya


class HumanoTresEnRaya(AgenteTresEnRaya):
    def __init__(self, n=4, jugador='X'):
        AgenteTresEnRaya.__init__(self, n)
        self.h = n
        self.v = n
        self.d = n
        self.k = n
        self.movida_pendiente = None
        self.jugador_id = jugador

    def programa(self):
        # Solo procesar movimiento si es nuestro turno
        if self.estado and self.estado.jugador != self.jugador_id:
            self.movida_pendiente = None # Descartar clics fuera de turno
            return

        if self.movida_pendiente:
            movida = self.movida_pendiente
            self.movida_pendiente = None
            
            # Validar si la casilla está libre
            if movida in self.estado.movidas:
                self.set_acciones(movida)
            else:
                print(f"Error: La casilla {movida} ya está ocupada o no es válida.")
        else:
            # No hay movida pendiente, simplemente regresamos
            # La UI se encargará de setear movida_pendiente
            pass

