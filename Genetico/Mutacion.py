import random
from Cromosoma import Cromosoma

class Mutacion:
    @staticmethod
    def mutar(individuo, prob=0.1):
        """Muta algunos genes de un individuo agregando ruido"""
        if random.random() > prob:
            return individuo
        
        nuevos_pesos = individuo.pesos.copy()
        
        # Elegir una clave al azar para mutar
        gen_a_mutar = random.choice(list(nuevos_pesos.keys()))
        
        # Agregar variación (ej. +/- 20%)
        variacion = random.uniform(0.8, 1.2)
        nuevo_valor = int(nuevos_pesos[gen_a_mutar] * variacion)
        
        # Ocasionalmente mutar drásticamente (exploración)
        if random.random() < 0.2:
            limite_max = 1000 if gen_a_mutar == 'linea_3' else 100
            nuevo_valor = random.randint(1, limite_max)
            
        nuevos_pesos[gen_a_mutar] = max(1, nuevo_valor) # Evitar ceros o negativos
        
        return Cromosoma(nuevos_pesos)
