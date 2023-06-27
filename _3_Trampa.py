import pygame
from ajustes import *
from cargar_imagenes import cargar_imagenes_carpeta
from _2_Item import Item


class Trampa(Item):
    def __init__(self, pos, imagen, nivel_daño):
        super().__init__(pos, imagen)
        self.nivel_daño = nivel_daño

    def update(self, desplazamiento_x, dt=None, frames=None, animar=False):
        if animar:
            self.animar(dt, frames)
        self.rect.x += round(desplazamiento_x)


class TrampaLaser(Trampa):
    def __init__(self, pos, imagen, nivel_daño):
        super().__init__(pos, imagen, nivel_daño)
        self.tiempo_espera = 0
        self.tiempo_disparo = 0
        self.imagen_df = pygame.image.load('Dragon_Ball\\resources\enemigos\\trampa_laser\\0.png')
        self.imagen_laser = pygame.image.load('Dragon_Ball\\resources\enemigos\\trampa_laser\\1.png')
    
    def disparar(self):
        self.nivel_daño = 1
        self.image = self.imagen_laser
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
    
    def update(self, desplazamiento_x, dt):
        self.tiempo_espera += dt
        if self.tiempo_espera > TIEMPO_LASER:
            if self.tiempo_disparo < 1:
                self.tiempo_disparo += dt
                self.disparar()
            else:
                self.nivel_daño = 0
                self.image = self.imagen_df
                self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
                self.tiempo_disparo = 0
                self.tiempo_espera = 0
        self.rect.x += round(desplazamiento_x)


class Mar(Trampa):
    def __init__(self, pos, imagen, largo):
        super().__init__(pos, f"{imagen}\\1.png", 10)
        nivel_mar = pos[1]
        inicio = -SCREEN_WIDTH
        final = largo + SCREEN_WIDTH
        largo_agua = 192
        cantidad_horizontal_tiles = int(final / largo_agua) + 5
        self.rect.w += SCREEN_WIDTH

        self.frames = cargar_imagenes_carpeta(imagen)

        self.sprites = pygame.sprite.Group()

        for i in range(cantidad_horizontal_tiles):
            x = i * largo_agua + inicio

            sprite = Trampa(
                (x, nivel_mar),
                "Dragon_Ball\\niveles\\niveles\graficos\\terreno\\agua\\1",
                10,
            )
            self.sprites.add(sprite)

    def draw(self, pantalla, desplazamiento_x, dt):
        self.sprites.update(desplazamiento_x, dt, self.frames, True)
        self.sprites.draw(pantalla)
