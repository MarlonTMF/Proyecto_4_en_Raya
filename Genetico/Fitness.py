from Simulador import Simulador
from AgenteAleatorio import AgenteAleatorio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AgenteTresEnRaya import AgenteTresEnRaya

class Fitness:
    @staticmethod
    def calcular(individuo, episodios=6):
        """
        Evalúa el fitness del individuo haciéndolo jugar contra un agente ALEATORIO.
        
        Esto genera VARIANZA real: los individuos con buenos pesos ganan,
        los malos pierden. Sin varianza, el algoritmo genético no evoluciona.
        
        Episodios: 4 partidas (2 como X, 2 como O) para reducir ruido estadístico.
        """
        puntaje_total = 0

        for i in range(episodios):
            if i % 2 == 0:
                # Individuo juega como X contra aleatorio O
                agente_x = AgenteTresEnRaya(n=4, altura=2, jugador='X', pesos_heuristica=individuo.pesos)
                agente_o = AgenteAleatorio(jugador='O')
                resultado, turnos = Simulador.jugar(agente_x, agente_o)
                ganador_esperado = 'X'
            else:
                # Individuo juega como O contra aleatorio X
                agente_x = AgenteAleatorio(jugador='X')
                agente_o = AgenteTresEnRaya(n=4, altura=2, jugador='O', pesos_heuristica=individuo.pesos)
                resultado, turnos = Simulador.jugar(agente_x, agente_o)
                ganador_esperado = 'O'

            if resultado == ganador_esperado:
                puntaje_total += 3                      # Victoria: 3 puntos
                puntaje_total += (64 - turnos) * 0.05  # Bonus por ganar rápido
            elif resultado == 'Empate':
                puntaje_total += 1                      # Empate: 1 punto (malo contra aleatorio)
            # Derrota: 0 puntos

        individuo.fitness = puntaje_total
        return puntaje_total

