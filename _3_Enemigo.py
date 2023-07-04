import pygame
from pygame.math import Vector2 as vector

from ajustes import *
from cargar_imagenes import *
from _2_Personaje import Personaje
from _3_Proyectil import Proyectil
from config import *



class Enemigo(Personaje):
    def __init__(self, velocidad, pos, vida, ataque, tipo, jefe = False):
        super().__init__(velocidad, vida, ataque, pos)
        if not jefe:
            self.tipo = tipo

            self.direccion.x = 0
            self.gravedad = GRAVEDAD_CAIDA
            
            self.dispara = False
            self.tiempo_disparar = 0
            self.espera_entre_disparos = 0
            self.disparos_rafaga = 0
            self.proyectiles = pygame.sprite.Group()
            
            
            # Muerte
            self.velocidad_animacion_muerte = VELOCIDAD_ANIMACION_MUERTE_ENEMIGOS

            # animar
            self.estado = "quieto"
            self.sentido = "_derecha"
            self.importar_animaciones()
            self.image = self.animaciones[self.estado + self.sentido][
                self.frame_index
            ]
            self.rect = self.image.get_rect(topleft=pos)
        
        else: # ----------------------------------------- -> Si es el jefe
            self.frames = cargar_imagenes_carpeta('Dragon_Ball\\resources\\final_boss\\boss')
            self.frames = agrandar_jefe(self.frames)
            self.image = self.frames[0]
            self.rect = self.image.get_rect(topleft=pos)
            self.velocidad_animacion = VELOCIDAD_ANIMACION_Y_DISPARO_JEFE
            
            self.is_killed = False
            
            # disparo ---
            self.rayo_cargando = pygame.image.load('Dragon_Ball\\resources\\final_boss\\4.png')
            self.rayo_cargando = pygame.transform.rotozoom(self.rayo_cargando, 0 , 4.195)
            self.rayo_cargando_rect = self.rayo_cargando.get_rect(midright = (49 * TILE_SIZE, 179))
            
            self.rayo = pygame.image.load('Dragon_Ball\\resources\\final_boss\\5.png')
            self.rayo = pygame.transform.rotozoom(self.rayo, 0 , 4.195)
            self.rayo = pygame.transform.scale(self.rayo, (self.rayo.get_width() * 2.367,self.rayo.get_height()))
            self.rayo_largo_rect = self.rayo.get_rect(midright = (49 * TILE_SIZE, 179))
            
            self.rayo_rect = self.rayo_cargando_rect
            
            self.head_rect = pygame.Rect(48 * TILE_SIZE-100, 0, 190, 190)
            
            self.tiempo_transcurrido_frame = 0
            self.tiempo_espera_disparo = TIEMPO_CARGA_ATAQUE_JEFE
            self.tiempo_disparo = DURACION_ATAQUE_JEFE
            
            #-----------

    def importar_animaciones(self):
        escalar = False
        match self.tipo:
            case 0:
                self.dispara = True
                self.puede_moverse = False
                self.estado = "quieto"
                robot = "Destroyer"
            case 1:
                self.puede_moverse = False
                self.estado = "quieto"
                robot = "Infantryman"
            case _:
                self.puede_moverse = True
                self.estado = "caminar"
                robot = "robot_capa"
                escalar = True
        self.animaciones = cargar_animaciones_personaje(
            f"Dragon_Ball\\resources\enemigos\{robot}",
            ANCHO_PERSONAJE,
            ALTO_PERSONAJE,
            True,
            True,
        )
        if escalar:
            escalar = False
            self.animaciones = reescalar_imagenes(self.animaciones)

    def mover(self, dt):
        if self.puede_moverse:
            self.rect.x += self.direccion.x * self.velocidad * dt

    def definir_sentido(self):
        if self.direccion.x == 1:
            self.sentido = "_derecha"
        else:
            self.sentido = "_izquierda"

    def cambiar_sentido(self):
        self.direccion.x *= -1

    def muerte(self, dt): # las animaciones de muerte ya estan incluidas en el diccionario de animaciones de cada robot, estado = 'muerte' + sentido
        self.direccion.x = 0
        
        self.frame_index += self.velocidad_animacion_muerte * dt
        if self.frame_index >= len(self.animaciones[self.estado + self.sentido]):
            self.frame_index = len(self.animaciones[self.estado + self.sentido]) - 1 # se queda en el ultimo frame
        self.image = self.animaciones[self.estado + self.sentido][int(self.frame_index)]
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        
        if self.tiempo_muerte > 1.5:
            self.kill()

    def apuntar_jugador(self, vec_jugador):
        vec_enemigo = vector(self.rect.x, self.rect.y)
        vector_diferencia = vec_jugador - vec_enemigo # positivo-> derecha, negativo-> izq
        if vector_diferencia.x > 0:
            self.direccion.x = 1
        else:
            self.direccion.x = -1

    def disparar(self):
        if self.sentido == '_derecha':
            sentido = 1
        else:
            sentido = -1
        x = self.rect.centerx + (self.rect.w * 0.5) * sentido
        y = self.rect.y + 14
        
        enemy_shoot_sound.play()
        
        path = 'Dragon_Ball\\resources\enemigos\Destroyer\proyectil\\0.png'
        disparo = Proyectil((x, y), path, VELOCIDAD_PROYECTIL_ENEMIGO, sentido, self.ataque)
        self.proyectiles.add(disparo)

    def update(self, dt, pantalla, desplazamiento_x, tiempo, colisionables, vec_jugador, grupo_jugador, grupo_terreno):
        colisiones = self.colisiones_horizontales(colisionables, dt)
        if colisiones:
            self.cambiar_sentido()
        self.colisiones_verticales(colisionables, dt)
        self.rect.x += round(desplazamiento_x)
        self.proyectiles.update(dt, desplazamiento_x)
        self.proyectiles.draw(pantalla)
        if self.vida <= 0: # muerto
            if self.tiempo_muerte <= 0:
                self.frame_index = 0
            self.estado = 'muerte'
            self.tiempo_muerte += dt
            self.muerte(dt)
        else:
            #----- disparo -------
            self.tiempo_disparar += dt
            if self.dispara and self.tiempo_disparar > TIEMPO_DISPARO_ENEMIGO: # tiempo entre rafagas
                self.estado = 'ataque'
                
                if self.espera_entre_disparos > ESPERA_ENTRE_DISPAROS: # tiempo entre disparos de la rafaga
                    self.espera_entre_disparos = 0
                    self.disparar()
                    self.disparos_rafaga += 1
                    if self.disparos_rafaga >= DISPAROS_ENEMIGOS: # cantidad de disparos en la rafaga
                        self.disparos_rafaga = 0
                        self.tiempo_disparar = 0
                self.espera_entre_disparos += dt
            else:
                if self.dispara:
                    self.estado = 'quieto'
            if self.dispara: # los que disparan
                self.apuntar_jugador(vec_jugador)
                for proyectil in self.proyectiles:
                    proyectil.verificar_objetivo(grupo_jugador, grupo_terreno)
            #----- ------- -------
            
            self.animar(dt, self.animaciones[self.estado + self.sentido])
            
            if tiempo > 1 and tiempo < 1.1:
                self.direccion.x = -1
            self.definir_sentido()

    def caer_libre():
        pass

    #--- JEFE ---
    
    def verificar_colision_jugador(self, jugador):
        colision = pygame.sprite.spritecollide(self, jugador, False)
        if colision:
            colision[0].vida -= 10
    
    def verificar_colision_rayo(self, jugador):
        if jugador.sprite:
            colision = self.rayo_rect.colliderect(jugador.sprite.rect)
            if colision:
                jugador.sprite.vida -= self.ataque
                return True
            return False
    
    def update_jefe(self, dt, desplazamiento_x, pantalla):
        self.rect.x += round(desplazamiento_x)
        self.rayo_largo_rect.x += round(desplazamiento_x)
        self.rayo_cargando_rect.x += round(desplazamiento_x)
        self.head_rect.x += round(desplazamiento_x)
        
        self.animar_jefe(dt, self.frames, pantalla)
        self.rect.y =  9 * TILE_SIZE - self.image.get_height()
    
    def draw_jefe(self, pantalla):
        pantalla.blit(self.image, self.rect.topleft)

    def animar_jefe(self, dt, frames, pantalla):
        self.frame_index += self.velocidad_animacion * dt
        if self.frame_index >= len(frames): # -> frame de disparo
            # self.frame_index = len(frames)-1
            self.tiempo_transcurrido_frame += dt
            if self.tiempo_transcurrido_frame < self.tiempo_espera_disparo:
                pantalla.blit(self.rayo_cargando, self.rayo_cargando_rect)
                self.rayo_rect = self.rayo_cargando_rect
            elif self.tiempo_transcurrido_frame < self.tiempo_disparo + self.tiempo_espera_disparo:
                pantalla.blit(self.rayo, self.rayo_largo_rect)
                self.rayo_rect = self.rayo_largo_rect
            else:
                self.rayo_rect = pygame.Rect(1,1,1,1)
                self.frame_index = 0
                self.tiempo_transcurrido_frame = 0
        
        if self.tiempo_transcurrido_frame != 0:
            self.image = frames[len(frames)-1]
        else:
            self.image = frames[int(self.frame_index)]