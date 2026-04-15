import random
from Cromosoma import Cromosoma

class Mutacion:
    @staticmethod
    def mutar(individuo, prob=0.25):
        """Muta genes de un individuo. prob=0.25 da más diversidad para escapar óptimos locales."""
        if random.random() > prob:
            return individuo
        
        nuevos_pesos = individuo.pesos.copy()
        
        # Mutar 2 genes a la vez (más diversidad que mutar solo 1)
        genes_a_mutar = random.sample(list(nuevos_pesos.keys()), k=min(2, len(nuevos_pesos)))
        
        for gen_a_mutar in genes_a_mutar:
            variacion = random.uniform(0.75, 1.35)  # +/-35% en lugar de +/-20%
            nuevo_valor = int(nuevos_pesos[gen_a_mutar] * variacion)
            
            # Mutación drástica con 15% de probabilidad (exploración agresiva)
            if random.random() < 0.15:
                limite_max = 1000 if gen_a_mutar == 'linea_3' else 150
                nuevo_valor = random.randint(1, limite_max)
                
            nuevos_pesos[gen_a_mutar] = max(1, nuevo_valor)
        
        return Cromosoma(nuevos_pesos)
