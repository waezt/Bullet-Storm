import pygame
pygame.init()
pygame.mixer.init()

#PLAYER IDLE ANIMATIONS

PLAYER_1_FRAME1 = pygame.image.load('2dassets/idle/enemy1idle1.png')
PLAYER_1_FRAME2 = pygame.image.load('2dassets/idle/enemy1idle2.png')
PLAYER_1_FRAME3 = pygame.image.load('2dassets/idle/enemy1idle3.png')
PLAYER_1_FRAME4 = pygame.image.load('2dassets/idle/enemy1idle4.png')

#PLAYER MOVING ANIMATIONS

PLAYER_1_MOVE_FRAME1 = pygame.image.load('2dassets/walk/enemy1walk1.png')
PLAYER_1_MOVE_FRAME2 = pygame.image.load('2dassets/walk/enemy1walk2.png')
PLAYER_1_MOVE_FRAME3 = pygame.image.load('2dassets/walk/enemy1walk3.png')
PLAYER_1_MOVE_FRAME4 = pygame.image.load('2dassets/walk/enemy1walk4.png')

#BULLETS

BULLET_1 = pygame.image.load('2dassets/Laser Sprites/01.png')
BULLET_2 = pygame.image.load('2dassets/Laser Sprites/02.png')
BULLET_3 = pygame.image.load('2dassets/Laser Sprites/64.png')


#MAP

BACKGROUND_1 = pygame.image.load('2dassets/SpaceMap.png')


#ENEMIES

ENEMY_1_FRAME_1 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export1.png')
ENEMY_1_FRAME_2 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export2.png')
ENEMY_1_FRAME_3 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export3.png')
ENEMY_1_FRAME_4 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export4.png')
ENEMY_1_FRAME_5 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export5.png')
ENEMY_1_FRAME_6 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export6.png')
ENEMY_1_FRAME_7 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export7.png')
ENEMY_1_FRAME_8 = pygame.image.load('2dassets/tanknsoldier/tank/tank1/tank1-export8.png')

ENEMY_2_FRAME_1 = pygame.image.load('2dassets/tanknsoldier/drone/drone2/drone2-export1.png')
ENEMY_2_FRAME_2 = pygame.image.load('2dassets/tanknsoldier/drone/drone2/drone2-export2.png')
ENEMY_2_FRAME_3 = pygame.image.load('2dassets/tanknsoldier/drone/drone2/drone2-export3.png')
ENEMY_2_FRAME_4 = pygame.image.load('2dassets/tanknsoldier/drone/drone2/drone2-export4.png')

ENEMY_3_FRAME_1 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export1.png')
ENEMY_3_FRAME_2 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export2.png')
ENEMY_3_FRAME_3 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export3.png')
ENEMY_3_FRAME_4 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export4.png')
ENEMY_3_FRAME_5 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export5.png')
ENEMY_3_FRAME_6 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export6.png')
ENEMY_3_FRAME_7 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export7.png')
ENEMY_3_FRAME_8 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export8.png')
ENEMY_3_FRAME_9 = pygame.image.load('2dassets/tanknsoldier/tank/tank4/tank4-export9.png')

BOSS_IMAGE = pygame.image.load('2dassets/BOSS_1.png')

#UI

HEALTH_BAR_1 = pygame.image.load('2dassets/greenbar (3).png')
HEALTH_BAR_2 = pygame.image.load('2dassets/greenbar (2).png')
FONT = pygame.font.Font("2dassets/pixel_font.ttf", 30)
LARGE_FONT = pygame.font.Font("2dassets/pixel_font.ttf", 70)
MEDIUM_FONT = pygame.font.Font("2dassets/pixel_font.ttf", 50)
CROSS_IMAGE = pygame.image.load('2dassets/CROSS.png')
CROSS_IMAGE = pygame.transform.scale(CROSS_IMAGE, (50, 50))
GAME_OVER_IMAGE = pygame.image.load('2dassets/game_over_ss.png')
BUTTON_IDLE = pygame.image.load('2dassets/UI Elements/layer3.png')
BUTTON_IDLE = pygame.transform.scale(BUTTON_IDLE, (420, 100))
BUTTON_PRESSED = pygame.image.load('2dassets/UI Elements/layer4.png')
BUTTON_PRESSED = pygame.transform.scale(BUTTON_PRESSED, (420, 100))
BLANK_MENU = pygame.image.load('2dassets/BLANK MENU.png')
MENU_1 = pygame.image.load('2dassets/menu3 2.png')
MENU_2 = pygame.image.load('2dassets/STATS_SCREEN.png')
MENU_3 = pygame.image.load('2dassets/settings _menu_image.png')

SMALL_BUTTON_IDLE = pygame.image.load('2dassets/UI Elements/layer3.png')
SMALL_BUTTON_IDLE = pygame.transform.scale(SMALL_BUTTON_IDLE, (380, 60))
SMALL_BUTTON_PRESSED = pygame.image.load('2dassets/UI Elements/layer4.png')
SMALL_BUTTON_PRESSED = pygame.transform.scale(SMALL_BUTTON_PRESSED, (380, 60))

#POWER UPS

ENERGY_FRAME_1 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export1.png')
ENERGY_FRAME_2 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export2.png')
ENERGY_FRAME_3 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export3.png')
ENERGY_FRAME_4 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export4.png')
ENERGY_FRAME_5 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export5.png')
ENERGY_FRAME_6 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export6.png')
ENERGY_FRAME_7 = pygame.image.load('2dassets/tanknsoldier/icon/energy/energy-export7.png')

STRENGTH_BOOST = pygame.image.load('2dassets/tanknsoldier/icon/potion_03a.png')

SPEED_BOOTS = pygame.image.load('2dassets/tanknsoldier/icon/boots_01d.png')

#SOUNDS

GUN_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/gun_shot.wav')
GUN_SOUND.set_volume(0.3)
GUN_SOUND2 = pygame.mixer.Sound('2dassets/Sound Effects/gun_shot2.wav')
GUN_SOUND2.set_volume(0.15)
FOOTSTEPS = pygame.mixer.Sound('2dassets/Sound Effects/footstep.mp3')
FOOTSTEPS.set_volume(0.15)
ENEMY_DEATH_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/enemy_death_sound.wav')
ENEMY_DEATH_SOUND.set_volume(0.4)
GAME_OVER = pygame.mixer.Sound('2dassets/Sound Effects/game_over.wav')
HITMARKER = pygame.mixer.Sound('2dassets/Sound Effects/hitmarker.mp3')
HITMARKER.set_volume(0.3)
HURT = pygame.mixer.Sound('2dassets/Sound Effects/hurt.wav')
HURT.set_volume(0.2)
RELOAD_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/reload.mp3')
ENERGY_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/energy_coin.wav')
STRENGTH_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/whoosh.wav')
SPEED_BOOTS_SOUNDS = pygame.mixer.Sound('2dassets/Sound Effects/lightning.wav')
BUTTON_CLICK_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/button_click.wav')
GUN_SOUND3 = pygame.mixer.Sound('2dassets/Sound Effects/ENEMY3GUNSOUND.wav')
GUN_SOUND3.set_volume(0.15)
GUN_SOUND4 = pygame.mixer.Sound('2dassets/Sound Effects/mixkit-game-gun-shot-1662.mp3')
GUN_SOUND4.set_volume(0.15)
MAIN_MENU_MUSIC =  pygame.mixer.Sound('2dassets/Sound Effects/[ytmp3.ec]Jeremy_Blake_-_Powerup_NO_COPYRIGHT_8-bit_Music.mp3')
GAME_MUSIC_AUDIO = pygame.mixer.Sound('2dassets/Sound Effects/game_music.mp3')
GAME_MUSIC_AUDIO.set_volume(0.15)
ERROR_SOUND = pygame.mixer.Sound('2dassets/Sound Effects/mixkit-losing-bleeps-2026.wav')