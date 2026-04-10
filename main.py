from collections import namedtuple

from AgenteTresEnRaya import AgenteTresEnRaya, ElEstado
from Tablero import Tablero
from HumanoTresEnRaya import HumanoTresEnRaya

if __name__ == "__main__":
    luis = HumanoTresEnRaya(4)

    juan = AgenteTresEnRaya(4, altura=3)
    juan.tecnica = "fun_eval"
    tablero = Tablero(4)
    #ElEstado = namedtuple('ElEstado', 'jugador, get_utilidad, tablero, movidas')
    #a = ElEstado(jugador='X', get_utilidad=0, tablero={(2,2):'X',(1,1):'O', (3,3):'O'}, movidas=[])

    # print(juan.funcion_evaluacion(a))
    tablero.insertar(luis)
    tablero.insertar(juan)
    
    tablero.run()
