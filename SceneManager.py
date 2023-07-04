import pygame
from pygame.locals import *

from ajustes import *
from GUI._GUI_form_principal import *
from GUI._GUI_form_inicio import *
from GUI._GUI_form_final import *
from _4_Nivel import Nivel
from lvl_data import *
from interfaz import *
from config import *
from error import error
from utils import * 

class SceneManager():
    def __init__(self):
        self.lista_niveles = [lvl_0, lvl_1, lvl_2]
        self.nivel = None

        alternar_efectos_sonido(False)
        alternar_bg_music(False)

        # ------ GUI --------

        self.forms = [
            FormInicio(
                pantalla, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, "white", "red", 5, True
            ),
            FormPrincipal(
                pantalla,
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                "white",
                "red",
                5,
                True,
            ),
            FormFinal(pantalla, 300, 50, 600, 600, "white", "red", 5),
        ]

        self.form_actual = self.forms[0]

        # -------------------
    
    def run(self, dt, eventos):
        global scene_switch
        global home
        global flag_victoria
        global jugador
        # try:
        if scene_switch == 0:
            scene_switch = self.form_actual.update(dt, eventos)
        elif scene_switch == 1:
            self.menu_principal(eventos)
        elif scene_switch == 2:
            self.nivel_run(dt, eventos)

            if self.nivel.menu_victoria:  # Aca llego a la meta del nivel, mostrar menu
                self.victoria(eventos)
        # except Exception:
        #     error()
    
    
    def menu_principal(self, eventos):
        global scene_switch
        global flag_victoria
        global home
        self.form_actual = self.forms[1]
        if home: # Cuando se toca la casita al final del nivel para volver
            self.form_actual.bg_music.play(-1)
            flag_victoria = True
            home = False
        self.lvl_elegido = self.form_actual.update(eventos)
        if self.lvl_elegido != None:
            scene_switch = 2

            self.form_actual.bg_music.stop()

            if self.lista_niveles[self.lvl_elegido] == lvl_1:
                self.nivel_3 = False
                self.nivel_2 = True
            elif self.lista_niveles[self.lvl_elegido] == lvl_2:
                self.nivel_3 = True
                self.nivel_2 = False
            else:
                self.nivel_2 = False
                self.nivel_3 = False

            self.nivel = Nivel(
                self.lista_niveles[self.lvl_elegido], pantalla, self.nivel_2, self.nivel_3
            )
    
    
    def nivel_run(self, dt, eventos):
        global jugador
        if jugador:
                self.nivel.run(dt, eventos)
                jugador = self.nivel.jugador.sprite

        if jugador:
            imprimir_interfaz(
                pantalla,
                jugador.vida,
                jugador.ssj_count,
                jugador.esta_ssj,
                self.nivel_3,
                jugador.gd_counter,
            )
        else:  # Si el sprite del jugador se murio, se resetea el nivel
            bg_audio_game.stop()
            self.nivel = Nivel(
                self.lista_niveles[self.lvl_elegido], pantalla, self.nivel_2, self.nivel_3
            )
            jugador = self.nivel.jugador.sprite
    
    
    def victoria(self, eventos):
        global scene_switch
        global home
        global flag_victoria
        self.nivel.pantalla.fill("grey")
        jugador = self.nivel.jugador.sprite
        self.nivel.stop()

        if flag_victoria:
            flag_victoria = False
            if self.nivel_2:
                nivel = 'nivel_2'
            elif self.nivel_3:
                nivel = 'nivel_3'
            else:
                nivel = 'nivel_1'
            guardar_puntaje(nivel, int(self.nivel.tiempo), jugador.score)

            self.form_actual = self.forms[2]

            self.form_actual.tiempo_jugador = str(int(self.nivel.tiempo))
            self.form_actual.inicializar(nivel)

        home = self.form_actual.update(eventos)
        if home:
            scene_switch = 1