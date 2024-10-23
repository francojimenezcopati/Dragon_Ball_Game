import pygame, sys
from pygame.locals import *

from .GUI_button import *
from .GUI_button_image import *
from .GUI_form import *
from .GUI_label import *
from .GUI_slider import *
from .GUI_widget import *
from ._GUI_modales import *
from ._GUI_form_final import leer_puntaje
from .ajustes import *


class FormPrincipal(Form):
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

        img = pygame.image.load("resources\GUI\menu_general.png")
        self.img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.lvl_actual = None

        self.flag_cambio_nivel = False

        self.volumen = 0.1
        self.volumen_anterior = self.volumen
        self.flag_play = True

        pygame.mixer.init()
        self.bg_music = pygame.mixer.Sound(
            "resources\GUI\musica\\bg_menu_music.mp3"
        )
        self.bg_music.set_volume(self.volumen)
        self.bg_music.play(-1)

        self.btn_niveles = Button_Image(
            self._slave,
            x,
            y,
            CENTRAR_BOTON,
            150,
            LARGO_BOTON,
            ALTURA_BOTON,
            "resources\GUI\\botones\Defined\\niveles.png",  # -> LE PUEDO PONER CUALQUIER IMAGEN
            self.btn_niveles_click,
            "a",
        )
        self.btn_opciones = Button_Image(
            self._slave,
            x,
            y,
            CENTRAR_BOTON,
            150 + ESPACIO_ENTRE_BOTONES_Y,
            LARGO_BOTON,
            ALTURA_BOTON,
            "resources\GUI\\botones\Defined\opciones.png",  # -> LE PUEDO PONER CUALQUIER IMAGEN
            self.btn_opciones_click,
            "a",
        )
        self.btn_salir = Button_Image(
            self._slave,
            x,
            y,
            CENTRAR_BOTON,
            150 + ESPACIO_ENTRE_BOTONES_Y * 2,
            LARGO_BOTON,
            ALTURA_BOTON,
            "resources\GUI\\botones\Defined\salir.png",  # -> LE PUEDO PONER CUALQUIER IMAGEN
            self.btn_salir_click,
            "a",
        )

        self.lista_widgets.append(self.btn_niveles)
        self.lista_widgets.append(self.btn_opciones)
        self.lista_widgets.append(self.btn_salir)

        self.render()

    def btn_niveles_click(self, texto):
        niveles_menu = ModalBotones(
            self._master,
            0,
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            "white",
            "white",
            True,
            "resources\GUI\menu_general.png",
            funcion=self.set_lvl_actual,
            volumen=self.volumen,
        )

        self.show_dialog(
            niveles_menu
        )  # -> Muestra un formulario y desaparece el otro

    def btn_opciones_click(self, texto):
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
        )
        
        self.show_dialog(
            opciones_menu
        )  # -> Muestra un formulario y desaparece el otro

    def btn_salir_click(self, texto):
        pygame.quit()
        sys.exit()

    def update(self, lista_eventos):
        if self.verificar_dialog_result():  # -> si tengo un modal
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
        else:
            self.hijo.update(lista_eventos)

        if self.flag_cambio_nivel:
            self.flag_cambio_nivel = False
            return self.lvl_actual

    def set_lvl_actual(self, numero: int):
        if numero == 1:
            if leer_puntaje(f"nivel_1"):
                self.lvl_actual = numero
                self.flag_cambio_nivel = True
            else:
                print("Completar el nivel 1 primero")
        elif numero == 2:
            if leer_puntaje(f"nivel_1") and leer_puntaje(f"nivel_2"):
                self.lvl_actual = numero
                self.flag_cambio_nivel = True
            else:
                print("Completar los niveles 1 y 2 primero")
        elif numero == 0:
            self.lvl_actual = numero
            self.flag_cambio_nivel = True

    def funcion_opciones(self, cambios_v, cambios_m, musica, vm, efectos, ve):
        if cambios_m:
            if not musica:
                self.bg_music.set_volume(0)
            else:
                self.bg_music.set_volume(self.volumen)
            self.flag_play = not self.flag_play
        elif cambios_v:
            self.volumen = vm
            self.bg_music.set_volume(self.volumen)

    def render(self):
        self._slave.blit(self.img, (0, 0))
        # self._slave.fill(self._color_background)
