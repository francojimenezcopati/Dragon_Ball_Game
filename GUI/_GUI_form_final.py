import pygame, sys
from pygame.locals import *

from .GUI_button import *
from .GUI_button_image import *
from .GUI_form import *
from .GUI_label import *
from .GUI_slider import *
from .GUI_widget import *
from ._GUI_modal_score import *
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
        
        # img = pygame.image.load('Dragon_Ball\\resources\GUI\Menu_opciones.png').convert_alpha()
        # self.img = pygame.transform.scale(img, (w, h))
        
        
        # self.btn_salir = Button_Image(
        #     self._slave,
        #     x,
        #     y,
        #     183,
        #     490,
        #     LARGO_BOTON*0.7,
        #     ALTURA_BOTON*0.7,
        #     "Dragon_Ball\\resources\GUI\\botones\Defined\salir.png",# -> LE PUEDO PONER CUALQUIER IMAGEN
        #     self.btn_salir_click,
        #     "a"
        # )

        # self.lista_widgets.append(self.btn_salir)
        # # self.lista_widgets.append(self.btn_tabla)
        

    def inicializar(self):
        dict_score = [
            {"Jugador": "Pepe", "Tiempo": self.tiempo_jugador},
        ]
        form_score = Modal(
            self._master,
            self._x,
            self._y,
            self._w,
            self._h,
            "purple",
            "white",
            True,
            "menu\API FORMS\Window.png",
            dict_score,
            100,
            10,
            10,
            self.checkear_home
        )

        self.show_dialog(form_score)#-> Muestra un formulario y desaparece el otro

    def checkear_home(self, home):
        if home:
            self.menu_principal = True

    def btn_salir_click(self, texto):
        pygame.quit()
        sys.exit()
    
    def update(self, lista_eventos):
        if self.verificar_dialog_result(): #-> si tengo un modal
            if self.active:
                self.draw()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                # self.set_volumen(lista_eventos) -> TODO
        else:
            self.hijo.update(lista_eventos)
        return self.menu_principal


