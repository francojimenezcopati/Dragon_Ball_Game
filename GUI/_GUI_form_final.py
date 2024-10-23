import pygame, sys, json
from pygame.locals import *

from .GUI_button import *
from .GUI_button_image import *
from .GUI_form import *
from .GUI_label import *
from .GUI_slider import *
from .GUI_widget import *
from ._GUI_modales import Modal
from .ajustes import *


class FormFinal(Form):
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

        # img = pygame.image.load('resources\GUI\Menu_opciones.png').convert_alpha()
        # self.img = pygame.transform.scale(img, (w, h))

    def inicializar(self, nivel):
        dict_score = leer_puntaje(nivel)
        dict_score = dict_score["Jugadores"]
        self.menu_principal = False

        form_score = Modal(
            self._master,
            self._x,
            self._y,
            self._w,
            self._h,
            "purple",
            "white",
            True,
            "GUI\Window.png",
            dict_score,
            100,
            10,
            10,
            self.checkear_home,
        )

        self.show_dialog(
            form_score
        )  # -> Muestra un formulario y desaparece el otro

    def checkear_home(self, home):
        if home:
            self.menu_principal = True

    def btn_salir_click(self, texto):
        pygame.quit()
        sys.exit()

    def update(self, lista_eventos):
        if self.verificar_dialog_result():  # -> si tengo un modal
            if self.active:
                self.draw()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
        else:
            self.hijo.update(lista_eventos)
        return self.menu_principal


def leer_puntaje(nivel):
    try:
        with open(f"{nivel}_data.json") as archivo:
            data = json.load(archivo)
        return data
    except:
        return None
