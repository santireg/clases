import socket
import sys
import threading


def recibir_mensajes(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            if not data:
                break
            print(f"\n{data.decode('utf-8')}\n> ", end="")
        except (OSError, ConnectionResetError):
            break


def iniciar_cliente(host, port):
    nombre = input("Ingresa tu nombre de usuario: ").strip()
    while not nombre:
        nombre = input("El nombre no puede estar vacío. Ingresa tu usuario: ").strip()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Registro: el primer datagrama le indica al servidor nuestro nombre
    client_socket.sendto(nombre.encode("utf-8"), (host, port))
    print(
        "Conectado (UDP). Escribe un mensaje y presiona Enter (Escribe 'X' para salir):"
    )

    # Hilo en segundo plano para escuchar difusiones entrantes
    hilo_escucha = threading.Thread(
        target=recibir_mensajes, args=(client_socket,), daemon=True
    )
    hilo_escucha.start()

    while True:
        mensaje = input("> ")
        if mensaje == "X":
            print("Desconectando del servidor...")
            # Enviar aviso de desconexión explícito (necesario en UDP por no tener conexión persistente)
            client_socket.sendto("__DISCONNECT__".encode("utf-8"), (host, port))
            break

        client_socket.sendto(mensaje.encode("utf-8"), (host, port))

    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso correcto: python3 cliente_udp.py <puerto> <ip>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        host = sys.argv[2]
        iniciar_cliente(host, port)
    except ValueError:
        print("Error: El puerto debe ser un número entero.")
        sys.exit(1)
