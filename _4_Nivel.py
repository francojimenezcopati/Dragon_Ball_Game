import pygame, sys
from ajustes import *
from _1_ObjetoJuego import Objeto, Cielo
from _2_Plataforma import Plataforma, Hongo
from _2_Item import Item
from _3_Enemigo import Enemigo
from _3_Jugador import Jugador
from _3_Recompensa import Recompensa
from _3_Trampa import Mar, Trampa, TrampaLaser
from importar_niveles import importar_csv_layout
from cargar_imagenes import cargar_terreno, cargar_imagenes_carpeta


class Nivel:
    def __init__(self, data_nivel, pantalla, nivel_2 = False, nivel_3 = False):
        self.pantalla = pantalla
        self.modo = False
        self.running = True
        
        #---------- LVL FINAL ---------------
        
        self.flag_entrada = False
        self.flag_spawnear_enemigos = False
        self.flag_invencibilidad = False
        
        self.tiempo_invencibilidad = 0
        
        self.jefe_setup()
        
        #---------- --------- ---------------
        
        
        self.is_nivel_2 = nivel_2
        self.is_lvl_3 = nivel_3
        
        self.tiempo_anterior = 0
        self.desplazamiento_mundo = 0
        self.tiempo = 0
        self.tiempo_salto = 0
        
        self.bg_audio = pygame.mixer.Sound('Dragon_Ball\\resources\sounds\\bg_game_music.mp3')
        self.bg_audio.set_volume(0.1)
        self.bg_audio.play(-1)
        
        # texto
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.texto_blit = self.font.render('0', False, 'black')
        self.bg_rect = pygame.Rect(575, 3, 60, 40)
        self.bg_rect_2 = pygame.Rect(575, 3, 60, 40)
        
        # INTERFAZ MENUS
        self.menu_victoria = False
        
        
        # CONFIGURACION IMPORTAR NIVELES
        
        # jugador
        jugador_layout = importar_csv_layout(data_nivel['jugador'])
        self.jugador = pygame.sprite.GroupSingle()
        self.final = pygame.sprite.GroupSingle()
        self.configurar_jugador(jugador_layout)
        
        # items
        items_layout = importar_csv_layout(data_nivel['items'])
        self.sprites_items = self.crear_grupo_sprites(items_layout, 'items')
        
        # hongos fg
        fg_hongos_layout = importar_csv_layout(data_nivel['fg_hongos'])
        self.sprites_fg_hongos = self.crear_grupo_sprites(fg_hongos_layout, 'fg_hongos')
        
        # pinchos
        pinchos_layout = importar_csv_layout(data_nivel['pinchos'])
        self.sprites_pinchos = self.crear_grupo_sprites(pinchos_layout, 'pinchos')
        
        # restriccion enemigos
        restricciones_layout = importar_csv_layout(data_nivel['restricciones'])
        self.sprites_restricciones = self.crear_grupo_sprites(restricciones_layout, 'restricciones')
        
        # enemigos
        enemigos_layout = importar_csv_layout(data_nivel['enemigos'])
        self.sprites_enemigos = self.crear_grupo_sprites(enemigos_layout, 'enemigos')
        
        # pasto
        pasto_layout = importar_csv_layout(data_nivel['pasto'])
        self.sprites_pasto = self.crear_grupo_sprites(pasto_layout, 'pasto')
        
        # cajas
        cajas_layout = importar_csv_layout(data_nivel['cajas'])
        self.sprites_cajas = self.crear_grupo_sprites(cajas_layout, 'cajas')
        
        # terreno
        terreno_layout = importar_csv_layout(data_nivel['terreno'])
        self.sprites_terreno = self.crear_grupo_sprites(terreno_layout, 'terreno')
        
        # hongos bg
        bg_hongos_layout = importar_csv_layout(data_nivel['bg_hongos'])
        self.sprites_bg_hongos = self.crear_grupo_sprites(bg_hongos_layout, 'bg_hongos')
        
        # fondo cueva
        fondo_cueva_layout = importar_csv_layout(data_nivel['fondo_cueva'])
        self.sprites_fondo_cueva = self.crear_grupo_sprites(fondo_cueva_layout, 'fondo_cueva')
        
        if not self.is_nivel_2:
            # mar
            largo = len(terreno_layout[0]) * TILE_SIZE
            self.mar = Mar((0,SCREEN_HEIGHT - 40), 'Dragon_Ball\\niveles\\niveles\graficos\\terreno\\agua', largo)
            
            # cielo
            self.cielo = Cielo(4)
        else:
            # Trampa laser
            trampa_laser_layout = importar_csv_layout(data_nivel['trampa_laser'])
            self.sprites_trampa_laser = self.crear_grupo_sprites(trampa_laser_layout, 'trampa_laser')
        
        # nubes
        nubes_layout = importar_csv_layout(data_nivel['nubes'])
        self.sprites_nubes = self.crear_grupo_sprites(nubes_layout, 'nubes')
        
    #---------- LVL FINAL ---------------
    
    def jefe_setup(self):
        x = 46 * TILE_SIZE
        y = -23
        self.jefe = Enemigo(3, (x,y), VIDA_JEFE, 2, 0, True)
    
    def checkear_entrada_zona_jefe(self):
        if self.flag_entrada:
            entro = pygame.sprite.spritecollide(self.jugador.sprite, self.sprites_restricciones, False)
            if entro:
                self.cerrar_entrada()
                self.flag_spawnear_enemigos = True
                self.flag_entrada = False
    
    def spawnear_enemigos(self):
        pass
    
    def cerrar_entrada(self):
        pass
    
    #---------- --------- ---------------
    

    def crear_grupo_sprites(self,layout,tipo):
        grupo = pygame.sprite.Group()

        for i, fila in enumerate(layout): # -> cada fila [-1,-1,0,...]
            for j, valor in enumerate(fila): # -> cada valor de cada fila '-1' ... '0'
                if valor != '-1':
                    x = j * TILE_SIZE # -> la cantidad de columnas de la fila * tamaño tile
                    y = i * TILE_SIZE
                    
                    sprite = ''
                    match tipo:
                        case 'terreno':
                            terrenos = cargar_terreno('Dragon_Ball\\niveles\\niveles\graficos\\terreno\\terrain_tiles.png')
                            terreno = terrenos[int(valor)]
                            sprite = Plataforma((x,y), (TILE_SIZE, TILE_SIZE), terreno)
                        case 'pasto':
                            pastos = cargar_terreno('Dragon_Ball\\niveles\\niveles\graficos\\terreno\\grass.png')
                            pasto = pastos[int(valor)]
                            sprite = Plataforma((x,y), (TILE_SIZE, TILE_SIZE), pasto)
                        case 'cajas':
                            path = 'Dragon_Ball\\niveles\\niveles\graficos\\terreno\crate.png'
                            sprite = Plataforma((x,y), (TILE_SIZE, TILE_SIZE), path)
                            sprite.rect.bottomleft = (x, y + TILE_SIZE)
                        case 'items':
                            sprite = Recompensa((x,y), 'Dragon_Ball\\niveles\\niveles\graficos\items\semilla')
                        case 'fg_hongos':
                            path = 'Dragon_Ball\\niveles\\niveles\graficos\\terreno\hongos'
                            hongos = cargar_imagenes_carpeta(path)
                            tipo_hongo = int(valor) - 9
                            hongo = hongos[tipo_hongo]
                            sprite = Hongo((x,y), (TILE_SIZE, TILE_SIZE), hongo, tipo_hongo)
                        case 'bg_hongos':
                            path = 'Dragon_Ball\\niveles\\niveles\graficos\\terreno\hongos'
                            hongos = cargar_imagenes_carpeta(path)
                            tipo_hongo = int(valor) - 9
                            hongo = hongos[tipo_hongo]
                            sprite = Hongo((x,y), (TILE_SIZE, TILE_SIZE), hongo, tipo_hongo)
                        case 'enemigos':
                            tipo_robot = int(valor) - 2
                            sprite = Enemigo(VELOCIDAD_ENEMIGOS, (x, y), VIDA_BASE_ENEMIGOS, 1, tipo_robot)
                        case 'restricciones':
                            sprite = Plataforma((x,y), (TILE_SIZE, TILE_SIZE), None, False)
                        case 'nubes':
                            path = 'Dragon_Ball\\niveles\\niveles\graficos\\terreno\\nubes'
                            nubes = cargar_imagenes_carpeta(path)
                            nube = nubes[int(valor)]
                            sprite = Objeto((x, y), imagen=nube)
                        case 'fondo_cueva':
                            terrenos = cargar_terreno('Dragon_Ball\\niveles\\niveles\graficos\\terreno\\terrain_tiles.png')
                            terreno = terrenos[int(valor)]
                            sprite = Plataforma((x,y), (TILE_SIZE, TILE_SIZE), terreno)
                        case 'pinchos':
                            sprite = Trampa((x,y), 'Dragon_Ball\\resources\enemigos\spikes.png', 5)
                        case 'trampa_laser':
                            sprite = TrampaLaser((x,y), 'Dragon_Ball\\resources\enemigos\\trampa_laser\\0.png', 2)
                            sprite.rect.midbottom = (x + TILE_SIZE/2, y + TILE_SIZE)
                        
                    grupo.add(sprite)
                    
        return grupo


    def configurar_jugador(self, layout):
        for i, fila in enumerate(layout):
            for j, valor in enumerate(fila):
                x = j * TILE_SIZE
                y = i * TILE_SIZE
                if valor == '0':
                    sprite = Jugador(self.pantalla ,POTENCIA_SALTO, VELOCIDAD_JUGADOR, VIDA_BASE_JUGADOR, ATAQUE_BASE_JUGADOR, (x, y),)
                    self.jugador.add(sprite)
                elif valor == '1':
                    sprite = Item((x,y), 'Dragon_Ball\\resources\meta\\bola de dragon.png')
                    self.final.add(sprite)
    
    
    def colision_enemigos_restriccion(self, dt):
        for enemigo in self.sprites_enemigos:
            if pygame.sprite.spritecollide(enemigo, self.sprites_restricciones, False):
                enemigo.cambiar_sentido()

    
    def desplazar_x(self, dt):
        jugador = self.jugador.sprite # -> obtengo el objeto del grupo
        jugador_x = jugador.rect.centerx
        margen_izquierda = SCREEN_WIDTH / 4
        if not self.is_lvl_3:
            margen_derecha = SCREEN_WIDTH - margen_izquierda * 2
        else:
            margen_derecha = SCREEN_WIDTH - margen_izquierda * 3
        
        if jugador_x < margen_izquierda and jugador.direccion.x < 0: #-> esta yendo pa la izquierda
            self.desplazamiento_mundo = VELOCIDAD_JUGADOR * dt
            jugador.velocidad = 0
        elif jugador_x > margen_derecha and jugador.direccion.x > 0:
            self.desplazamiento_mundo = -VELOCIDAD_JUGADOR * dt
            jugador.velocidad = 0
        else:
            self.desplazamiento_mundo = 0
            jugador.velocidad = VELOCIDAD_JUGADOR
    
    def get_input(self, dt, eventos):
        jugador = self.jugador.sprite
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    self.modo = not self.modo
                if evento.key == pygame.K_f and jugador.vida > 0:
                    jugador.disparar()
                elif evento.key == pygame.K_d and jugador.vida > 0 and jugador.ssj_count == UMBRAL_SSJ and not jugador.esta_ssj and not jugador.transformandose:
                    jugador.transformandose = True
                    jugador.transformacion_sound.play()
                    jugador.frame_index = 0
                elif (
                    jugador
                    and evento.key == pygame.K_SPACE
                    and jugador.en_piso
                    and jugador.vida > 0
                ):
                    jugador.esta_saltando = True
                    jugador.en_piso = False
                    jugador.saltar(dt)
                elif not jugador.tirar_gd and evento.key == pygame.K_s and jugador.vida > 0 and jugador.gd_count == UMBRAL_GENKI_DAMA:
                    jugador.tirar_gd = True
                elif evento.key == pygame.K_COMMA and jugador:
                    jugador.god_mode = not jugador.god_mode
            if jugador and evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    jugador.esta_saltando = False
    
    def draw_all(self, dt):
        jugador = self.jugador.sprite
        
        if not self.is_nivel_2:
            # cielo
            self.cielo.draw(self.pantalla)
            
            # nubes
            self.sprites_nubes.update(self.desplazamiento_mundo)
            self.sprites_nubes.draw(self.pantalla)
            
            # fondo cueva
            self.sprites_fondo_cueva.update(self.desplazamiento_mundo)
            self.sprites_fondo_cueva.draw(self.pantalla)
        else:
            self.pantalla.fill((52,52,62))
        
        
        # hongos bg
        self.sprites_bg_hongos.update(self.desplazamiento_mundo)
        self.sprites_bg_hongos.draw(self.pantalla)
        
        # cajas
        self.sprites_cajas.update(self.desplazamiento_mundo)
        self.sprites_cajas.draw(self.pantalla)
        
        # enemigos
        vec_jugador = pygame.Vector2(jugador.rect.x, jugador.rect.y)
        
        objetos_colisionables_enemigo = self.sprites_terreno.sprites() + self.sprites_restricciones.sprites()
        self.sprites_enemigos.update(dt, self.pantalla, self.desplazamiento_mundo, self.tiempo, objetos_colisionables_enemigo, vec_jugador, self.jugador, self.sprites_terreno)
        self.sprites_enemigos.draw(self.pantalla)

        #pinchos
        self.sprites_pinchos.update(self.desplazamiento_mundo)
        self.sprites_pinchos.draw(self.pantalla)

        # mar
        if not self.is_nivel_2:
            self.mar.draw(self.pantalla, self.desplazamiento_mundo, dt)
        else:
            self.sprites_trampa_laser.update(self.desplazamiento_mundo, dt)
            self.sprites_trampa_laser.draw(self.pantalla)
            
        
        # Tierra
        self.sprites_terreno.update(self.desplazamiento_mundo)
        self.sprites_terreno.draw(self.pantalla)
        
        # pasto
        self.sprites_pasto.update(self.desplazamiento_mundo)
        self.sprites_pasto.draw(self.pantalla)
        
        # restriccion enemigos
        self.sprites_restricciones.update(self.desplazamiento_mundo)

        
        # hongos fg
        self.sprites_fg_hongos.update(self.desplazamiento_mundo)
        self.sprites_fg_hongos.draw(self.pantalla)
        
        # items
        self.sprites_items.update(dt, self.desplazamiento_mundo)
        self.sprites_items.draw(self.pantalla)

        self.final.update(self.desplazamiento_mundo)
        self.final.draw(self.pantalla)
        self.jugador.update(dt, self.pantalla, self.desplazamiento_mundo)
        self.jugador.draw(self.pantalla)
    
    def colisiones(self, dt):
        jugador = self.jugador.sprite
        
        objetos_colisionables = self.sprites_terreno.sprites() + self.sprites_fg_hongos.sprites()
        
        # jugador
        jugador.colisiones_horizontales(objetos_colisionables, dt)
        jugador.colisiones_verticales(objetos_colisionables, dt)
        
        jugador.verificar_colision_enemigos(self.sprites_enemigos)
        jugador.verificar_colision_trampas(self.sprites_pinchos)
        jugador.verificar_colision_items(self.sprites_items)
        
        if not self.is_nivel_2:
            jugador.verificar_colision_trampas(pygame.sprite.GroupSingle(self.mar))
        else:
            jugador.verificar_colision_trampas(self.sprites_trampa_laser)
            
        for proyectil in jugador.proyectiles:
            colisiono = proyectil.verificar_objetivo(self.sprites_enemigos, self.sprites_terreno)
            if colisiono:
                jugador.ssj_count += 1
            
            if self.is_lvl_3:
                headshot = proyectil.verificar_objetivo(self.jefe, self.sprites_terreno, True)
                if headshot == 'headshot':
                    self.jugador.sprite.gd_counter += 1
                    if self.jugador.sprite.gd_counter > UMBRAL_GENKI_DAMA:
                        self.jugador.sprite.gd_counter = UMBRAL_GENKI_DAMA
        
        if not self.menu_victoria:
            self.menu_victoria = jugador.verificar_colision_final(self.final)
    
    def dibujar_tiempo(self):
        if int(self.tiempo) > self.tiempo_anterior:
            self.tiempo_anterior = int(self.tiempo)
            blit = str(self.tiempo_anterior)
            self.texto_blit = self.font.render(blit, False, 'black')
            
        pygame.draw.rect(self.pantalla, 'grey', self.bg_rect, border_radius=8)
        pygame.draw.rect(self.pantalla, 'black', self.bg_rect_2, 5, 8)
        self.pantalla.blit(self.texto_blit, (586, 9))
    
    def stop(self):
        self.running = False
        self.bg_audio.stop()
    
    def run(self, dt, eventos):
        if self.running:
            self.get_input(dt, eventos)
            
            # camara
            self.desplazar_x(dt)
            
            # Checkeo todo tipo de colisiones
            self.colisiones(dt)
            
            # update and draw all the stuff
            self.draw_all(dt)
            
            if self.is_lvl_3:
                #-- jefe --
                self.jefe.verificar_colision_jugador(self.jugador)
                
                if not self.flag_invencibilidad:
                    jugador_herido = self.jefe.verificar_colision_rayo(self.jugador)
                    if jugador_herido:
                        self.flag_invencibilidad = not self.flag_invencibilidad
                else:
                    self.jugador.sprite.herido = True
                    self.tiempo_invencibilidad += dt
                    if self.tiempo_invencibilidad > 1:
                        self.tiempo_invencibilidad = 0
                        self.flag_invencibilidad = False
                
                self.jefe.update_jefe(dt, self.desplazamiento_mundo, self.pantalla)
                self.jefe.draw_jefe(self.pantalla)
                #-- ---- --
            
            self.tiempo += dt
            self.dibujar_tiempo()
            
            if self.modo and self.jugador:
                jugador = self.jugador.sprite
                
                pygame.draw.rect(self.pantalla, (0, 0, 255), jugador.rect, 2)
                
                for enemigo in self.sprites_enemigos:
                    pygame.draw.rect(self.pantalla, (255, 0, 0), enemigo.rect, 2)
                for item in self.sprites_items:
                    pygame.draw.rect(self.pantalla, (0, 255, 255), item.rect, 2)
                for proyectil in jugador.proyectiles:
                    pygame.draw.rect(self.pantalla, (255, 255, 255), proyectil.rect, 2)
                for trampa in self.sprites_pinchos:
                    pygame.draw.rect(self.pantalla, (255, 0, 0), trampa.rect, 2)
                for enemigo in self.sprites_enemigos:
                    pygame.draw.rect(self.pantalla, (255, 0, 0), enemigo.rect, 2)
                for hongo in self.sprites_fg_hongos:
                    pygame.draw.rect(self.pantalla, (0, 255, 0), hongo.rect, 2)
                
                if self.is_nivel_2:
                    for trampa in self.sprites_trampa_laser:
                        pygame.draw.rect(self.pantalla, (255, 0, 0), trampa.rect, 2)
                elif self.is_lvl_3:
                    pygame.draw.rect(self.pantalla, (255, 0, 0), self.jefe.rect, 2)
                    pygame.draw.rect(self.pantalla, (255, 0, 0), self.jefe.rayo_rect, 2)
                    pygame.draw.rect(self.pantalla, (0, 255, 0), self.jefe.head_rect, 2)
