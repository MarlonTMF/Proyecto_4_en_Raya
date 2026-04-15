from Poblacion import Poblacion
from Fitness import Fitness
from Seleccion import Seleccion
from Cruce import Cruce
from Mutacion import Mutacion
import time

def main():
    print("Iniciando optimización por Algoritmo Genético (Modo Headless)...")
    
    TAMANO_POBLACION = 20
    GENERACIONES = 25  # Ronda 2: más generaciones para escapar óptimo local
    
    poblacion = Poblacion.generar(TAMANO_POBLACION)
    historial_mejor_fitness = []
    historial_promedio_fitness = []
    historial_peor_fitness = []
    historial_tiempos = []
    matriz_dispersa_todas_las_puntuaciones = [] # Para el gráfico de nube
    
    metricas_informe = {
        "tamano_poblacion": TAMANO_POBLACION,
        "total_generaciones": GENERACIONES,
        "generaciones_detalle": []
    }
    
    tiempo_inicio_global = time.time()
    
    tiempos_por_generacion = []  # Para calcular ETA global
    
    for g in range(GENERACIONES):
        start_time = time.time()
        
        # Calcular fitness (solo los nuevos, los élite ya tienen fitness)
        individuos_a_evaluar = [ind for ind in poblacion if ind.fitness == 0]
        total_a_evaluar = len(individuos_a_evaluar)
        tiempo_inicio_eval = time.time()

        for idx, ind in enumerate(individuos_a_evaluar):
            Fitness.calcular(ind)
            
            # Imprimir UNA sola línea a mitad de la evaluación (sin spam)
            if total_a_evaluar > 4 and (idx + 1) == total_a_evaluar // 2:
                transcurrido = time.time() - tiempo_inicio_eval
                eta_gen = transcurrido * 2  # Estimado: faltan otros 50%
                pct_global = (g / GENERACIONES) * 100
                print(f"  ⏳ Mitad Gen {g+1}... | Avance global: {pct_global:.0f}% | ETA esta gen: ~{eta_gen/60:.1f} min")

        # Ordenar población por fitness
        poblacion.sort(key=lambda x: x.fitness, reverse=True)
        mejor_gen = poblacion[0]
        todos_los_fitness = [ind.fitness for ind in poblacion]
        promedio_fitness = sum(todos_los_fitness) / len(poblacion)
        peor_fitness = poblacion[-1].fitness
        elapsed = time.time() - start_time
        tiempos_por_generacion.append(elapsed)
        
        # ETA global basado en promedio real de generaciones anteriores
        prom_seg_gen = sum(tiempos_por_generacion) / len(tiempos_por_generacion)
        gens_restantes = GENERACIONES - (g + 1)
        eta_global_min = (prom_seg_gen * gens_restantes) / 60
        pct_global = ((g + 1) / GENERACIONES) * 100
        
        print(f"\n{'='*55}")
        print(f"  GEN {g+1}/{GENERACIONES} | Avance: {pct_global:.0f}% | ETA restante: ~{eta_global_min:.1f} min")
        print(f"  Fitness → Mejor: {mejor_gen.fitness:.2f} | Prom: {promedio_fitness:.2f} | Peor: {peor_fitness:.2f}")
        print(f"  Tiempo gen: {elapsed:.1f}s | Transcurrido total: {(time.time()-tiempo_inicio_global)/60:.1f} min")
        print(f"{'='*55}\n")
        
        historial_mejor_fitness.append(mejor_gen.fitness)
        historial_promedio_fitness.append(promedio_fitness)
        historial_peor_fitness.append(peor_fitness)
        historial_tiempos.append(elapsed)
        matriz_dispersa_todas_las_puntuaciones.append(todos_los_fitness)
        
        # Guardamos TODO en la memoria para el reporte final JSON
        metricas_informe["generaciones_detalle"].append({
            "generacion": g + 1,
            "mejor_fitness": mejor_gen.fitness,
            "promedio_fitness": promedio_fitness,
            "peor_fitness": peor_fitness,
            "todos_los_fitness_raw": todos_los_fitness,
            "pesos_del_ganador": mejor_gen.pesos,
            "tiempo_segundos": elapsed
        })
        
        nueva_poblacion = []
        
        # Elitismo reducido: solo el MEJOR sobrevive directamente.
        # Antes eran 2 élites → el campeón nunca era desafiado.
        # Con 1 élite hay más espacio para hijos con mutaciones frescas.
        nueva_poblacion.append(poblacion[0])
        
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
    
    tiempo_total_ejecucion = time.time() - tiempo_inicio_global
    metricas_informe["tiempo_total_segundos"] = tiempo_total_ejecucion
    metricas_informe["ganador_absoluto"] = {
        "fitness": ganador_absoluto.fitness,
        "pesos": ganador_absoluto.pesos
    }
    
    print("\n---------------- GANADOR ABSOLUTO ----------------")
    print(f"Fitness Máximo Alcanzado: {ganador_absoluto.fitness:.2f}")
    print(f"Tiempo total de entrenamiento: {tiempo_total_ejecucion/60:.2f} minutos")
    print("Pesos Recomendados para AgenteTresEnRaya:")
    import json
    print(json.dumps(ganador_absoluto.pesos, indent=4))
    
    # Exportar métricas a archivo (Excelente para anexos de informes)
    archivo_metricas = "metricas_entrenamiento_genetico.json"
    try:
        with open(archivo_metricas, 'w', encoding='utf-8') as f:
            json.dump(metricas_informe, f, indent=4)
        print(f"\n[INFO] Métricas completas exportadas en: {archivo_metricas}")
    except Exception as e:
        print(f"\n[ERROR] No se pudo guardar el archivo JSON de métricas: {e}")
    
    # ===== SECCIÓN DE GRÁFICAS =====
    try:
        import matplotlib.pyplot as plt
        
        # Gráfica 1: Líneas de Evolución Clásica
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, GENERACIONES + 1), historial_mejor_fitness, marker='o', linestyle='-', color='b', label='Mejor Fitness')
        plt.plot(range(1, GENERACIONES + 1), historial_promedio_fitness, marker='x', linestyle='--', color='g', label='Fitness Promedio')
        plt.plot(range(1, GENERACIONES + 1), historial_peor_fitness, marker='v', linestyle=':', color='r', label='Peor Fitness (Basura podada)')
        plt.title('Evolución de las Líneas de Sangre del Algoritmo Genético')
        plt.xlabel('Generaciones')
        plt.ylabel('Puntuación Fitness')
        plt.legend()
        plt.grid(True)
        plt.savefig('grafica_1_evolucion_lineas.png')
        plt.close()
        
        # Gráfica 2: Nube de Dispersión (Toda la población visible a la vez)
        plt.figure(figsize=(10, 5))
        for gen in range(GENERACIONES):
            # Pintamos todos los puntos individuales en cada columna X=gen
            y_puntos = matriz_dispersa_todas_las_puntuaciones[gen]
            x_puntos = [gen + 1] * len(y_puntos)
            plt.scatter(x_puntos, y_puntos, color='purple', alpha=0.5, s=20)
        
        plt.plot(range(1, GENERACIONES + 1), historial_mejor_fitness, linestyle='-', color='black', label='Límite Máximo del Fitness')
        plt.title('Nube Evolutiva: Dispersión Genética de todos los Individuos')
        plt.xlabel('Generación')
        plt.ylabel('Fitness (Inteligencia)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig('grafica_2_nube_poblacion.png')
        plt.close()
        
        # Gráfica 3: Rendimiento de Computación (Tiempo CPU)
        plt.figure(figsize=(10, 5))
        plt.bar(range(1, GENERACIONES + 1), historial_tiempos, color='orange')
        plt.title('Coste de Cómputo CPU por Generación Evaluada')
        plt.xlabel('Generaciones (Nivel)')
        plt.ylabel('Tiempo consumido (Segundos)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('grafica_3_tiempos_cpu.png')
        plt.close()
        
        print("\n[ÉXITO] Se generaron automáticamente 3 gráficas profesionales avanzadas como archivos .png para tu informe.")
        
    except ImportError:
        print("\n[INFO] No se pudo generar gráficas porque matplotlib no está instalado (pip install matplotlib).")

if __name__ == "__main__":
    main()
