import pygame
from .ajustes import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
clock = pygame.time.Clock()
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dragon Ball")

# ----- flags -----

flag_victoria = True
scene_switch = 0
home = False
jugador = True

# -----------------


# ----- sonidos -----

# -- efectos --
pikcup_sound = pygame.mixer.Sound("resources\sounds\pickup.wav")
transformacion_sound = pygame.mixer.Sound(
    "resources\sounds\\transformacion.wav"
)
daño_sound = pygame.mixer.Sound("resources\sounds\\daño.wav")

enemy_shoot_sound = pygame.mixer.Sound(
    "resources\sounds\\laser4.wav"
)

bullet_impact_sound = pygame.mixer.Sound(
    "resources\sounds\\bullet_impact.flac"
)
# -- ------- --

bg_audio_game = pygame.mixer.Sound(
    "resources\sounds\\bg_game_music.mp3"
)


# ----- ------- -----
