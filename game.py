import numpy as np

class TicTacToe3D:
    def __init__(self):
        self.board = np.zeros((3, 3, 3), dtype=int)  # 0: vacío, 1: jugador1, 2: jugador2
        self.current_player = 1

    def make_move(self, layer, row, col):
        if self.board[layer, row, col] == 0:
            self.board[layer, row, col] = self.current_player
            self.current_player = 3 - self.current_player  # Alterna entre 1 y 2
            return True
        return False

    def check_winner(self):
        # Verifica líneas en capas, filas, columnas y diagonales (simplificado)
        for i in range(3):
            for j in range(3):
                if np.all(self.board[i, j, :] == 1) or np.all(self.board[i, :, j] == 1) or np.all(self.board[:, i, j] == 1):
                    return 1
                if np.all(self.board[i, j, :] == 2) or np.all(self.board[i, :, j] == 2) or np.all(self.board[:, i, j] == 2):
                    return 2
        # Diagonales simples (puedes expandir)
        if np.all(np.diag(self.board[:, :, 0]) == 1) or np.all(np.diag(self.board[0, :, :]) == 1):
            return 1
        if np.all(np.diag(self.board[:, :, 0]) == 2) or np.all(np.diag(self.board[0, :, :]) == 2):
            return 2
        if np.count_nonzero(self.board) == 27:
            return 0  # Empate
        return -1  # Continúa

    def print_board(self):
        for layer in range(3):
            print(f"Capa {layer}:")
            for row in range(3):
                print(self.board[layer, row])
            print()