from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class GhostCube(Button):
    def __init__(self, position, board_pos, parent_ui):
        super().__init__(
            parent=parent_ui,
            position=position,
            model='cube',
            texture=None,
            color=color.rgba(0, 1, 1, 0.02), # Casi invisible por defecto
            highlight_color=color.rgba(0, 1, 1, 0.4),
            pressed_color=color.rgba(1, 1, 0, 0.5),
            scale=0.9,
            collider='box'
        )
        # Borde de la casilla para ver la rejilla
        self.outline = Entity(
            parent=self,
            model='cube',
            mode='wireframe',
            color=color.rgba(0, 1, 1, 0.1),
            scale=1.0
        )
        self.board_pos = board_pos
        self.parent_ui = parent_ui

    def on_click(self):
        self.parent_ui.on_square_clicked(self.board_pos)

class Piece(Entity):
    def __init__(self, position, player, parent_board):
        # Humano (X) es ahora Azul Oscuro, IA (O) es Magenta
        color_val = color.blue.tint(-0.5) if player == 'X' else color.magenta
        model_type = 'sphere' # Ambos son esferas para un look más moderno
        super().__init__(
            parent=parent_board,
            model=model_type,
            color=color_val,
            position=position,
            scale=0.7,
            alpha=1.0
        )
        # Adding some glow effect simulation
        self.glow = Entity(
            parent=self,
            model=model_type,
            color=color_val,
            scale=1.2,
            alpha=0.3,
            add_to_scene_entities=True
        )

class TableroUI(Entity):
    def __init__(self, n=4, on_move_callback=None):
        super().__init__()
        self.n = n
        self.on_move_callback = on_move_callback
        self.cubes = {}
        self.pieces = {}
        self.selector_pos = [1, 1, 4] # x, y, z starting point
        
        self.scale = 1.2 # Tablero un poco más grande
        
        # Cage/Wireframe to define the 3D volume
        self.cage = Entity(
            parent=self,
            model='cube',
            mode='wireframe',
            color=color.rgba(1, 1, 1, 0.2),
            scale=n,
        )
        
        # Grid setup
        offset = (n - 1) / 2
        for z in range(1, n + 1):
            # Líneas guía de nivel
            Entity(
                parent=self,
                model='quad',
                color=color.rgba(1, 1, 1, 0.05),
                scale=n,
                position=(0, z - 1 - offset, 0),
                rotation_x=90
            )
            
            for x in range(1, n + 1):
                for y in range(1, n + 1):
                    pos = (x - 1 - offset, y - 1 - offset, z - 1 - offset)
                    cube = GhostCube(position=pos, board_pos=(x, y, z), parent_ui=self)
                    self.cubes[(x, y, z)] = cube

        # Cursor de teclado (Más pequeño para que no sobresalga)
        self.cursor = Entity(
            parent=self,
            model='cube',
            mode='wireframe',
            color=color.yellow,
            scale=0.9, # Reducido según petición
            visible=False
        )
        # Efecto de pulso en el cursor
        self.cursor.animate_scale(0.95, duration=0.5, loop=True, curve=curve.linear)
        
        self.rotation_speed = 150


    def update(self):
        # Rotation logic: drag mouse on background
        if mouse.left and not mouse.hovered_entity:
            self.rotation_y -= mouse.velocity[0] * self.rotation_speed
            self.rotation_x += mouse.velocity[1] * self.rotation_speed

    def on_square_clicked(self, board_pos):
        if self.on_move_callback:
            self.on_move_callback(board_pos)

    def update_board(self, tablero_dict):
        # Place pieces for new entries
        for pos, player in tablero_dict.items():
            if pos not in self.pieces:
                cube = self.cubes[pos]
                cube.visible = False
                self.pieces[pos] = Piece(cube.position, player, self)

    def move_selector(self, dx, dy, dz):
        self.cursor.visible = True
        self.selector_pos[0] = max(1, min(self.n, self.selector_pos[0] + dx))
        self.selector_pos[1] = max(1, min(self.n, self.selector_pos[1] + dy))
        self.selector_pos[2] = max(1, min(self.n, self.selector_pos[2] + dz))
        self.cursor.position = self.cubes[tuple(self.selector_pos)].position

    def input(self, key):
        # Movimiento en plano XY
        if key == 'left arrow' or key == 'a': self.move_selector(-1, 0, 0)
        if key == 'right arrow' or key == 'd': self.move_selector(1, 0, 0)
        if key == 'up arrow' or key == 'w': self.move_selector(0, 1, 0)
        if key == 'down arrow' or key == 's': self.move_selector(0, -1, 0)
        
        # Movimiento de Capas (Z) - Variantes para comodidad
        if key == 'q' or key == 'page up' or key == '+': self.move_selector(0, 0, 1)
        if key == 'e' or key == 'page down' or key == '-': self.move_selector(0, 0, -1)
        
        # Colocar pieza
        if key == 'enter' or key == 'space':
            self.on_square_clicked(tuple(self.selector_pos))


