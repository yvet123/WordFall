import pygame
import random
import requests
import sys
import time

pygame.init()
AMPLADA = 1000
ALCADA_TOTAL = 600
ALCADA_JOC = 450
ALCADA_INFERIOR = ALCADA_TOTAL - ALCADA_JOC
CATEGORIES = ["NOM", "VERB", "ADJECTIU", "DETERMINANT", "ADVERBI"]
COLUMNES = len(CATEGORIES)
TAM_COLUMNA = AMPLADA // COLUMNES
FPS = 30
DURADA = 60

PARAULES = {
    "CAMINAR": "VERB",
    "TAULA": "NOM",
    "LLEIG": "ADJECTIU",
    "LLEGIR": "VERB",
    "GOS": "NOM",
    "VERMELL": "ADJECTIU",
    "NEN": "NOM",
    "TRIST": "ADJECTIU",
    "EL": "DETERMINANT",
    "LA": "DETERMINANT",
    "UN": "DETERMINANT",
    "MOLT": "ADVERBI",
    "RÀPIDAMENT": "ADVERBI",
    "BÉ": "ADVERBI"
}

NEGRE = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
VERMELL = (255, 70, 70)
FONT = pygame.font.SysFont("Trebuchet MS", 28)

pantalla = pygame.display.set_mode((AMPLADA, ALCADA_TOTAL))
pygame.display.set_caption("Tetris Gramatical en Català")

class Paraula:
    def __init__(self, text, categoria):
        self.text = text
        self.categoria = categoria
        self.columna = random.randint(0, COLUMNES - 1)
        self.y = 60

    def moure_esquerra(self):
        if self.columna > 0:
            self.columna -= 1

    def moure_dreta(self):
        if self.columna < COLUMNES - 1:
            self.columna += 1

    def caure(self, velocitat):
        self.y += velocitat

def dibuixar_cajita_paraula(pantalla, paraula, x, y):
    text_surface = FONT.render(paraula.text, True, NEGRE)
    ancho_text, alto_text = text_surface.get_size()
    margen_x = 12
    margen_y = 8
    rect = pygame.Rect(x, y, ancho_text + 2 * margen_x, alto_text + 2 * margen_y)
    pygame.draw.rect(pantalla, GRIS, rect, border_radius=6)
    pantalla.blit(text_surface, (x + margen_x, y + margen_y))

def dibuixar_tauler(paraula, punts, temps_restant):
    pantalla.fill(GRIS)

    # Dibujar columnas del juego
    for i, cat in enumerate(CATEGORIES):
        x = i * TAM_COLUMNA
        pygame.draw.rect(pantalla, NEGRE, (x, 0, TAM_COLUMNA, 450))
        pygame.draw.line(pantalla, BLANC, (x, 0), (x, 450), 3)
        etiqueta = FONT.render(cat, True, BLANC)
        pantalla.blit(etiqueta, (x + 10, 10))

    # Dibujar palabra actual
    if paraula:
        x = paraula.columna * TAM_COLUMNA + 20
        dibuixar_cajita_paraula(pantalla, paraula, x, paraula.y)

    # NUEVA zona inferior para mostrar tiempo y puntuación
    zona_info_y = 470
    pygame.draw.rect(pantalla, NEGRE, (0, zona_info_y, AMPLADA, ALCADA - zona_info_y))  # fondo zona info

    punts_txt = FONT.render(f"Punts: {punts}", True, BLANC)
    pantalla.blit(punts_txt, (20, zona_info_y + 20))
import pygame
import random
import requests
import sys
import time

pygame.init()
AMPLADA = 1000
ALCADA_TOTAL = 600
ALCADA_JOC = 450
ALCADA_INFO = ALCADA_TOTAL - ALCADA_JOC

CATEGORIES = ["NOM", "VERB", "ADJECTIU", "DETERMINANT", "ADVERBI"]
COLUMNES = len(CATEGORIES)
TAM_COLUMNA = AMPLADA // COLUMNES
FPS = 30
DURADA = 60

PARAULES = {
    "CAMINAR": "VERB",
    "TAULA": "NOM",
    "LLEIG": "ADJECTIU",
    "LLEGIR": "VERB",
    "GOS": "NOM",
    "VERMELL": "ADJECTIU",
    "NEN": "NOM",
    "TRIST": "ADJECTIU",
    "EL": "DETERMINANT",
    "LA": "DETERMINANT",
    "UN": "DETERMINANT",
    "MOLT": "ADVERBI",
    "RÀPIDAMENT": "ADVERBI",
    "BÉ": "ADVERBI"
}

NEGRE = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
VERMELL = (255, 70, 70)

FONT = pygame.font.SysFont("Trebuchet MS", 28)
pantalla = pygame.display.set_mode((AMPLADA, ALCADA_TOTAL))
pygame.display.set_caption("Tetris Gramatical en Català")

class Paraula:
    def __init__(self, text, categoria):
        self.text = text
        self.categoria = categoria
        self.columna = random.randint(0, COLUMNES - 1)
        self.y = 60

    def moure_esquerra(self):
        if self.columna > 0:
            self.columna -= 1

    def moure_dreta(self):
        if self.columna < COLUMNES - 1:
            self.columna += 1

    def caure(self, velocitat):
        self.y += velocitat

def dibuixar_cajita_paraula(pantalla, paraula, x, y):
    text_surface = FONT.render(paraula.text, True, BLANC)
    ancho_text, alto_text = text_surface.get_size()
    margen_x = 12
    margen_y = 8
    rect = pygame.Rect(x, y, ancho_text + 2 * margen_x, alto_text + 2 * margen_y)
    pygame.draw.rect(pantalla, NEGRE, rect, border_radius=6)
    pantalla.blit(text_surface, (x + margen_x, y + margen_y))

def dibuixar_tauler(paraula, punts, temps_restant):
    pantalla.fill(GRIS)

    # Àrea de joc
    for i, cat in enumerate(CATEGORIES):
        x = i * TAM_COLUMNA
        pygame.draw.rect(pantalla, NEGRE, (x, 0, TAM_COLUMNA, ALCADA_JOC))
        pygame.draw.line(pantalla, BLANC, (x, 0), (x, ALCADA_JOC), 3)
        etiqueta = FONT.render(cat, True, BLANC)
        pantalla.blit(etiqueta, (x + 10, 10))

    if paraula:
        x = paraula.columna * TAM_COLUMNA + 20
        dibuixar_cajita_paraula(pantalla, paraula, x, paraula.y)

    # Àrea inferior d'informació
    pygame.draw.rect(pantalla, NEGRE, (0, ALCADA_JOC, AMPLADA, ALCADA_INFO))

    punts_txt = FONT.render(f"Punts: {punts}", True, BLANC)
    pantalla.blit(punts_txt, (20, ALCADA_JOC + 20))

    color_temps = VERMELL if temps_restant <= 10 else BLANC
    temps_txt = FONT.render(f"Temps: {temps_restant}s", True, color_temps)
    pantalla.blit(temps_txt, (AMPLADA - 200, ALCADA_JOC + 20))

    pygame.display.flip()

def joc():
    resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
    if resposta.status_code == 200:
        resposta_json = resposta.json()
        game_id = resposta_json['game_id']
        random.seed(resposta_json['seed'])
        print("Game ID:", game_id)
    else:
        print("Error al obtener game_id")
        sys.exit()

    rellotge = pygame.time.Clock()
    paraules = list(PARAULES.items())
    paraula_actual = None
    punts = 0
    temps_inici = pygame.time.get_ticks()
    corrent = True

    INTERVALO = 5
    ultimo_envio = time.time()

    velocitat_caiguda_inicial = 5
    velocitat_caiguda_max = 25
    increment_velocitat_per_seg = (velocitat_caiguda_max - velocitat_caiguda_inicial) / DURADA

    while corrent:
        rellotge.tick(FPS)
        temps_actual = pygame.time.get_ticks()
        temps_transcorregut = (temps_actual - temps_inici) // 1000
        temps_restant = max(0, DURADA - temps_transcorregut)

        for esdeveniment in pygame.event.get():
            if esdeveniment.type == pygame.QUIT:
                corrent = False
            elif esdeveniment.type == pygame.KEYDOWN and paraula_actual:
                if esdeveniment.key == pygame.K_LEFT:
                    paraula_actual.moure_esquerra()
                elif esdeveniment.key == pygame.K_RIGHT:
                    paraula_actual.moure_dreta()

        if not paraula_actual:
            text, cat = random.choice(paraules)
            paraula_actual = Paraula(text, cat)
        else:
            velocitat_actual = min(
                velocitat_caiguda_inicial + increment_velocitat_per_seg * temps_transcorregut,
                velocitat_caiguda_max
            )
            paraula_actual.caure(velocitat_actual)
            if paraula_actual.y >= ALCADA_JOC - 100:
                columna_categoria = CATEGORIES[paraula_actual.columna]
                if columna_categoria == paraula_actual.categoria:
                    punts += 10
                else:
                    punts -= 5
                paraula_actual = None

        dibuixar_tauler(paraula_actual, punts, temps_restant)

        ara = time.time()
        if ara - ultimo_envio >= INTERVALO:
            progreso = {
                "game_id": game_id,
                "data": {
                    "score": punts,
                    "status": "en progreso"
                }
            }
            try:
                resposta_post = requests.post(
                    "https://fun.codelearn.cat/hackathon/game/store_progress",
                    json=progreso
                )
                print("Respuesta:", resposta_post.status_code)
                print("Contenido:", resposta_post.json())
            except Exception as e:
                print("Error al enviar progreso:", e)
            ultimo_envio = ara

        if temps_restant == 0:
            corrent = False

    pantalla.fill(NEGRE)
    missatge = FONT.render(f"Temps acabat! Puntuació: {punts}", True, BLANC)
    pantalla.blit(missatge, (AMPLADA // 2 - 200, ALCADA_JOC // 2))
    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    joc()

    color_temps = VERMELL if temps_restant <= 10 else BLANC
    temps_txt = FONT.render(f"Temps: {temps_restant}s", True, color_temps)
    pantalla.blit(temps_txt, (AMPLADA - 200, zona_info_y + 20))

    pygame.display.flip()

def joc():
    resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
    if resposta.status_code == 200:
        resposta_json = resposta.json()
        game_id = resposta_json['game_id']
        random.seed(resposta_json['seed'])
        print("Game ID:", game_id)
    else:
        print("Error al obtener game_id")
        sys.exit()

    rellotge = pygame.time.Clock()
    paraules = list(PARAULES.items())
    paraula_actual = None
    punts = 0
    temps_inici = pygame.time.get_ticks()
    corrent = True

    INTERVALO = 5
    ultimo_envio = time.time()

    velocitat_caiguda_inicial = 5
    velocitat_caiguda_max = 25
    increment_velocitat_per_seg = (velocitat_caiguda_max - velocitat_caiguda_inicial) / DURADA

    while corrent:
        rellotge.tick(FPS)
        temps_actual = pygame.time.get_ticks()
        temps_transcorregut = (temps_actual - temps_inici) // 1000
        temps_restant = max(0, DURADA - temps_transcorregut)

        for esdeveniment in pygame.event.get():
            if esdeveniment.type == pygame.QUIT:
                corrent = False
            elif esdeveniment.type == pygame.KEYDOWN and paraula_actual:
                if esdeveniment.key == pygame.K_LEFT:
                    paraula_actual.moure_esquerra()
                elif esdeveniment.key == pygame.K_RIGHT:
                    paraula_actual.moure_dreta()

        if not paraula_actual:
            text, cat = random.choice(paraules)
            paraula_actual = Paraula(text, cat)
        else:
            velocitat_actual = min(
                velocitat_caiguda_inicial + increment_velocitat_per_seg * temps_transcorregut,
                velocitat_caiguda_max
            )
            paraula_actual.caure(velocitat_actual)
            if paraula_actual.y >= ALCADA_JOC - 100:
                columna_categoria = CATEGORIES[paraula_actual.columna]
                if columna_categoria == paraula_actual.categoria:
                    punts += 10
                else:
                    punts -= 5
                paraula_actual = None

        dibuixar_tauler(paraula_actual, punts, temps_restant)

        ara = time.time()
        if ara - ultimo_envio >= INTERVALO:
            progreso = {
                "game_id": game_id,
                "data": {
                    "score": punts,
                    "status": "en progreso"
                }
            }
            try:
                resposta_post = requests.post(
                    "https://fun.codelearn.cat/hackathon/game/store_progress",
                    json=progreso
                )
                print("Resposta:", resposta_post.status_code)
            except Exception as e:
                print("Error al enviar progreso:", e)
            ultimo_envio = ara

        if temps_restant == 0:
            corrent = False

    pantalla.fill(NEGRE)
    missatge = FONT.render(f"Temps acabat! Puntuació: {punts}", True, BLANC)
    pantalla.blit(missatge, (AMPLADA // 2 - 200, ALCADA_TOTAL // 2))
    pygame.display.flip()

    final_data = {
        "game_id": game_id,
        "data": {
            "score": punts,
            "status": "finalitzat"
        }
    }
    try:
        final_post = requests.post("https://fun.codelearn.cat/hackathon/game/store_progress", json=final_data)
        print("Finalitzat:", final_post.status_code)
    except Exception as e:
        print("Error en enviar final:", e)

    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    joc()
