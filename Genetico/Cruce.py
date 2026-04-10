import random
from Cromosoma import Cromosoma

class Cruce:
    @staticmethod
    def cruzar(p1, p2):
        """Cruce uniforme: cada gen tiene 50% de probabilidad de venir de p1 o p2"""
        pesos_h1 = {}
        pesos_h2 = {}
        
        for key in p1.pesos.keys():
            if random.random() < 0.5:
                pesos_h1[key] = p1.pesos[key]
                pesos_h2[key] = p2.pesos[key]
            else:
                pesos_h1[key] = p2.pesos[key]
                pesos_h2[key] = p1.pesos[key]
                
        return Cromosoma(pesos_h1), Cromosoma(pesos_h2)
