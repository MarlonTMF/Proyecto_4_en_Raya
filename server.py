import socket
import threading
from game import TicTacToe3D

HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 12345

game = TicTacToe3D()
clients = []
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"Jugador conectado: {addr}")
    clients.append(conn)
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            # Procesa movimiento: formato "layer row col"
            parts = data.split()
            if len(parts) == 3:
                layer, row, col = map(int, parts)
                with lock:
                    if game.make_move(layer, row, col):
                        winner = game.check_winner()
                        response = f"Movimiento válido. Ganador: {winner}" if winner != -1 else "Movimiento válido"
                        for c in clients:
                            c.sendall(response.encode())
                    else:
                        conn.sendall("Movimiento invalido".encode('utf-8'))  # Cambiado para evitar caracteres no ASCII
        except:
            break
    conn.close()
    clients.remove(conn)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)  # Máximo 2 jugadores
    print(f"Servidor iniciado en {HOST}:{PORT}. Comparte tu IP local para que otros se conecten.")
    while len(clients) < 2:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()