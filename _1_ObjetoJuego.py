import pygame
from pygame.image import load

from ajustes import *

class Objeto(pygame.sprite.Sprite):
    def __init__(self, pos, tamaño = (3, 3), imagen = None):
        super().__init__()
        # Animacion
        self.frame_index = 0
        self.velocidad_animacion = VELOCIDAD_ANIMACION
        
        if type(imagen) == pygame.surface.Surface:
            self.image = imagen
        else:
            try:
                self.image = load(imagen).convert_alpha()
            except:
                self.image = pygame.Surface(tamaño)
                self.image.fill((209,170,157))
        
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pos
    
    def animar(self, dt, frames):
        self.frame_index += self.velocidad_animacion * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]
    
    def update(self, desplazamiento_x):
        self.rect.x += round(desplazamiento_x)
    
    def draw(self, pantalla): #-> se ejecuta todo el tiempo
        pantalla.blit(self.image, self.rect.topleft)
        


class Cielo:
    def __init__(self, middle):
        self.middle = middle
        
        self.top = load('Dragon_Ball\\niveles\\niveles\graficos\\terreno\cielo\sky_top.png')
        self.mid = load('Dragon_Ball\\niveles\\niveles\graficos\\terreno\cielo\sky_middle.png')
        self.bottom = load('Dragon_Ball\\niveles\\niveles\graficos\\terreno\cielo\\sky_bottom.png')

        self.top = pygame.transform.scale(self.top, (SCREEN_WIDTH, TILE_SIZE))
        self.mid = pygame.transform.scale(self.mid, (SCREEN_WIDTH, TILE_SIZE))
        self.bottom = pygame.transform.scale(self.bottom, (SCREEN_WIDTH, TILE_SIZE))

    def draw(self, pantalla): #-> se ejecuta todo el tiempo
        for fila in range(CANTIDAD_VERTICAL_TILES):
            y = fila * TILE_SIZE
            if fila < self.middle:
                pantalla.blit(self.top, (0, y))
            elif fila == self.middle:
                pantalla.blit(self.mid, (0, y))
            else:
                pantalla.blit(self.bottom, (0, y))
    
