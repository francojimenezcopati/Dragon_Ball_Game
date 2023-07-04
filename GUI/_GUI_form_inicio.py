import pygame, sys
from pygame.locals import *

from .GUI_button import *
from .GUI_button_image import *
from .GUI_form import *
from .GUI_label import *
from .GUI_slider import *
from .GUI_widget import *
from ._GUI_modales import *
from .ajustes import *


class FormInicio(Form):
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
        
        
        self.tiempo_parpadeo = 0
        
        bg = pygame.image.load('Dragon_Ball\\resources\GUI\menu_start.png')
        self.bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.play = pygame.image.load('Dragon_Ball\\resources\GUI\start.png')
        self.play = pygame.transform.scale2x(self.play)
        

        self.render()

    def render(self):
        self._slave.blit(self.bg, (0,0))

    def update(self, dt, eventos):
        
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 1

        self.draw()
        self.render()
        self.tiempo_parpadeo += dt
        blit = False
        if self.tiempo_parpadeo > 0.5:
            blit = True
            if self.tiempo_parpadeo > 1:
                self.tiempo_parpadeo = 0
        if blit:
            self._slave.blit(self.play, (512, 500))
        return 0