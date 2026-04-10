import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Genetico.Simulador import Simulador
from AgenteTresEnRaya import AgenteTresEnRaya
from AgenteAleatorio import AgenteAleatorio

def correr_torneo(agente1, agente2, partidas=100, nombre_a1='Agente 1', nombre_a2='Agente 2'):
    victorias_a1 = 0
    victorias_a2 = 0
    empates = 0
    
    print(f"\nIniciando torneo: {nombre_a1} vs {nombre_a2} ({partidas} partidas)")
    for i in range(partidas):
        if i % 10 == 0:
            print(f"Progreso: {i}/{partidas}...")
            
        # Alternar quién empieza
        if i % 2 == 0:
             agente1.jugador_id = 'X'
             agente2.jugador_id = 'O'
             resultado, turnos = Simulador.jugar(agente1, agente2)
             gana_a1 = 'X'
             gana_a2 = 'O'
        else:
             agente1.jugador_id = 'O'
             agente2.jugador_id = 'X'
             resultado, turnos = Simulador.jugar(agente2, agente1)
             gana_a1 = 'O'
             gana_a2 = 'X'
             
        if resultado == gana_a1:
            victorias_a1 += 1
        elif resultado == gana_a2:
            victorias_a2 += 1
        else:
            empates += 1
            
    # Imprimir Tabla
    print(f"\n{'-'*60}")
    print(f"RESULTADOS: {nombre_a1}")
    print(f"{'-'*60}")
    print(f"Victorias: {victorias_a1}")
    print(f"Derrotas : {victorias_a2}")
    print(f"Empates  : {empates}")
    print(f"Tasa Vic : {victorias_a1 / partidas:.2f}")
    print(f"{'-'*60}")

def main():
    # Asumimos estos pesos base (manuales)
    pesos_manuales = {
        'linea_1': 5, 'linea_2': 50, 'linea_3': 500,
        'centro': 30, 'esquina': 25, 'cara': 10, 'arista': 5
    }
    
    # Simula pesos del AG (puedes reemplazar con los mejores que arroje main_genetico.py)
    pesos_ag = {
        'linea_1': 1, 'linea_2': 20, 'linea_3': 925,
        'centro': 49, 'esquina': 18, 'cara': 7, 'arista': 7
    }
    
    print(" === EVALUACIÓN FINAL DE RENDIMIENTO (FASE 4) === ")
    
    # Prueba 1: GA vs Aleatorio
    agente_ag = AgenteTresEnRaya(n=4, altura=1, pesos_heuristica=pesos_ag)
    agente_rand = AgenteAleatorio()
    correr_torneo(agente_ag, agente_rand, 100, "Genético (Mejor)", "Aleatorio")
    
    # Prueba 2: GA vs Manual
    agente_manual = AgenteTresEnRaya(n=4, altura=1, pesos_heuristica=pesos_manuales)
    correr_torneo(agente_ag, agente_manual, 100, "Genético (Mejor)", "Pesos Manuales")

if __name__ == "__main__":
    main()
