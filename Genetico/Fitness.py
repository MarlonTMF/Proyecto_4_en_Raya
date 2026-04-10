from Simulador import Simulador
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AgenteTresEnRaya import AgenteTresEnRaya

class Fitness:
    @staticmethod
    def calcular(individuo, episodios=2):
        """
        Evalúa el fitness del individuo haciéndolo jugar contra un oponente estático.
        """
        puntaje_total = 0
        
        # Pesos base por defecto para el oponente
        pesos_base = {
            'linea_1': 5, 'linea_2': 50, 'linea_3': 500,
            'centro': 30, 'esquina': 25, 'cara': 10, 'arista': 5
        }
        
        for i in range(episodios):
            # Mitad partidas empieza X, mitad empieza O
            if i % 2 == 0:
                # Individuo es X
                agente_x = AgenteTresEnRaya(n=4, altura=1, jugador='X', pesos_heuristica=individuo.pesos)
                agente_o = AgenteTresEnRaya(n=4, altura=1, jugador='O', pesos_heuristica=pesos_base)
                resultado, turnos = Simulador.jugar(agente_x, agente_o)
                ganador_esperado = 'X'
                perdedor_esperado = 'O'
            else:
                # Individuo es O
                agente_x = AgenteTresEnRaya(n=4, altura=1, jugador='X', pesos_heuristica=pesos_base)
                agente_o = AgenteTresEnRaya(n=4, altura=1, jugador='O', pesos_heuristica=individuo.pesos)
                resultado, turnos = Simulador.jugar(agente_x, agente_o)
                ganador_esperado = 'O'
                perdedor_esperado = 'X'
                
            if resultado == ganador_esperado:
                puntaje_total += 3
                # Bonus por ganar rápido
                puntaje_total += (64 - turnos) * 0.1
            elif resultado == 'Empate':
                puntaje_total += 1
            else:
                # Perdió
                puntaje_total += 0
                
        individuo.fitness = puntaje_total
        return puntaje_total
