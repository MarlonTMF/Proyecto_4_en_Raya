import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AgenteTresEnRaya import AgenteTresEnRaya

class AgenteAleatorio(AgenteTresEnRaya):
    """
    Agente que selecciona movimientos completamente al azar.
    Hereda de AgenteTresEnRaya para tener acceso a getResultado(),
    pero sobreescribe programa() para elegir movidas al azar.
    
    Sirve como oponente débil en el entrenamiento genético,
    generando la VARIANZA necesaria para que el algoritmo evolucione.
    """
    def __init__(self, jugador='O'):
        # Altura=1 solo para inicializar, no se usará el Minimax
        super().__init__(n=4, altura=1, jugador=jugador)

    def programa(self):
        """Sobreescribe: ignora Minimax y elige al azar."""
        if self.estado and self.estado.jugador == self.jugador_id:
            if self.estado.movidas:
                accion = random.choice(self.estado.movidas)
                self.set_acciones(accion)

