import socket

HOST = input("Ingresa la IP del servidor: ")
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    msg = client.recv(1024).decode()
    print(msg)
    if "Ganador" in msg:
        break
    move = input("Tu movimiento (layer row col): ")
    client.sendall(move.encode())

client.close()