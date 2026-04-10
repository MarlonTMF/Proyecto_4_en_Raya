class Cromosoma:
    def __init__(self, pesos):
        # pesos es un diccionario de la forma {'linea_1': 5, 'centro': 30, ...}
        self.pesos = pesos
        self.fitness = 0

    def __repr__(self):
        return f"<Cromosoma Fitness={self.fitness} Pesos={self.pesos}>"
