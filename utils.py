from config import *
import json

def alternar_efectos_sonido(mute):
    global pikcup_sound, transformacion_sound, daño_sound, enemy_shoot_sound, bullet_impact_sound
    if not mute:
        pikcup_sound.set_volume(0.5)
        transformacion_sound.set_volume(0.2)
        daño_sound.set_volume(0.2)
        
        enemy_shoot_sound.set_volume(0.05)
        
        bullet_impact_sound.set_volume(0.2)
    else:
        pikcup_sound.set_volume(0)
        transformacion_sound.set_volume(0)
        daño_sound.set_volume(0)
        
        enemy_shoot_sound.set_volume(0)
        
        bullet_impact_sound.set_volume(0)


def alternar_bg_music(mute):
    global bg_audio_game
    if not mute:
        bg_audio_game.set_volume(0.1)
    else:
        bg_audio_game.set_volume(0)


def guardar_puntaje(nivel, tiempo, score):
    dict_jugador = {
        'Nombre': f'Pepe_1',
        'Tiempo': tiempo,
        'Score': score
    }
    
    data = leer_puntaje(nivel)
    if not data:
        data = {
            'Jugadores': [dict_jugador]
        }
    else:
        dict_jugador['Nombre'] = f'Pepe_{len(data["Jugadores"])+1}'
        data['Jugadores'].append(dict_jugador)
    
    with open(f'Dragon_Ball/{nivel}_data.json', 'w') as archivo:
        json.dump(data, archivo, indent=4)

def leer_puntaje(nivel):
    try:
        with open(f'Dragon_Ball/{nivel}_data.json') as archivo:
            data = json.load(archivo)
        return data
    except:
        return None

