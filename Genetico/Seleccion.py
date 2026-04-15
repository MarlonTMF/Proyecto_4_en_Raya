import random

class Seleccion:
    @staticmethod
    def seleccionar(poblacion, k=4):
        """Selección por torneo: elige k individuos al azar y devuelve el mejor.
        k=4 sobre población de 20 da mayor presión selectiva que k=3."""
        torneo = random.sample(poblacion, k)
        return max(torneo, key=lambda ind: ind.fitness)
