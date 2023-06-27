import pygame
from pygame.math import Vector2 as vector

from ajustes import *
from cargar_imagenes import *
from _2_Personaje import Personaje
from _3_Proyectil import Proyectil

class Jugador(Personaje):
    def __init__(self, pantalla, potencia_salto, velocidad, vida, ataque, pos):
        super().__init__(velocidad, vida, ataque, pos)
        self.pantalla = pantalla
        
        self.god_mode = False
        
        
        
        self.pikcup_sound = pygame.mixer.Sound('Dragon_Ball\\resources\sounds\pickup.wav')
        self.transformacion_sound = pygame.mixer.Sound('Dragon_Ball\\resources\sounds\\transformacion.wav')
        self.pikcup_sound.set_volume(0.5)
        self.transformacion_sound.set_volume(0.2)
        self.daño_sound = pygame.mixer.Sound('Dragon_Ball\\resources\sounds\\daño.wav')
        self.daño_sound.set_volume(0.2)
        
        # GD
        self.gd_counter = 0
        self.tirar_gd = False
        self.frames_gd = cargar_imagenes_carpeta('Dragon_Ball\\resources\goku\\goku_genkidama')
        self.frames_gd = escalar_genkidama(self.frames_gd)
        self.gd_img = pygame.image.load('Dragon_Ball\\resources\proyectiles\genkidama.png')
        x = self.rect.x - 10
        y = self.rect.y + 100
        self.gd = Proyectil((x,y), self.gd_img, 0, 1, 100)
        
        # SSJ
        self.ssj_count = 0
        self.esta_ssj = False
        self.transformandose = False
        self.frames_transformacion = cargar_imagenes_carpeta('Dragon_Ball\\resources\goku\\transformacion')
        
        # Muerte
        self.frames_muerte = cargar_imagenes_carpeta('Dragon_Ball\\resources\goku\goku_muerte')
        self.velocidad_animacion_muerte = VELOCIDAD_ANIMACION_MUERTE
        
        # Herido
        self.herido = False
        self.hud_herido = pygame.image.load('Dragon_Ball\\resources\HUD\DAÑO\\bordes_rojos.png')
        self.hud_herido = pygame.transform.scale(self.hud_herido, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Proyectiles
        self.proyectiles = pygame.sprite.Group()
        self.tiempo_disparo = 1
        self.puede_disparar = True
        
        # Enemigos
        self.tiempo_inmortalidad = 0
        
        # animar
        self.importar_animaciones('Dragon_Ball\\resources\goku\goku_base')
        self.estado = 'quieto'
        self.sentido = '_derecha'
        self.image = self.animaciones[self.estado + self.sentido][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movimiento
        self.en_piso = False
        self.potencia_salto = potencia_salto
        self.tiempo_salto = 0
        self.esta_saltando = False
        self.gravedad = GRAVEDAD
        
    
    def importar_animaciones(self, path):
        self.animaciones = cargar_animaciones_personaje(path, ANCHO_PERSONAJE, ALTO_PERSONAJE, True)
    
    def get_input(self, dt):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direccion.x = 1
            self.sentido = '_derecha'
        elif keys[pygame.K_LEFT]:
            self.direccion.x = -1
            self.sentido = '_izquierda'
        else:
            self.direccion.x = 0

        if keys[pygame.K_SPACE] and self.esta_saltando:
            if self.tiempo_salto < 0.2:
                self.tiempo_salto += dt
                self.saltar(dt)
    
    # ANIMACIONES
    
    def definir_estado(self):
        if self.tiempo_disparo < TIEMPO_DISPARO_JUGADOR:
            self.puede_disparar = False
            self.estado = 'ataque'
        else:
            self.puede_disparar = True
            if self.direccion.y < 0:
                self.estado = 'salto'
            elif self.direccion.y > 1:
                self.estado = 'caida'
            elif self.direccion.y == 0 and self.direccion.x != 0:
                self.estado = 'caminar'
            elif self.direccion.y == 0 and self.direccion.x == 0:
                self.estado = 'quieto'
    
    # Movilidad

    def saltar(self, dt):
        self.direccion.y = self.potencia_salto * dt
    
    def mover(self, dt):
        self.rect.x += self.direccion.x * self.velocidad * dt
    
    # Enemigos
    
    def verificar_colision_enemigos(self, enemigos):
        colision = pygame.sprite.spritecollide(self, enemigos, False)
        if colision:
            # print(colision[0].velocidad)
            if self.tiempo_inmortalidad == 0:
                if self.vida > 0 and colision[0].vida > 0:
                    self.herido = True
                    self.vida -= 1

    def verificar_colision_items(self, items):
        colision = pygame.sprite.spritecollide(self, items, True)
        if colision:
            self.pikcup_sound.play()
            self.vida += 1
            if self.vida > 3 and not self.esta_ssj:
                self.vida = 3
            elif self.vida > 5 and self.esta_ssj:
                self.vida = 5
    
    def verificar_colision_final(self, final):
        colision = pygame.sprite.spritecollide(self, final, True)
        if colision:
            return True
        return False

    def verificar_colision_trampas(self, trampas):
        colision = pygame.sprite.spritecollide(self, trampas, False)
        if colision:
            if self.tiempo_inmortalidad == 0:
                vida = self.vida
                if self.vida > 0:
                    self.vida -= colision[0].nivel_daño
                    if vida != self.vida:
                        self.herido = True

    def disparar(self):
        if self.puede_disparar:
            self.tiempo_disparo = 0
            
            if self.sentido == '_derecha':
                sentido = 1
                tipo = '.png'
            else:
                sentido = -1
                tipo = '_izq.png'
            
            x = self.rect.centerx + (self.rect.w * 0.5) * sentido
            y = self.rect.y + self.rect.h / 2 - 10
            
            if not self.esta_ssj:
                path = f'Dragon_Ball\\resources\proyectiles\proyectil_base{tipo}'
            else:
                path = f'Dragon_Ball\\resources\proyectiles\proyectil_mejorado{tipo}'
            
            disparo = Proyectil((x, y), path, VELOCIDAD_PROYECTIL_JUGADOR, sentido, self.ataque)
            self.proyectiles.add(disparo)

    def muerte(self, dt):
        self.direccion.x = 0
        
        self.frame_index += self.velocidad_animacion_muerte * dt
        if self.frame_index >= len(self.frames_muerte):
            self.frame_index = len(self.frames_muerte) - 1
        self.image = self.frames_muerte[int(self.frame_index)]
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        
        if self.tiempo_muerte > 2.4:
            self.kill()

    def transformacion(self, dt):
        self.direccion.x = 0
        flag = False
        
        self.frame_index += self.velocidad_animacion_muerte * dt
        if self.frame_index >= len(self.frames_transformacion):
            self.frame_index = len(self.frames_transformacion) - 1
            self.transformandose = False
            self.vida = VIDA_SSJ_JUGADOR
            self.ataque = ATAQUE_SSJ_JUGADOR
            self.esta_ssj = True
            flag = True
            self.importar_animaciones('Dragon_Ball\\resources\goku\goku_ssj')
        
        
        self.image = self.frames_transformacion[int(self.frame_index)]
        if flag: # para que no se deforme el rectangulo al final
            self.animar(dt, self.animaciones[self.estado + self.sentido])
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        if flag:
            self.rect.y += 31

    def ejecutar_gd(self, dt):
        pass

    def update(self, dt, pantalla, desplazamiento_mundo):
        if self.vida <= 0:
            pantalla.blit(self.hud_herido, (0,0))
            self.tiempo_muerte += dt
            if 0.01 < self.tiempo_muerte < 0.05:
                self.daño_sound.play()
            self.muerte(dt)
        else:
            self.gd.draw(pantalla)
            self.gd.update(dt, desplazamiento_mundo)
            if self.transformandose:
                self.transformacion(dt)
            else:
                if self.tirar_gd:
                    self.ejecutar_gd(dt)
                else:
                    if self.god_mode:
                        self.en_piso = True
                        self.ssj_count = UMBRAL_SSJ

                    if self.ssj_count > UMBRAL_SSJ:
                        self.ssj_count = UMBRAL_SSJ
                    
                    if self.herido:
                        pantalla.blit(self.hud_herido, (0,0))
                        self.tiempo_inmortalidad += dt
                        if 0.01 < self.tiempo_inmortalidad < 0.05:
                            self.daño_sound.play()
                    if self.tiempo_inmortalidad > 3:
                        self.tiempo_inmortalidad = 0
                        self.herido = False
                    
                    self.tiempo_disparo += dt
                    self.get_input(dt)
                    self.animar(dt, self.animaciones[self.estado + self.sentido])
        self.proyectiles.update(dt, desplazamiento_mundo)
        self.proyectiles.draw(pantalla)
        self.definir_estado()
