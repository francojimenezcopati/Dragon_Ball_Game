import pygame
from _1_ObjetoJuego import Objeto
from _2_Personaje import Personaje

class Item(Objeto):
    def __init__(self, pos, imagen):
        super().__init__(pos, (40,40), imagen)
    
