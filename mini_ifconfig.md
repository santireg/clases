# Análisis del Comando ifconfig

`ifconfig` (*Interface Configuration*) es una herramienta de consola en sistemas Unix/Linux utilizada para inspeccionar, configurar y administrar las interfaces de red del sistema (placas Ethernet, Wi-Fi, interfaces virtuales, etc.).

## Parámetros Comunes

* **`ifconfig` (sin parámetros):** Muestra exclusivamente las interfaces de red que están activas.
* **`ifconfig -a`:** Muestra **todas** las interfaces del sistema, incluyendo aquellas que están desactivadas (*DOWN*).
* **`ifconfig <interfaz>` (ej. `ifconfig eth0`):** Filtra e imprime la información de una interfaz específica.
* **`ifconfig <interfaz> up / down`:** Permite encender (`up`) o apagar (`down`) administrativamente una placa de red.
* **`ifconfig <interfaz> <IP> netmask <MÁSCARA>`:** Permite asignar manualmente una IP estática y máscara a la interfaz.

---

## Análisis en profundidad de los Campos

| Campo | Descripción |
| :--- | :--- |
| **`inet`** | Dirección IPv4 asignada actualmente a la interfaz. |
| **`netmask`** | Máscara de subred (delimita qué porción de la IP pertenece a la red y cuál a los hosts). |
| **`broadcast`** | Dirección IP de difusión (usada para enviar paquetes a todos los equipos de la subred simultáneamente). |
| **`inet6`** | Dirección IPv6 asignada, indicando su prefijo y el alcance de red (*scope*). |
| **`ether` / `HWaddr`** | Dirección MAC (*Media Access Control*), el identificador físico único grabado en el chip de la placa de red. |
| **`RX packets`** | Muestra el total de paquetes y bytes **recibidos** (*Received*) por la interfaz desde el último reinicio. |
| **`TX packets`** | Muestra el total de paquetes y bytes **transmitidos** (*Transmitted*) por la interfaz hacia la red. |
| **`errors`** | Paquetes defectuosos o corruptos recibidos/enviados (suele indicar fallas en el cable o interferencias). |
| **`dropped`** | Paquetes descartados por el sistema operativo debido a falta de memoria o búferes llenos. |
| **`collisions`** | Número de colisiones detectadas al transmitir (común en redes Ethernet antiguas con *hubs*). |

---

## Banderas (Flags) y Conceptos Clave

* **`UP`:** La interfaz está habilitada administrativamente por el sistema operativo.
* **`RUNNING`:** La interfaz tiene vínculo físico activo (el cable Ethernet está enchufado o el Wi-Fi está asociado) y está lista para transferir datos.
* **`LOOPBACK` (`lo`):** Interfaz virtual para comunicaciones internas del equipo local (`127.0.0.1`). No envía tráfico a la red exterior.
* **`MULTICAST`:** Indica que la interfaz soporta el envío de paquetes *multicast* a grupos específicos de hosts.
* **`MTU` (*Maximum Transmission Unit*):** Define el tamaño máximo (en bytes) que puede tener un paquete para ser transmitido por esta interfaz sin ser fragmentado (el valor predeterminado estándar es `1500` bytes).
