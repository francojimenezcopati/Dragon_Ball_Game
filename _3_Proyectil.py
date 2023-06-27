import pygame
from ajustes import *
from _2_Item import Item
from _2_Personaje import Personaje

class Proyectil(Item):
    def __init__(self, pos, imagen, velocidad, direccion, daño):
        super().__init__(pos, imagen)
        self.velocidad = velocidad
        self.direccion = direccion
        self.daño = daño
        self.bullet_impact_sound = pygame.mixer.Sound('Dragon_Ball\\resources\sounds\\bullet_impact.flac')
        self.bullet_impact_sound.set_volume(0.2)

    
    def verificar_objetivo(self, objetivos, terrenos, jefe = False, gd = False):
        colision_objetivo = False
        if jefe:
            if not gd:
                colision_head = self.rect.colliderect(objetivos.head_rect)
                if colision_head:
                    self.kill()
                    return 'headshot'
            else:
                colision = self.rect.colliderect(objetivos.rect)
                if colision_head:
                    self.kill()
                    return 'kill'
        else:
            colision_objetivo = pygame.sprite.spritecollide(self, objetivos, False)
        colision_terreno = pygame.sprite.spritecollide(self, terrenos, False)
        if colision_objetivo:
            
            if colision_objetivo[0].velocidad == VELOCIDAD_JUGADOR or colision_objetivo[0].velocidad == 0: # si es el jugador
                colision_objetivo[0].herido = True
                if colision_objetivo[0].tiempo_inmortalidad == 0:
                    colision_objetivo[0].vida -= self.daño
            else: # si es un enemigo
                self.bullet_impact_sound.play()
                colision_objetivo[0].vida -= self.daño
            
            self.kill()
            if colision_objetivo[0].vida >= 0:
                return True
        elif colision_terreno:
            self.kill()
        return False
    
    def update(self, dt, desplazamiento_x):
        self.rect.x += self.direccion * self.velocidad * dt
        self.rect.x += round(desplazamiento_x)