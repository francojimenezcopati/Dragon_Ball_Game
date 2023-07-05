import pygame
from GUI.config import *
from ajustes import SCREEN_WIDTH, SCREEN_HEIGHT

error_img = pygame.image.load('Dragon_Ball\\resources\Errores\\dificultades_tecnicas.jpg')
error_img = pygame.transform.scale(error_img, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()

flag = True

def error(sm):
    global flag
    
    if flag:
        flag = False
        sm.forms[1].bg_music.set_volume(0)
        pantalla.blit(error_img, (0,0))
        pygame.display.flip()
        
