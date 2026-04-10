import random

class Seleccion:
    @staticmethod
    def seleccionar(poblacion, k=3):
        """Selección por torneo: elige k individuos al azar y devuelve el mejor"""
        torneo = random.sample(poblacion, k)
        return max(torneo, key=lambda ind: ind.fitness)
