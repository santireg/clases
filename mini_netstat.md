# Análisis del Comando Netstat y Parámetros -tuna

`netstat` (*Network Statistics*) es una herramienta de consola para inspeccionar las conexiones de red activas, puertos abiertos, tablas de enrutamiento y estadísticas de las placas de red.

## Impacto de los Parámetros (-tuna)

* **`-t` (TCP):** Muestra únicamente los sockets que utilizan el protocolo TCP.
* **`-u` (UDP):** Muestra únicamente los sockets del protocolo UDP.
* **`-n` (Numeric):** Fuerza a `netstat` a mostrar direcciones IP y números de puerto de forma numérica (ej. `127.0.0.1:80`). Evita la resolución DNS de nombres de host y la traducción de nombres de servicios (evita convertir `80` a `http`), acelerando la respuesta del comando.
* **`-a` (All):** Muestra todos los sockets, tanto los que están en escucha (`LISTEN`) como los activos. Por defecto, `netstat` oculta los puertos que están escuchando a la espera de conexiones.

---

## Comportamiento: Sin parámetros vs. `netstat -tuna`

* **Sin parámetros:** Muestra solo conexiones activas de red, añade todos los sockets de dominio UNIX (comunicación interna entre procesos del sistema operativo) e intenta resolver dominios por DNS, generando demoras si no hay internet o el DNS es lento.
* **Con `-tuna`:** Oculta los sockets UNIX, incluye los puertos a la espera de conexión, filtra estrictamente a red (TCP/UDP) y responde de forma instantánea al no consultar DNS.

---

## Análisis en profundidad de las Columnas

| Columna | Descripción |
| :--- | :--- |
| **Proto** | Protocolo de red en uso: `tcp`, `udp`, `tcp6`, `udp6`. |
| **Recv-Q** | **Receive Queue:** Bytes recibidos por la pila de red del Kernel que la aplicación local **aún no ha leído** mediante `recv()`. Si este valor se mantiene alto de forma constante, la aplicación local está saturada o trabada. |
| **Send-Q** | **Send Queue:** Bytes enviados por la aplicación local que la red **aún no ha podido entregar o no han recibido confirmación (ACK)** del receptor. Un número alto continuo suele indicar congestión de red, alta latencia o pérdida de paquetes. |
| **Local Address** | IP y puerto de la máquina local. `0.0.0.0:5000` significa que escucha en **todas** las interfaces de red del equipo. `127.0.0.1:5000` indica que solo acepta tráfico interno local. |
| **Foreign Address** | IP y puerto del dispositivo remoto conectado. Si figura `*:*` o `0.0.0.0:*`, indica que el puerto está libre para recibir cualquier conexión externa. |
| **State** | Estado del socket dentro del ciclo de vida de la conexión. En UDP este campo siempre aparece vacío porque es un protocolo sin estado (*stateless*). |

---

## Principales Estados TCP (Columna State)

* **LISTEN:** El servidor está con el socket abierto esperando a que algún cliente inicie una conexión.
* **ESTABLISHED:** Existe una conexión bidireccional de datos abierta y activa entre ambas máquinas.
* **SYN_SENT / SYN_RECV:** La conexión está en pleno proceso de negociación inicial (*3-way handshake*).
* **CLOSE_WAIT:** El equipo remoto cerró la conexión; el proceso local debe procesar el cierre de su socket.
* **TIME_WAIT:** El socket local fue cerrado pero la pila de red espera unos segundos para garantizar que no queden paquetes perdidos navegando por la red antes de liberar el puerto.
