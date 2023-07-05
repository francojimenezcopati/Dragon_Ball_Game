import pygame, os
from pygame.image import load
from ajustes import *


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def cargar_animaciones_personaje(
    path, width, height, direction=False, enemigo=False
):
    lista_carpetas = os.listdir(path)

    all_sprites = {}

    for sprite in lista_carpetas:
        lista_archivos = os.listdir(f"{path}\{sprite}")
        sprites = []
        for archivo in lista_archivos:
            imagen = load(f"{path}\{sprite}\{archivo}").convert_alpha()
            if not enemigo:
                imagen = pygame.transform.scale(imagen, (width, height))
            sprites.append(imagen)
        if direction:
            all_sprites[sprite + "_derecha"] = sprites
            all_sprites[sprite + "_izquierda"] = flip(sprites)
        else:
            all_sprites[sprite] = sprites

    return all_sprites


def cargar_terreno(path):
    terreno = load(path).convert_alpha()
    numero_de_cortes_x = int(terreno.get_width() / TILE_SIZE)
    numero_de_cortes_y = int(terreno.get_height() / TILE_SIZE)

    tiles = []
    for fila in range(numero_de_cortes_y):
        for col in range(numero_de_cortes_x):
            x = col * TILE_SIZE
            y = fila * TILE_SIZE
            cuadrante = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            cuadrante.blit(
                terreno, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            )
            tiles.append(cuadrante)
    return tiles


def cargar_imagenes_carpeta(path):
    lista_archivos = os.listdir(path)

    sprites = []
    for archivo in lista_archivos:
        imagen = load(f"{path}\{archivo}").convert_alpha()
        sprites.append(imagen)

    return sprites


def escalar_genkidama(frames):
    lista = []
    for img in frames:
        img = pygame.transform.scale(img, (60, 60))
        lista.append(img)
    return lista


def agrandar_jefe(frames):
    lista = []
    for img in frames:
        img = pygame.transform.rotozoom(img, 0, 4.195)
        lista.append(img)
    return lista


def reescalar_imagenes(dict_animaciones):
    dict_scaled = {}

    for key, value in dict_animaciones.items():
        i = 0
        lista = []
        for imagen in value:
            if key == "muerte_derecha" or key == "muerte_izquierda":
                lista.append(imagen)
            else:
                i += 1
                lista.append(pygame.transform.scale(imagen, (44, 75)))

        dict_scaled[key] = lista

    return dict_scaled


# cargar_imagenes_carpeta('')
