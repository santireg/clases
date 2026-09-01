import socket
import sys
import threading


def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Imprime el mensaje recibido y restaura el prompt de entrada
            print(f"\n{data.decode('utf-8')}\n> ", end="")
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            break


def iniciar_cliente(host, port):
    nombre = input("Ingresa tu nombre de usuario: ").strip()
    while not nombre:
        nombre = input("El nombre no puede estar vacío. Ingresa tu usuario: ").strip()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Enviar el nombre de usuario al conectar
    client_socket.sendall(nombre.encode("utf-8"))
    print(
        "Conectado al servidor. Escribe un mensaje y presiona Enter (Escribe 'X' para salir):"
    )

    # Hilo en segundo plano para escuchar difusiones del servidor
    hilo_escucha = threading.Thread(
        target=recibir_mensajes, args=(client_socket,), daemon=True
    )
    hilo_escucha.start()

    while True:
        mensaje = input("> ")
        if mensaje == "X":
            print("Desconectando del servidor...")
            break

        client_socket.sendall(mensaje.encode("utf-8"))

    client_socket.close()


if __name__ == "__main__":
    # Validar que se hayan pasado exactamente 2 argumentos
    if len(sys.argv) != 3:
        print("Uso correcto: python3 archivo.py <puerto> <ip>")
        sys.exit(1)

    try:
        # sys.argv[1] toma el puerto y sys.argv[2] toma la ip
        port = int(sys.argv[1])
        host = sys.argv[2]
        iniciar_cliente(host, port)
    except ValueError:
        print("Error: El puerto debe ser un número entero.")
        sys.exit(1)
