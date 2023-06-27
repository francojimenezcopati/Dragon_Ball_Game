import pygame, sys
from pygame.locals import *
from ajustes import *
from _4_Nivel import Nivel
from lvl_data import *
from interfaz import *
from GUI._GUI_form_principal import *
from GUI._GUI_form_inicio import *
from GUI._GUI_form_final import *

# from Dragon_Ball.GUI._GUI_form_inicio import *
# from Dragon_Ball.GUI import *

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


lista_niveles = [lvl_0, lvl_1, lvl_2]


# ------ GUI --------

forms = [
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

form_actual = forms[0]

# -------------------


# ----- recursos -------
pygame.display.set_caption("Dragon Ball")

flag_victoria = True
enter = 0
home = False
jugador = False
while True:
    dt = clock.tick(FPS) / 1000

    # print(dt)
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if jugador and event.key == pygame.K_ESCAPE:
                pass
                # enter = 1
                # nivel.bg_audio.stop() TODO --> ----- HACER QUE SE PARE EL JUEGO Y APAREZCA UN MENU DE OPCIONES DISTINTO AL DE ANTES
                # forms[1].btn_opciones_click('')

    if enter == 0:
        enter = form_actual.update(dt, eventos)
    elif enter == 1:
        form_actual = forms[1]
        if home:
            form_actual.bg_music.play(-1)
            home = False
        lvl_elegido = form_actual.update(eventos)
        if lvl_elegido != None:
            enter = 2

            form_actual.bg_music.stop()

            if lista_niveles[lvl_elegido] == lvl_1:
                nivel_3 = False
                nivel_2 = True
            elif lista_niveles[lvl_elegido] == lvl_2:
                nivel_3 = True
                nivel_2 = False
            else:
                nivel_2 = False
                nivel_3 = False

            jugador = True
            nivel = Nivel(
                lista_niveles[lvl_elegido], pantalla, nivel_2, nivel_3
            )
    elif enter == 2:
        if jugador:
            nivel.run(dt, eventos)
            jugador = nivel.jugador.sprite

        if jugador:
            imprimir_interfaz(
                pantalla,
                jugador.vida,
                jugador.ssj_count,
                jugador.esta_ssj,
                nivel_3,
                jugador.gd_counter,
            )
        else:  # Si el sprite del jugador se murio, se resetea el nivel
            nivel.bg_audio.stop()
            nivel = Nivel(
                lista_niveles[lvl_elegido], pantalla, nivel_2, nivel_3
            )
            jugador = nivel.jugador.sprite

        if nivel.menu_victoria:  # Aca llego a la meta del nivel, mostrar menu
            nivel.pantalla.fill("grey")
            nivel.stop()

            if flag_victoria:
                flag_victoria = False

                form_actual = forms[2]

                form_actual.tiempo_jugador = str(int(nivel.tiempo))
                form_actual.inicializar()

            home = form_actual.update(eventos)
            if home:
                enter = 1

    pygame.display.flip()
