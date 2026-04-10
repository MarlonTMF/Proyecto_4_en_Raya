import random
from Cromosoma import Cromosoma

class Poblacion:
    @staticmethod
    def generar(tamano):
        poblacion = []
        for _ in range(tamano):
            # Pesos aleatorios con sentido común (línea 3 > línea 2...)
            pesos_aleatorios = {
                'linea_1': random.randint(1, 10),
                'linea_2': random.randint(10, 100),
                'linea_3': random.randint(100, 1000),
                'centro': random.randint(1, 50),
                'esquina': random.randint(1, 40),
                'cara': random.randint(1, 20),
                'arista': random.randint(1, 15)
            }
            poblacion.append(Cromosoma(pesos_aleatorios))
        return poblacion
