import pygame
from _1_ObjetoJuego import Objeto
from pygame.math import Vector2 as vector
from ajustes import *


class Personaje(Objeto):
    def __init__(self, velocidad, vida, ataque, pos):
        super().__init__(
            pos, imagen="Dragon_Ball\\resources\goku\goku_base\quieto\\0.png"
        )
        self.vida = vida
        self.ataque = ataque
        self.velocidad = velocidad
        self.direccion = vector(0, 0)

        # Muerte
        self.tiempo_muerte = 0

    def aplicar_gravedad(self, dt):
        self.direccion.y += self.gravedad * dt
        self.rect.y += self.direccion.y

    # Colisiones
    def colisiones_verticales(self, plataformas, dt):
        self.aplicar_gravedad(dt)

        if (
            self.velocidad == VELOCIDAD_JUGADOR and not self.god_mode
        ):  # si es el jugador
            self.en_piso = False
        for plataforma in plataformas:
            if plataforma.rect.colliderect(self.rect):
                if self.direccion.y > 0:  # -> pabajo
                    self.rect.bottom = plataforma.rect.top
                    self.direccion.y = 0
                    self.tiempo_salto = 0
                    self.en_piso = True
                elif self.direccion.y < 0:  # -> parriba
                    self.rect.top = plataforma.rect.bottom
                    self.direccion.y = 0

    def colisiones_horizontales(self, plataformas, dt):
        self.mover(dt)
        colisiones = []
        for plataforma in plataformas:
            if plataforma.rect.colliderect(self.rect):
                if self.direccion.x < 0:  # -> pa la izquierda
                    self.rect.left = plataforma.rect.right
                    colisiones.append(plataforma)
                elif self.direccion.x > 0:  # -> pa la derecha
                    self.rect.right = plataforma.rect.left
                    colisiones.append(plataforma)

        return colisiones

    def lanzar_proyectil(objetivo):
        pass
