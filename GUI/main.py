import pygame
import sys
from pygame.locals import *
from _GUI_form_principal import *
from _GUI_form_inicio import *
from ajustes import *

pygame.init()
FPS = 60

reloj = pygame.time.Clock()
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

forms = [
    FormInicio(
        pantalla, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, "white", "red", 5, True
    ),
    FormPrincipal(
        pantalla,
        0,
        0,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "white",
        "red",
        5,
        True,
    ),
]

form_actual = forms[0]

enter = False
while True:
    dt = reloj.tick(FPS) / 1000

    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill("black")

    if not enter:
        enter = form_actual.update(dt, eventos)
    else:
        form_actual = forms[1]
        form_actual.update(eventos)

    pygame.display.flip()
