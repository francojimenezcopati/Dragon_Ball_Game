import pygame
from ajustes import *
from pygame.draw import rect as drect


def imprimir_interfaz(
    pantalla, vida, contador_ssj, esta_ssj, gd_bool, gd_counter=None
):
    # Barra vida
    corazon = pygame.image.load(
        "Dragon_Ball\\resources\HUD\pixel_art_corazon.png"
    )
    corazon = pygame.transform.rotozoom(corazon, 0, 0.1)
    altura = 20
    if not esta_ssj:
        rect = pygame.Rect(8, altura - 2, 100 * VIDA_BASE_JUGADOR + 4, 22)
        drect(pantalla, "black", rect, 0, 12)
        rect = pygame.Rect(10, altura, 100 * VIDA_BASE_JUGADOR, 18)
        drect(pantalla, "grey", rect, 0, 12)
    else:
        rect = pygame.Rect(8, altura - 2, 100 * VIDA_SSJ_JUGADOR + 4, 22)
        drect(pantalla, "black", rect, 0, 12)
        rect = pygame.Rect(10, altura, 100 * VIDA_SSJ_JUGADOR, 18)
        drect(pantalla, "grey", rect, 0, 12)

    rect = pygame.Rect(10, altura, 100 * vida, 18)
    drect(pantalla, "red", rect, 0, 12)

    pantalla.blit(corazon, (5, 10))

    # Barra SSJ
    ssj = pygame.image.load("Dragon_Ball\\resources\HUD\ssj_simbolo.png")
    ssj = pygame.transform.rotozoom(ssj, 0, 0.1)

    rect = pygame.Rect(SCREEN_WIDTH - 314, altura - 2, 304, 22)
    drect(pantalla, "black", rect, 0, 12)
    rect = pygame.Rect(SCREEN_WIDTH - 312, altura, 300, 18)
    drect(pantalla, "grey", rect, 0, 12)
    rect = pygame.Rect(SCREEN_WIDTH - 312, altura, 50 * contador_ssj, 18)
    drect(pantalla, "yellow", rect, 0, 12)

    pantalla.blit(ssj, (SCREEN_WIDTH - 325, -4))

    # Barra genkidama
    if gd_bool:
        gd = pygame.image.load("Dragon_Ball\\resources\proyectiles\\5.png")
        gd = pygame.transform.rotozoom(gd, 0, 0.45)

        rect = pygame.Rect(SCREEN_WIDTH - 314, altura * 4 - 2, 304, 22)
        drect(pantalla, "black", rect, 0, 12)
        rect = pygame.Rect(SCREEN_WIDTH - 312, altura * 4, 300, 18)
        drect(pantalla, "grey", rect, 0, 12)
        rect = pygame.Rect(
            SCREEN_WIDTH - 312, altura * 4, 12.5 * gd_counter, 18
        )
        drect(pantalla, "cyan", rect, 0, 12)

        pantalla.blit(gd, (SCREEN_WIDTH - 330, 55))


def crear_interfaz():
    pass
