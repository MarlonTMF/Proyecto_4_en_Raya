from ursina import *
from GUI3D import TableroUI
from AgenteTresEnRaya import AgenteTresEnRaya
from HumanoTresEnRaya import HumanoTresEnRaya
from Tablero import Tablero

# Configuración de Ursina
app = Ursina(title="3D Tic-Tac-Toe (4x4x4) - Premium Edition")
window.fps_counter.enabled = False
window.exit_button.visible = False

# Inicialización de la lógica del juego
n = 4
tablero_logico = Tablero(n)
huemano = HumanoTresEnRaya(n, jugador='X')
agente_ia = AgenteTresEnRaya(n, altura=3, jugador='O')
agente_ia.tecnica = "fun_eval"

tablero_logico.insertar(huemano)
tablero_logico.insertar(agente_ia)

# Inicialización de la interfaz 3D
def on_player_move(pos):
    # Solo permitimos el movimiento si es el turno del humano y el juego no ha terminado
    if not huemano.esta_habilitado() or tablero_logico.juegoActual.jugador != 'X':
        return
    
    if pos in tablero_logico.juegoActual.movidas:
        huemano.movida_pendiente = pos

ui = TableroUI(n=n, on_move_callback=on_player_move)
# Ángulo inicial isométrica
ui.rotation = (25, -45, 0)

# Indicador de Turno y Nivel
turno_text = Text(text="Esperando tu jugada...", position=(-0.85, 0.45), scale=1.5, color=color.cyan)
nivel_text = Text(text="Nivel Actual: 4", position=(-0.85, 0.38), scale=1.2, color=color.yellow)

# Panel de Ayuda
help_text = Text(
    text="CONTROLES:\n"
         "- Arrastrar Fondo: Rotar Cubo\n"
         "- WASD: Mover en Capa\n"
         "- Q/E o PgUp/PgDn: Cambiar de Nivel\n"
         "- Enter/Espacio: Jugar",
    position=(0.55, 0.45),
    scale=0.8,
    color=color.gray
)

# Botón de Reiniciar Vista
reset_button = Button(
    text='Reiniciar Vista',
    color=color.rgba(0,0,0,0.5),
    scale=(0.15, 0.05),
    position=(0.75, -0.45),
    on_click=lambda: setattr(ui, 'rotation', (25, -45, 0))
)

# Cámara Estándar
camera.position = (0, 0, -18) # Un poco más lejos para ver todo
camera.fov = 60

def update():
    # El bucle de Ursina reemplaza al Entorno.run() bloquearte
    if not tablero_logico.finalizar():
        # Actualizar indicadores
        if tablero_logico.juegoActual.jugador == 'X':
            turno_text.text = "TU TURNO (X)"
            turno_text.color = color.cyan
        else:
            turno_text.text = "TURNO IA (O)..."
            turno_text.color = color.magenta
            
        nivel_text.text = f"Nivel Actual: {ui.selector_pos[2]}"

        # Ejecutamos un paso de la evolución en cada frame
        tablero_logico.evolucionar()
        
        # Sincronizamos la UI con el estado lógico
        ui.update_board(tablero_logico.juegoActual.tablero)
    else:
        turno_text.enabled = False
        nivel_text.enabled = False
        # Fin del juego

        resul = tablero_logico.juegoActual.get_utilidad
        msg = "¡Empate!"
        if resul > 0: msg = "¡GANA X (HUMANO)!"
        elif resul < 0: msg = "¡GANA O (IA)!"
        
        # Título superior
        Text(text=msg, scale=3, position=(0, 0.45), origin=(0,0), background=True, color=color.yellow)


# Iluminación y Ambiente
Sky(color=color.black)
ambient_light = AmbientLight(color=color.rgba(1, 1, 1, 0.2))
directional_light = DirectionalLight(y=2, z=-3, rotation=(45, 45, 0), shadows=True)

app.run()

