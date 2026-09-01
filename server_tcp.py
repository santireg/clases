import socket
import threading

HOST = "192.168.1.50"
PORT = 50000

clientes = []
lock = threading.Lock()


def broadcast(mensaje, socket_origen):
    with lock:
        for cliente in clientes:
            if cliente != socket_origen:
                try:
                    cliente.sendall(mensaje.encode("utf-8"))
                except:
                    pass


def manejar_cliente(connection):
    nombre = ""
    try:
        nombre = connection.recv(1024).decode("utf-8").strip()
        if nombre:
            print(f"Se ha conectado el usuario: {nombre}")
            with lock:
                clientes.append(connection)

        while True:
            data = connection.recv(1024)
            if not data:
                break
            mensaje_formateado = f"{nombre}: {data.decode('utf-8')}"
            print(mensaje_formateado)
            broadcast(mensaje_formateado, connection)
    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        with lock:
            if connection in clientes:
                clientes.remove(connection)
        if nombre:
            print(f"El usuario '{nombre}' se ha desconectado.")
        connection.close()


def iniciar_servidor():
    acceptor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    acceptor.bind((HOST, PORT))
    acceptor.listen()
    print(f"Socket TCP escuchando en {HOST}:{PORT}...")

    while True:
        connection, addr = acceptor.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(connection,))
        hilo_cliente.start()


if __name__ == "__main__":
    iniciar_servidor()
