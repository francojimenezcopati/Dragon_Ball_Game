import pygame
from pygame.locals import *

from ajustes import *
from GUI._GUI_form_principal import *
from GUI._GUI_form_inicio import *
from GUI._GUI_form_final import *
from GUI._GUI_form_pausa import FormPausa
from _4_Nivel import Nivel
from lvl_data import *
from interfaz import *
from GUI.config import *
from error import error
from GUI.utils import *


class SceneManager:
    def __init__(self):
        self.lista_niveles = [lvl_0, lvl_1, lvl_2]
        self.nivel = None

        self.lore_inicio = pygame.image.load(
            "resources\GUI\Lore\Lore_1.png"
        ).convert()
        self.lore_mid = pygame.image.load(
            "resources\GUI\Lore\Lore_2.png"
        ).convert()
        self.lore_final = pygame.image.load(
            "resources\GUI\Lore\Lore_3.png"
        ).convert()
        
        print()
        print("--- TECLAS ---")
        print("Disparo: 'F'")
        print("Convertirse en SSJ: 'D'")
        print("Genki Dama (lvl 3): 'S'")
        print()

        self.flag_lore = True

        self.flag_pausa = False
        self.flag_pausa_init = False

        alternar_efectos_sonido(False)
        alternar_bg_music(False)

        # ------ GUI --------

        self.forms = [
            FormInicio(
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
            FormPausa(pantalla, 300, 50, 600, 600, "white", "red", 5),
        ]

        self.form_actual = self.forms[0]

        # -------------------

    def run(self, dt, eventos):
        global scene_switch
        global home
        global flag_victoria
        global jugador

        try:
            match scene_switch:
                case 0:
                    scene_switch = self.form_actual.update(dt, eventos)
                case 1:
                    self.menu_principal(eventos)
                case 2:
                    self.lore_scene(eventos)
                case 3:
                    self.nivel_run(dt, eventos)

                    if self.nivel.menu_victoria:
                        self.victoria(eventos)
        except Exception:
            self.forms[1].bg_music.set_volume(0)
            error()

    def menu_principal(self, eventos):
        global scene_switch
        global flag_victoria
        global home

        self.form_actual = self.forms[1]
        if home:  # Cuando se toca la casita al final del nivel para volver
            self.form_actual.bg_music.play(-1)
            self.flag_pausa_init = False
            self.flag_pausa = False
            flag_victoria = True
            home = False
        self.lvl_elegido = self.form_actual.update(eventos)
        if self.lvl_elegido != None:
            scene_switch = 2

            self.form_actual.bg_music.stop()

            if self.lista_niveles[self.lvl_elegido] == lvl_1:
                scene_switch = 3
                self.nivel_3 = False
                self.nivel_2 = True
                self.nivel = Nivel(
                    self.lista_niveles[self.lvl_elegido],
                    pantalla,
                    self.nivel_2,
                    self.nivel_3,
                )
            elif self.lista_niveles[self.lvl_elegido] == lvl_2:
                self.nivel_3 = True
                self.nivel_2 = False
            else:
                self.nivel_2 = False
                self.nivel_3 = False

    def lore_scene(self, eventos):
        global scene_switch

        if self.nivel_3:
            lore = self.lore_mid
        else:
            lore = self.lore_inicio
        if self.flag_lore:
            pantalla.blit(lore, (0, 0))
            self.flag_lore = False

        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scene_switch = 3
                    self.flag_lore = True
                    self.nivel = Nivel(
                        self.lista_niveles[self.lvl_elegido],
                        pantalla,
                        self.nivel_2,
                        self.nivel_3,
                    )

    def nivel_run(self, dt, eventos):
        global jugador

        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.flag_pausa = not self.flag_pausa
                    self.nivel.alternar_pausa()

        if self.flag_pausa:
            self.pausa(eventos)

        if jugador:
            self.nivel.run(dt, eventos)
            jugador = self.nivel.jugador.sprite
        if jugador:
            if self.nivel.running:
                imprimir_interfaz(
                    pantalla,
                    jugador.vida,
                    jugador.ssj_count,
                    jugador.esta_ssj,
                    self.nivel_3,
                    jugador.gd_counter,
                )
        else:  # Si el sprite del jugador se murio, se resetea el nivel
            self.nivel.stop()
            self.nivel = Nivel(
                self.lista_niveles[self.lvl_elegido],
                pantalla,
                self.nivel_2,
                self.nivel_3,
            )
            jugador = self.nivel.jugador.sprite

    def pausa(self, eventos):
        global scene_switch
        global home

        if not self.flag_pausa_init:
            self.flag_pausa_init = True
            self.forms[3].inicializar()
        home = self.forms[3].update(eventos)
        if home:
            self.nivel.stop()
            scene_switch = 1

    def victoria(self, eventos):
        global scene_switch
        global home
        global flag_victoria
        try:
            jugador = self.nivel.jugador.sprite
            self.nivel.stop()

            if flag_victoria:
                flag_victoria = False
                if self.nivel_2:
                    nivel = "nivel_2"
                elif self.nivel_3:
                    nivel = "nivel_3"
                else:
                    nivel = "nivel_1"

                guardar_puntaje(nivel, int(self.nivel.tiempo), jugador.score)

                self.form_actual = self.forms[2]

                self.form_actual.tiempo_jugador = str(int(self.nivel.tiempo))
                self.form_actual.inicializar(nivel)
            

            home = self.form_actual.update(eventos)
            if home:
                if self.nivel_3:
                    self.lore_3(eventos)
                else:
                    scene_switch = 1
        except Exception as e:
            print(e)


    def lore_3(self, eventos):
        global scene_switch

        if self.flag_lore:
            self.flag_lore = False
            pantalla.blit(self.lore_final, (0, 0))

        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scene_switch = 1
                    self.flag_lore = True
