import pygame
from _2_Item import Item
from cargar_imagenes import cargar_imagenes_carpeta


class Recompensa(Item):
    def __init__(self, pos, imagen):
        super().__init__(pos, f"{imagen}\\1.png")
        self.recuperar_vida = 1
        self.frames = cargar_imagenes_carpeta(imagen)

    def update(self, dt, desplazamiento_x):
        self.rect.x += round(desplazamiento_x)
        self.animar(dt, self.frames)
