import pygame
from _1_ObjetoJuego import Objeto
from pygame.image import load

class Plataforma(Objeto):
    def __init__(self, pos, tamaño, imagen, visible = True):
        super().__init__(pos, tamaño, imagen)
        self.visible = visible

    def draw(self, pantalla):
        if self.visible:
            pantalla.blit(self.image, self.rect.topleft)

class Hongo(Plataforma):
    def __init__(self, pos, tamaño, imagen, tipo):
        super().__init__(pos, tamaño, imagen)
        self.tipo = tipo
        self.aplicar_offset()
    
    def aplicar_offset(self):
        match self.tipo:
            case 0: # -> largo
                self.rect.y -= 74
                self.rect = self.rect.inflate(-10,0)
            case 1:  # -> corto
                self.rect.y -= 50
            case 4: # -> corto fondo
                self.rect.y -= 47
            case 5: 
                self.rect.y -= 90
            case 2: # -> izquierda
                self.rect.y -= 50
                self.rect.x -= 22
                self.rect.inflate_ip(-50,-60)
            case 3: # -> derecha
                self.rect.y -= 50
                # self.rect.x -= 10
                self.rect = self.rect.inflate(0,-60)

