import pygame
import random
import requests
import sys
import time

pygame.init()

# --- Paso 1: Obtener game_id y seed ---
resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
if resposta.status_code == 200:
    resposta = resposta.json()
    game_id = resposta['game_id']
    random.seed(resposta['seed'])
    print("Game ID:", game_id)
else:
    print("Error al obtener game_id")
    sys.exit()

# --- Paso 2: Enviar progreso cada 5 segundos ---
INTERVALO = 5
ultimo_envio = time.time()
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    ahora = time.time()
    if ahora - ultimo_envio >= INTERVALO:
        # Datos simulados
        progreso = {
            "game_id": game_id,
            "data": {
                "score": random.randint(0, 100),
                "status": "en progreso"
            }
        }

        try:
            resposta = requests.post(
                "https://fun.codelearn.cat/hackathon/game/store_progress",
                json=progreso
            )
            print("Respuesta:", resposta.status_code)
            print("Contenido:", resposta.json())
        except Exception as e:
            print("Error:", e)
            print("Texto crudo:", resposta.text)

        ultimo_envio = ahora

    reloj.tick(60)

pygame.quit()
sys.exit()
