import socket
import sys

HOST = "0.0.0.0"
PORT = 50000


def iniciar_servidor(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Servidor UDP escuchando en {host}:{port}...")

    # Diccionario para asociar cada dirección (IP, puerto) con un nombre de usuario
    usuarios = {}

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            mensaje = data.decode("utf-8")

            # 1. Si la dirección es nueva, el primer paquete es su nombre de usuario
            if addr not in usuarios:
                usuarios[addr] = mensaje
                print(f"Se ha conectado el usuario: {mensaje}")

            # 2. Señal explícita de desconexión enviada por el cliente
            elif mensaje == "__DISCONNECT__":
                print(f"El usuario '{usuarios[addr]}' se ha desconectado.")
                del usuarios[addr]

            # 3. Mensaje normal: formatear e retransmitir (broadcast) a los demás
            else:
                mensaje_formateado = f"{usuarios[addr]}: {mensaje}"
                print(mensaje_formateado)

                for cliente_addr in usuarios:
                    if cliente_addr != addr:
                        server_socket.sendto(
                            mensaje_formateado.encode("utf-8"), cliente_addr
                        )
        except Exception as e:
            print(f"Error en el servidor: {e}")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    iniciar_servidor(HOST, port)
