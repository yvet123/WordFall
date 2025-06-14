import pygame
import random
import requests
import sys
import time

# Inicialització
pygame.init()

# Configuració
AMPLADA = 1000
ALCADA_TOTAL = 600
ALCADA_JOC = 450
ALCADA_INFO = ALCADA_TOTAL - ALCADA_JOC

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

# Colors
NEGRE = (0, 0, 0)
BLANC = (255, 255, 255)
VERMELL = (255, 70, 70)
BLAU = (0, 60, 160)  # info
BLAU2=(0, 60, 160)#fons

colores_retro = [
    (255, 0, 0), (255, 128, 0), (0, 128, 255), (0, 0, 255), (128, 0, 255),
    (255, 0, 255), (255, 0, 128), (139, 69, 19), (0, 100, 0), (75, 0, 130)
]

# Pygame setup
FONT = pygame.font.SysFont("Trebuchet MS", 28)
pantalla = pygame.display.set_mode((AMPLADA, ALCADA_TOTAL))
pygame.display.set_caption("WordFall: classifiquem per categories gramaticals!")


class Paraula:
    def __init__(self, text, categoria):
        self.text = text
        self.categoria = categoria
        self.columna = random.randint(0, len(CATEGORIES) - 1)
        self.y = 60
        self.color = random.choice(colores_retro)

    def moure_esquerra(self):
        if self.columna > 0:
            self.columna -= 1

    def moure_dreta(self):
        if self.columna < len(CATEGORIES) - 1:
            self.columna += 1

    def caure(self, velocitat):
        self.y += velocitat


def dibuixar_cajita_paraula(pantalla, paraula, x, y):
    text_surface = FONT.render(paraula.text, True, BLANC)
    ancho_text, alto_text = text_surface.get_size()
    margen_x = 12
    margen_y = 8
    rect = pygame.Rect(x, y, ancho_text + 2 * margen_x, alto_text + 2 * margen_y)
    pygame.draw.rect(pantalla, paraula.color, rect, border_radius=6)
    pantalla.blit(text_surface, (x + margen_x, y + margen_y))


def dibuixar_tauler(paraula, punts, temps_restant, encerts, errors, categories, tam_columna):
    pantalla.fill(BLAU2)

    for i, cat in enumerate(categories):
        x = i * tam_columna
        pygame.draw.line(pantalla, BLANC, (x, 0), (x, ALCADA_JOC), 3)
        etiqueta = FONT.render(cat, True, BLANC)
        pantalla.blit(etiqueta, (x + 10, 10))

    if paraula:
        x = paraula.columna * tam_columna + 20
        dibuixar_cajita_paraula(pantalla, paraula, x, paraula.y)

    pygame.draw.rect(pantalla, BLAU, (0, ALCADA_JOC, AMPLADA, ALCADA_INFO))
    punts_txt = FONT.render(f"Punts: {punts}", True, BLANC)
    pantalla.blit(punts_txt, (20, ALCADA_JOC + 20))

    color_temps = VERMELL if temps_restant <= 10 else BLANC
    temps_txt = FONT.render(f"Temps: {temps_restant}s", True, color_temps)
    pantalla.blit(temps_txt, (AMPLADA - 200, ALCADA_JOC + 20))

    encerts_txt = FONT.render(f"Encerts: {encerts}", True, BLANC)
    pantalla.blit(encerts_txt, (20, ALCADA_JOC + 50))

    errors_txt = FONT.render(f"Errors: {errors}", True, BLANC)
    pantalla.blit(errors_txt, (200, ALCADA_JOC + 50))

    pygame.display.flip()



def pantalla_inici():
    pantalla.fill(BLAU2)
    titol = FONT.render("WordFall: classifiquem per categories gramaticals!", True, BLANC)
    instr = FONT.render("Tria la dificultat: Fàcil (F) o Difícil (D)", True, BLANC)
    pantalla.blit(titol, (AMPLADA // 2 - titol.get_width() // 2, 150))
    pantalla.blit(instr, (AMPLADA // 2 - instr.get_width() // 2, 250))
    pygame.display.flip()

    esperant = True
    mode = None
    while esperant:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    mode = "facil"
                    esperant = False
                elif event.key == pygame.K_d:
                    mode = "dificil"
                    esperant = False
    return mode


def joc():
    mode = pantalla_inici()
    

    if mode == "facil":
        CATEGORIES = ["NOM", "VERB", "ADJECTIU"]
        velocitat_caiguda_inicial = 3
        velocitat_caiguda_max = 10
    else:
        CATEGORIES = ["NOM", "VERB", "ADJECTIU", "DETERMINANT", "ADVERBI"]
        velocitat_caiguda_inicial = 6
        velocitat_caiguda_max = 18

    TAM_COLUMNA = AMPLADA // len(CATEGORIES)

    class Paraula:
        def __init__(self, text, categoria):
            self.text = text
            self.categoria = categoria
            self.columna = random.randint(0, len(CATEGORIES) - 1)
            self.y = 60
            self.color = random.choice(colores_retro)

        def moure_esquerra(self):
            if self.columna > 0:
                self.columna -= 1

        def moure_dreta(self):
            if self.columna < len(CATEGORIES) - 1:
                self.columna += 1

        def caure(self, velocitat):
            self.y += velocitat

    resposta = requests.get("https://fun.codelearn.cat/hackathon/game/new")
    if resposta.status_code != 200:
        print("Error al obtenir game_id")
        sys.exit()

    game_id = resposta.json()['game_id']
    random.seed(resposta.json()['seed'])

    rellotge = pygame.time.Clock()
    paraules_possibles = [(text, cat) for text, cat in PARAULES.items() if cat in CATEGORIES]
    paraula_actual = None
    punts = 0
    encerts = 0
    errors = 0
    temps_inici = pygame.time.get_ticks()
    corrent = True
    INTERVALO = 5
    ultimo_envio = time.time()

    increment_velocitat_per_seg = (velocitat_caiguda_max - velocitat_caiguda_inicial) / DURADA

    while corrent:
        rellotge.tick(FPS)
        temps_actual = pygame.time.get_ticks()
        temps_transcorregut = (temps_actual - temps_inici) // 1000
        temps_restant = max(0, DURADA - temps_transcorregut)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                corrent = False
            elif e.type == pygame.KEYDOWN and paraula_actual:
                if e.key == pygame.K_LEFT:
                    paraula_actual.moure_esquerra()
                elif e.key == pygame.K_RIGHT:
                    paraula_actual.moure_dreta()

        if not paraula_actual:
            text, cat = random.choice(paraules_possibles)
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
                    encerts += 1
                else:
                    punts -= 5
                    errors += 1
                paraula_actual = None

                if punts < 0:
                    punts = 0

        dibuixar_tauler(paraula_actual, punts, temps_restant, encerts, errors, CATEGORIES, TAM_COLUMNA)

        if time.time() - ultimo_envio >= INTERVALO:
            progreso = {"game_id": game_id, "data": {"score": punts, "status": "en progreso"}}
            try:
                requests.post("https://fun.codelearn.cat/hackathon/game/store_progress", json=progreso)
            except Exception as e:
                print("Error al enviar progrés:", e)
            ultimo_envio = time.time()

        if temps_restant == 0:
            corrent = False

    pantalla.fill(BLAU2)
    missatge = FONT.render(f"Temps acabat! Puntuació: {punts}", True, BLANC)
    pantalla.blit(missatge, (AMPLADA // 2 - 200, ALCADA_TOTAL // 2))
    pygame.display.flip()

    try:
        final_data = {"game_id": game_id, "data": {"score": punts, "status": "finalitzat"}}
        requests.post("https://fun.codelearn.cat/hackathon/game/store_progress", json=final_data)
    except Exception as e:
        print("Error en enviar final:", e)

    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    joc()
