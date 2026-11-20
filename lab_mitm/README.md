# Laboratorio MitM con Bettercap (Docker)

Entorno aislado para pruebas de ataques Man-in-the-Middle: ARP spoofing,
captura de credenciales HTTP y modificación de contenido HTTP.

## Requisitos
- Docker y Docker Compose

## Nodos y red (172.20.0.0/24, aislada)
| Nodo         | IP          | Rol                               |
|--------------|-------------|-----------------------------------|
| servidor-web | 172.20.0.10 | Login en HTTP (80) y HTTPS (443)  |
| victima      | 172.20.0.20 | Cliente al que se espia           |
| atacante     | 172.20.0.30 | Bettercap                         |

## Levantar el entorno
    docker compose up -d --build

## Prueba 1 - ARP spoofing + captura de credenciales HTTP
    docker compose exec atacante bettercap -iface eth0 -caplet /caplets/prueba1.cap
    docker compose exec victima curl -s http://172.20.0.10/login -d "usuario=paciente01&password=hospital1234"

## Prueba 2 - Modificacion de contenido HTTP
    docker compose exec atacante bettercap -iface eth0 -caplet /caplets/prueba2.cap
    docker compose exec victima curl -s http://172.20.0.10/

## Parar el entorno
    docker compose down