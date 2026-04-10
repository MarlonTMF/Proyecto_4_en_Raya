import random
from AgenteIA.AgenteJugador import AgenteJugador

class AgenteAleatorio(AgenteJugador):
    def __init__(self, jugador='O'):
        # La altura no importa ya que no usa Minimax
        AgenteJugador.__init__(self, altura=1)
        self.jugador_id = jugador

    def programa(self):
        """Sobrescribe el Minimax para devolver un movimiento legal al azar."""
        if self.estado and self.estado.jugador == self.jugador_id:
            if self.estado.movidas:
                # Selecciona una jugada completamente al azar
                movida = random.choice(list(self.estado.movidas))
                # Limpiar sus propias acciones de la cola (si aplica)
                self.set_acciones(None)
                return movida
        return None
