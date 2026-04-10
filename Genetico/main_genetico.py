from Poblacion import Poblacion
from Fitness import Fitness
from Seleccion import Seleccion
from Cruce import Cruce
from Mutacion import Mutacion

def main():
    print("Iniciando optimización por Algoritmo Genético (Modo Headless)...")
    
    TAMANO_POBLACION = 20
    GENERACIONES = 10
    
    poblacion = Poblacion.generar(TAMANO_POBLACION)
    historial_fitness = []
    
    for g in range(GENERACIONES):
        print(f"--- Generación {g+1}/{GENERACIONES} ---")
        
        # Calcular fitness de todos
        # Evaluamos solo a los que no tienen fitness calculado para ahorrar tiempo
        for ind in poblacion:
            if ind.fitness == 0:
                Fitness.calcular(ind)
                
        # Ordenar población por fitness de mayor a menor
        poblacion.sort(key=lambda x: x.fitness, reverse=True)
        mejor_gen = poblacion[0]
        
        # Imprimir métricas de la generación
        print(f"Mejor fitness de la Generación: {mejor_gen.fitness:.2f}")
        print(f"Mejores Pesos: {mejor_gen.pesos}\n")
        
        historial_fitness.append(mejor_gen.fitness)
        
        nueva_poblacion = []
        
        # Elitismo: Pasar los 2 mejores directamente
        nueva_poblacion.append(poblacion[0])
        nueva_poblacion.append(poblacion[1])
        
        # Llenar el resto
        while len(nueva_poblacion) < TAMANO_POBLACION:
            p1 = Seleccion.seleccionar(poblacion)
            p2 = Seleccion.seleccionar(poblacion)
            
            h1, h2 = Cruce.cruzar(p1, p2)
            
            h1 = Mutacion.mutar(h1)
            h2 = Mutacion.mutar(h2)
            
            nueva_poblacion.append(h1)
            if len(nueva_poblacion) < TAMANO_POBLACION:
                nueva_poblacion.append(h2)
                
        poblacion = nueva_poblacion

    print("\n[OK] Evolucion terminada.")
    
    # Calcular fitness final de los rezagados si los hay
    for ind in poblacion:
         if ind.fitness == 0:
             Fitness.calcular(ind)
             
    poblacion.sort(key=lambda x: x.fitness, reverse=True)
    ganador_absoluto = poblacion[0]
    
    print("\n---------------- GANADOR ABSOLUTO ----------------")
    print(f"Fitness Máximo Alcanzado: {ganador_absoluto.fitness:.2f}")
    print("Pesos Recomendados para AgenteTresEnRaya:")
    import json
    print(json.dumps(ganador_absoluto.pesos, indent=4))
    
    # Generar Gráfica de Convergencia
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, GENERACIONES + 1), historial_fitness, marker='o', linestyle='-', color='b')
        plt.title('Convergencia del Algoritmo Genético (Mejor Fitness por Generación)')
        plt.xlabel('Generación')
        plt.ylabel('Fitness Score')
        plt.grid(True)
        nombre_grafica = 'convergencia_AG.png'
        plt.savefig(nombre_grafica)
        print(f"\n[INFO] Gráfica de convergencia guardada como: {nombre_grafica}")
    except ImportError:
        print("\n[INFO] No se pudo generar la gráfica porque matplotlib no está instalado.")

if __name__ == "__main__":
    main()
