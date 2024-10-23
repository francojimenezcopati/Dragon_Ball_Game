import pygame, sys, json
from pygame.locals import *

from .GUI_button import *
from .GUI_button_image import *
from .GUI_form import *
from .GUI_label import *
from .GUI_slider import *
from .GUI_widget import *
from ._GUI_modales import ModalBotones
from .ajustes import *
from .config import *
from .utils import *


class FormPausa(Form):
    def __init__(
        self,
        screen,
        x,
        y,
        w,
        h,
        color_background,
        color_border="Black",
        border_size=-1,
        active=True,
    ):
        super().__init__(
            screen,
            x,
            y,
            w,
            h,
            color_background,
            color_border,
            border_size,
            active,
        )

        self.menu_principal = False

        self.tiempo_jugador = 1

        self.flag_play = True
        self.flag_efectos = True

        self.volumen = 0.1

        # img = pygame.image.load('resources\GUI\Menu_opciones.png').convert_alpha()
        # self.img = pygame.transform.scale(img, (w, h))

    def inicializar(self):
        self.menu_principal = False

        opciones_menu = ModalBotones(
            self._master,
            300,
            50,
            WIDTH_OPCIONES,
            HEIGHT_OPCIONES,
            "white",
            "white",
            True,
            opciones="resources\GUI\Menu_opciones.png",
            func_opc=self.funcion_opciones,
            flag_play=self.flag_play,
            volumen=self.volumen,
            pausa=True,
            flag_efectos=self.flag_efectos,
            checkear_home=self.checkear_home,
        )

        self.show_dialog(
            opciones_menu
        )  # -> Muestra un formulario y desaparece el otro

    def funcion_opciones(
        self, cambios_v, cambios_m, musica, vm, cambios_e, efectos
    ):
        global bg_audio_game

        if cambios_m:
            if not musica:
                bg_audio_game.set_volume(0)
            else:
                bg_audio_game.set_volume(self.volumen)
            self.flag_play = not self.flag_play
        elif cambios_v:
            self.volumen = vm
            bg_audio_game.set_volume(self.volumen)

        if cambios_e:
            if efectos:
                alternar_efectos_sonido(False)
            else:
                alternar_efectos_sonido(True)
            self.flag_efectos = not self.flag_efectos

    def checkear_home(self, home):
        if home:
            self.menu_principal = True

    def update(self, lista_eventos):
        if self.verificar_dialog_result():  # -> si tengo un modal
            if self.active:
                self.draw()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
        else:
            self.hijo.update(lista_eventos)
        return self.menu_principal
