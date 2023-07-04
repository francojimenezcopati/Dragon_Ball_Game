import pygame, sys
from pygame.locals import *
from ajustes import FPS
from SceneManager import SceneManager
from config import *
from error import error

scene_manager = SceneManager()

while True:
    # try:
    dt = clock.tick(FPS) / 1000

    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if scene_switch == 2 and event.key == pygame.K_ESCAPE:
                pass
                # scene_switch = 1
                # nivel.bg_audio.stop() TODO --> ----- HACER QUE SE PARE EL JUEGO Y APAREZCA UN MENU DE OPCIONES DISTINTO AL DE ANTES
                # forms[1].btn_opciones_click('')

    scene_manager.run(dt, eventos)

    pygame.display.flip()
    # except Exception:
    #     error()