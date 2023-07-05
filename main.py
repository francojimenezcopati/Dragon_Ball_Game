import pygame, sys
from pygame.locals import *
from ajustes import FPS
from SceneManager import SceneManager
from GUI.config import *
from error import error

scene_manager = SceneManager()

while True:
    try:
        dt = clock.tick(FPS) / 1000

        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        scene_manager.run(dt, eventos)

        pygame.display.flip()
    except Exception:
        error(scene_manager)
