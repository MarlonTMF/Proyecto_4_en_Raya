from AgenteIA.Entorno import Entorno
from AgenteIA.AgenteJugador import ElEstado

class Tablero(Entorno):
    def __init__(self, n=4):
        super().__init__()
        self.n = n
        tablero = {}
        movidas = []
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                for z in range(1, n + 1):
                    movidas.append((x, y, z))
        
        # Estado inicial
        self.juegoActual = ElEstado(jugador='X', get_utilidad=0, tablero=tablero, movidas=movidas)

    def get_percepciones(self, agente):
        return self.juegoActual

    def ejecutar(self, agente, accion):
        if accion:
            # El agente calcula el nuevo estado
            self.juegoActual = agente.getResultado(self.juegoActual, accion)

    def evolucionar(self):
        # Procesamos un agente a la vez por frame para no bloquear la UI
        for agente in self.get_agentes():
            # Solo permitimos actuar al agente cuyo turno coincide
            if self.juegoActual.jugador == getattr(agente, 'jugador_id', None):
                percepcion = self.get_percepciones(agente)
                agente.estado = percepcion
                agente.set_percepciones(percepcion)
                accion = agente.programa()
                
                # Soportar tanto retorno directo como set_acciones()
                if not accion:
                    acciones = agente.get_acciones()
                    if acciones:
                        accion = acciones
                        agente.set_acciones(None) # Limpiar
                
                if accion:
                    self.ejecutar(agente, accion)
                    # Una vez ejecutado el movimiento, detenemos esta iteración 
                    # para que la UI se refresque antes del siguiente turno.
                    break

    def finalizar(self):
        # El juego termina si hay un ganador o no quedan movimientos
        if self.juegoActual.get_utilidad != 0 or not self.juegoActual.movidas:
            return True
        return False
