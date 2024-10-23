import pygame, json
from pygame.locals import *
from pygame.image import load

from .GUI_button import *
from .GUI_button_image import *
from .GUI_form import *
from .GUI_label import *
from .GUI_slider import *
from .GUI_widget import *
from .ajustes import *


class Modal(Form):
    def __init__(
        self,
        screen,
        x,
        y,
        w,
        h,
        color_background,
        color_border,
        active,
        path,
        score,
        margen_y,
        margen_x,
        espacio,
        return_funcion,
    ):
        super().__init__(
            screen, x, y, w, h, color_background, color_border, active
        )

        self.return_funcion = return_funcion

        aux_imagen = load(path)
        aux_imagen = pygame.transform.scale(aux_imagen, (w, h))

        self._slave = aux_imagen
        self.score = score

        self._margen_y = margen_y
        self._margen_x = margen_x

        self.lbl_col1 = Label(
            self._slave,
            self._margen_x + 10,
            20,
            w / 3 - self._margen_x - 10,
            50,
            "Jugador",
            "Verdana",
            30,
            "white",
            "GUI/bar.png",
        )
        self.lbl_col2 = Label(
            self._slave,
            self._margen_x + 10 + w / 3 - self._margen_x - 10,
            20,
            w / 3 - self._margen_x - 10,
            50,
            "Tiempo",
            "Verdana",
            30,
            "white",
            "GUI/bar.png",
        )
        self.lbl_col3 = Label(
            self._slave,
            self._margen_x + 10 + w * 2 / 3 - self._margen_x - 10,
            20,
            w / 3 - self._margen_x - 10,
            50,
            "Score",
            "Verdana",
            30,
            "white",
            "GUI/bar.png",
        )

        self.lista_widgets.append(self.lbl_col1)
        self.lista_widgets.append(self.lbl_col2)
        self.lista_widgets.append(self.lbl_col3)

        pos_inicial_y = margen_y

        for dict in self.score:
            pos_inicial_x = margen_x
            for key, value in dict.items():
                cadena = f"{value}"
                jugador = Label(
                    self._slave,
                    pos_inicial_x,
                    pos_inicial_y,
                    w / 3 - margen_x,
                    100,
                    cadena,
                    "Verdana",
                    30,
                    "white",
                    "GUI/Table.png",
                )
                self.lista_widgets.append(jugador)
                pos_inicial_x += w / 3 - margen_x
            pos_inicial_y += 100 + espacio

        self.btn_home = Button_Image(
            self._slave,
            x,
            y,
            w - 70,
            h - 70,
            50,
            50,
            "GUI/home.png",
            self.btn_home_click,
            "a",
        )
        self.lista_widgets.append(self.btn_home)

    def btn_home_click(self, param):
        self.return_funcion(True)
        self.end_dialog()

    def update(self, lista_eventos):
        if self.active:
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()


class ModalBotones(Form):
    def __init__(
        self,
        screen,
        x,
        y,
        w,
        h,
        color_background,
        color_border,
        active,
        niveles=False,
        opciones=False,
        funcion=None,
        func_opc=None,
        flag_play=None,
        volumen=None,
        pausa=None,
        flag_efectos=None,
        checkear_home=None,
    ):
        super().__init__(
            screen, x, y, w, h, color_background, color_border, active
        )

        self.pausa = pausa
        self.flag_efectos = flag_efectos
        self.checkear_home = checkear_home

        self.mute_efects_img = load(
            "resources\GUI\\botones\\Defined\\Efectos_Mute.png"
        ).convert_alpha()
        self.mute_efects_img = pygame.transform.scale(
            self.mute_efects_img, (96, 96)
        )
        self.unmute_efects_img = load(
            "resources\GUI\\botones\\Defined\\Efectos_Unmute.png"
        ).convert_alpha()
        self.unmute_efects_img = pygame.transform.scale(
            self.unmute_efects_img, (96, 96)
        )

        self.flag_play = flag_play

        mute_img = load(
            "resources\GUI\\botones\\Defined\\Musica_Mute.png"
        ).convert_alpha()
        self.mute_img = pygame.transform.scale(mute_img, (96, 96))
        unmute_img = load(
            "resources\GUI\\botones\\Defined\\Musica_Unmute.png"
        ).convert_alpha()
        self.unmute_img = pygame.transform.scale(unmute_img, (96, 96))

        self.volumen = volumen

        self.func_opc = func_opc
        self.funcion = funcion

        self.niveles = niveles
        self.opciones = opciones

        if self.niveles:
            img = pygame.image.load(self.niveles).convert_alpha()
            self.img = pygame.transform.scale(img, (w, h))
        else:
            img = pygame.image.load(self.opciones).convert_alpha()
            self.img = pygame.transform.scale(img, (w, h))

        self._slave = self.img

        self.img = self.img.convert_alpha()

        if self.niveles:
            x_btn = CENTRAR_BOTON
            y_btn = h - 150
            w_btn = LARGO_BOTON
            h_btn = ALTURA_BOTON
        else:
            x_btn = CENTRAR_BOTON
            y_btn = 40
            w_btn = LARGO_BOTON
            h_btn = ALTURA_BOTON

        if self.niveles:
            if leer_puntaje("nivel_1") != None:
                lvl_1 = "LVL_0_C"
            else:
                lvl_1 = "LVL_0_I"
            if leer_puntaje("nivel_2") != None:
                lvl_2 = "LVL_1_C"
            else:
                lvl_2 = "LVL_1_I"
            if leer_puntaje("nivel_3") != None:
                lvl_3 = "LVL_2_C"
            else:
                lvl_3 = "LVL_2_I"

            self.btn_atras = Button_Image(
                self._slave,
                x,
                y,
                x_btn,
                y_btn,
                w_btn,
                h_btn,
                "resources\GUI\\botones\Defined\\atras.png",
                self.btn_atras_click,
                "abccc",
            )
            self.btn_lvl_3 = Button_Image(
                self._slave,
                x,
                y,
                BOTON_2_CENTRAR,
                y_btn - Y_ESPACIADO_BOTONES_2,
                BOTON_2_ANCHO,
                BOTON_2_ALTO,
                f"resources\GUI\\botones\\Defined\\{lvl_3}.png",
                self.btn_lvl_click,
                "2",
            )
            self.btn_lvl_2 = Button_Image(
                self._slave,
                x,
                y,
                BOTON_2_CENTRAR,
                y_btn - Y_ESPACIADO_BOTONES_2 * 2,
                BOTON_2_ANCHO,
                BOTON_2_ALTO,
                f"resources\GUI\\botones\\Defined\\{lvl_2}.png",
                self.btn_lvl_click,
                "1",
            )
            self.btn_lvl_1 = Button_Image(
                self._slave,
                x,
                y,
                BOTON_2_CENTRAR,
                y_btn - Y_ESPACIADO_BOTONES_2 * 3,
                BOTON_2_ANCHO,
                BOTON_2_ALTO,
                f"resources\GUI\\botones\\Defined\\{lvl_1}.png",
                self.btn_lvl_click,
                "0",
            )
            self.btn_titulo = Button_Image(
                self._slave,
                x,
                y,
                CENTRAR_BOTON,
                y_btn - Y_ESPACIADO_BOTONES_2 * 4,
                LARGO_BOTON,
                ALTURA_BOTON,
                "resources\GUI\\botones\\Defined\\niveles_titulo.png",
            )
            self.lista_widgets.append(self.btn_lvl_1)
            self.lista_widgets.append(self.btn_lvl_2)
            self.lista_widgets.append(self.btn_lvl_3)
        else:
            if self.pausa:
                centrar = 200 - 48
                btn_abajo = "salir"
                boton = "pausa"
            else:
                centrar = 252
                btn_abajo = "atras"
                boton = "opciones"
            self.btn_titulo = Button_Image(
                self._slave,
                x,
                y,
                CENTRAR_BOTON_OPCIONES,
                y_btn,
                LARGO_BOTON,
                ALTURA_BOTON,
                f"resources\GUI\\botones\\Defined\\{boton}_titulo.png",
            )

            if self.flag_play:
                path = "resources\GUI\\botones\\Defined\\Musica_Unmute.png"
            else:
                path = "resources\GUI\\botones\\Defined\\Musica_Mute.png"
            if self.flag_efectos:
                path_e = "resources\GUI\\botones\\Defined\\Efectos_Unmute.png"
            else:
                path_e = "resources\GUI\\botones\\Defined\\Efectos_Mute.png"

            self.btn_mute_music = Button_Image(
                self._slave,
                x,
                y,
                centrar,
                y_btn + 160,
                96,
                96,
                path,
                self.alternar_musica,
                "a",
            )
            if self.pausa:
                self.btn_mute_efects = Button_Image(
                    self._slave,
                    x,
                    y,
                    400 - 48,
                    y_btn + 160,
                    96,
                    96,
                    path_e,
                    self.alternar_efectos,
                    "a",
                )


            self.label_volumen = Label(
                self._slave,
                470,
                347,
                100,
                50,
                "20%",
                "Comic Sans",
                15,
                "white",
                "GUI/Table.png",  # -> LE PUEDO PONER CUALQUIER IMAGEN
            )
            self.slider_volumen = Slider(
                self._slave,
                x,
                y,
                50,
                360,
                400,
                15,
                self.volumen,
                "Blue",
                "cyan",
            )

            self.btn_atras = Button_Image(
                self._slave,
                x,
                y,
                183,
                490,
                LARGO_BOTON * 0.7,
                ALTURA_BOTON * 0.7,
                f"resources\GUI\\botones\Defined\\{btn_abajo}.png",
                self.btn_atras_click,
                "abccc",
            )
            self.lista_widgets.append(self.btn_mute_music)
            if self.pausa:
                self.lista_widgets.append(self.btn_mute_efects)
            self.lista_widgets.append(self.label_volumen)
            self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_atras)
        self.lista_widgets.append(self.btn_titulo)



    def alternar_musica(self, param):
        if self.flag_play:
            self.flag_play = False
            self.btn_mute_music._slave = self.mute_img
        else:
            self.flag_play = True
            self.btn_mute_music._slave = self.unmute_img
        self.func_opc(False, True, self.flag_play, self.volumen, False, False)

    def alternar_efectos(self, param):
        if self.flag_efectos:
            self.flag_efectos = False
            self.btn_mute_efects._slave = self.mute_efects_img
        else:
            self.flag_efectos = True
            self.btn_mute_efects._slave = self.unmute_efects_img
        self.func_opc(False, False, False, False, True, self.flag_efectos)

    def set_volumen(self):
        volumen_previo = self.volumen
        self.volumen = self.slider_volumen.get_value()
        self.label_volumen.update("")
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        if volumen_previo != self.volumen:
            if self.flag_play:
                self.func_opc(
                    True, False, self.flag_play, self.volumen, False, False
                )

    def btn_lvl_click(self, param):
        if param == "0":
            self.funcion(0)
        elif param == "1":
            self.funcion(1)
        else:
            self.funcion(2)

    def btn_atras_click(self, param):
        if self.pausa:
            self.checkear_home(True)
        self.end_dialog()

    def render(self):
        self._slave.blit(self.img, (0, 0))

    def update(self, lista_eventos):
        if self.active:
            self.draw()
            self.render()
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            if self.opciones:
                self.set_volumen()


def leer_puntaje(nivel):
    try:
        with open(f"{nivel}_data.json") as archivo:
            data = json.load(archivo)
        return data
    except:
        return None
