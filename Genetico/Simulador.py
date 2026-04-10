import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tablero import Tablero
from AgenteTresEnRaya import AgenteTresEnRaya

class Simulador:
    @staticmethod
    def jugar(agente_x, agente_o):
        """
        Inicia una partida entre dos agentes en modo headless (sin gráficos).
        Retorna:
            - 'X' si gana agente_x
            - 'O' si gana agente_o
            - 'Empate'
            - Un número (turnos jugados, para premiar rapidez)
        """
        juego = Tablero(n=4)
        juego.insertar(agente_x)
        juego.insertar(agente_o)
        
        turnos = 0
        while not juego.finalizar():
            juego.evolucionar()
            turnos += 1
            if turnos > 64 * 2: # Límite de seguridad
                break
                
        utilidad = juego.juegoActual.get_utilidad
        if utilidad > 0:
            return 'X', turnos
        elif utilidad < 0:
            return 'O', turnos
        else:
            return 'Empate', turnos
