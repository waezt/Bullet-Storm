import pygame
import  sys
from settings import *
from assets import *
import math
import random
from datetime import datetime
import time
import hashlib
import json
import os

pygame.init()
pygame.mixer.init()
pygame.font.init()

#Window

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Storm")
GameClock = pygame.time.Clock()
WHITE = (255, 255, 255)
paused = False
MAIN_MENU = "main_menu"
SIGN_IN = "sign_in"
GAME = "game"
SETTINGS = "settings"
STATS = "stats"
KEYBINDING = "keybinding"
current_state = SIGN_IN
color_blind_mode = False
high_score = 0
total_enemy_kills = 0
start_time = 0
difficulty_start_time = 0



keybinds = {
    "move_left": pygame.K_a,
    "move_right": pygame.K_d,
    "move_up": pygame.K_w,
    "move_down": pygame.K_s,
    "shoot": pygame.K_SPACE,
    "reload": pygame.K_r,
    "pause": pygame.K_p
}



#Map

MainMap = pygame.transform.rotozoom(BACKGROUND_1.convert(), 0, 1.5)
CharacterGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
EnemyGroup = pygame.sprite.Group()
PowerupsGroup = pygame.sprite.Group()




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(START_X, START_Y)
        self.idle_frames = [PLAYER_1_FRAME1.convert_alpha(),
                       PLAYER_1_FRAME2.convert_alpha(),
                       PLAYER_1_FRAME3.convert_alpha(),
                       PLAYER_1_FRAME4.convert_alpha()

        ]
        self.walk_frames = [PLAYER_1_MOVE_FRAME1.convert_alpha(),
                       PLAYER_1_MOVE_FRAME2.convert_alpha(),
                       PLAYER_1_MOVE_FRAME3.convert_alpha(),
                       PLAYER_1_MOVE_FRAME4.convert_alpha()
        ]
        self.current_frame = 0
        self.image = self.idle_frames[self.current_frame]
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.frame_count = 0
        self.frame_speed= FRAME_SPEED
        self.gun_pos = pygame.math.Vector2(25, 3)
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.font = pygame.font.Font(None, 30)
        self.footstep_timer = 0
        self.footstep_cooldown = 500
        self.ammo = MAX_AMMO
        self.max_ammo = MAX_AMMO
        self.reload_speed = RELOAD_SPEED
        self.last_reload_time = 0
        self.reloading = False
        self.is_boosted = False
        self.boost_end_time = 0
        self.speed_boosted = False
        self.speed_boost_end_time = 0
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.last_score_update = self.start_time
        self.angle = 0
        self.dead = False
        self.final_time = 0
        self.kills = 0





    def Aiming(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - WIDTH//2)
        self.y_change_mouse_player = (self.mouse_coords[1] - HEIGHT//2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle + 90)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)


    def Movement(self):
        self.speed_x = 0
        self.speed_y = 0

        keys_pressed = pygame.key.get_pressed()
        moved = False

        if keys_pressed[keybinds['move_left']]:  # LEFT
            self.speed_x -= self.speed
            moved = True
        if keys_pressed[keybinds['move_right']]:  # RIGHT
            self.speed_x += self.speed
            moved = True
        if keys_pressed[keybinds['move_up']]:  # UP
            self.speed_y -= self.speed
            moved = True
        if keys_pressed[keybinds['move_down']]:  # DOWN
            self.speed_y += self.speed
            moved = True

        current_time = pygame.time.get_ticks()

        if moved and current_time - self.footstep_timer > self.footstep_cooldown:
            FOOTSTEPS.play()
            self.footstep_timer = current_time

        if self.speed_x != 0 and self.speed_y != 0:
            self.speed_x /= math.sqrt(2)
            self.speed_y /= math.sqrt(2)


        if pygame.mouse.get_pressed() == (1, 0, 0) or keys_pressed[keybinds['shoot']]:
            self.shoot = True
            self.Shooting()
        else:
            self.shoot = False

    def Shooting(self):
        if self.shoot_cooldown == 0 and self.ammo > 0 and not self.reloading:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_pos.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            self.ammo -= 1
            CharacterGroup.add(self.bullet)
            GUN_SOUND.play()

    def Reload(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[keybinds['reload']] and self.ammo < self.max_ammo and not self.reloading:
            self.reloading = True
            self.last_reload_time = pygame.time.get_ticks()
            RELOAD_SOUND.play()

        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_reload_time >= self.reload_speed:
                self.ammo = self.max_ammo
                self.reloading = False

    def draw_ammo(self, surface):
        ammo_text = FONT.render(f'{self.ammo}/{self.max_ammo}', True, WHITE)
        surface.blit(ammo_text, (WIDTH -160, HEIGHT - 120))

    def increase_score(self, points):
        self.score += points

    def draw_score(self, surface):
        score_text = FONT.render(f'Score:{self.score}', True, WHITE)
        surface.blit(score_text, (WIDTH - 240 , 25))

    def draw_kill_count(self, surface):
        kill_text = FONT.render(f'Kills:{self.kills}', True, WHITE)
        surface.blit(kill_text, (WIDTH - 240 , 65))

    def time_survived_score(self):
        current_time = pygame.time.get_ticks()
        seconds_passed = (current_time - self.last_score_update) / 1000

        if seconds_passed >= 60:
            self.increase_score(100)
            self.last_score_update = current_time



    def Move(self):
        self.pos += pygame.math.Vector2(self.speed_x, self.speed_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def Animate(self):
        if self.speed_x == 0 and self.speed_y == 0:
            self.frame_count += self.frame_speed
            if self.frame_count >= len(self.idle_frames):
                self.frame_count = 0

            self.current_frame = int(self.frame_count)
            self.base_player_image = self.idle_frames[self.current_frame]

        elif self.speed_x != 0 or self.speed_y != 0:
            self.frame_count += self.frame_speed
            if self.frame_count >= len(self.walk_frames):
                self.frame_count = 0

            self.current_frame = int(self.frame_count)
            self.base_player_image = self.walk_frames[self.current_frame]

    def damage_taken(self, damage):
        self.health -= damage
        HURT.play()
        if self.health <= 0 and not self.dead:
            self.dead = True
            self.final_time = pygame.time.get_ticks()
            self.kill()
            GAME_OVER.play()

    def energy_power_up(self, health):
        if self. health <= 80:
            self.health += health
        else:
            self.health = self.max_health

    def strength_boosted(self, duration):
        self.is_boosted = True
        self.boost_end_time = pygame.time.get_ticks() + duration

    def speed_boots(self, duration):
        self.speed_boosted = True
        self.speed_boost_end_time = pygame.time.get_ticks() + duration
        self.speed = BOOSTED_SPEED

    def new_speed(self):
        if self.speed_boosted:
            if pygame.time.get_ticks() > self.speed_boost_end_time:
                self.speed_boosted = False
                self.speed = PLAYER_SPEED
        else:
            self.speed = self.speed

    def save_score(self):
        data = {
            "score": self.score,
            "player": self.name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        scores.append(data)
        with open("scores.json", "w") as file:
            json.dump(scores, file, indent=4)

    def load_scores(self):
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
            return sorted(scores, key=lambda x: x["score"], reverse=True)
        except FileNotFoundError:
            return []

    def display_leaderboard(self, surface):
        scores = self.load_scores()
        top_scores = scores[:5]
        font = pygame.font.Font(None, 36)

        y_offset = 400
        for rank, entry in enumerate(top_scores, start=1):
            score_text = FONT.render(f"{rank}. {entry['player']} - {entry['score']} ", True,
                                     (255, 255, 255))
            surface.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, y_offset))
            y_offset += 40

    def game_over_screen(self, surface):
        elapsed_time = (self.final_time - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer = f"{minutes:02}:{seconds:02}"
        score_message = FONT.render(f'Your Final Score Was: {self.score}', True, (255, 255, 255))
        time_message = FONT.render(f'You survived for: {timer}', True, (255, 255, 255))
        self.game_over_image = GAME_OVER_IMAGE

        if self.dead:
            self.save_score()
            window.fill((0, 0, 0))
            window.blit(self.game_over_image, (0, 0))
            surface.blit(score_message, (WIDTH / 2 - (score_message.get_width() / 2), HEIGHT / 2 + (score_message.get_height() / 2)-150))
            surface.blit(time_message, (WIDTH / 2 - (time_message.get_width() / 2), HEIGHT / 2 + (time_message.get_height() / 2)-85))
            self.display_leaderboard(surface)
            update_stats()
            save_stats(self.name)

            for enemy in EnemyGroup:
                enemy.kill()

            pygame.display.update()
            time.sleep(20)
            pygame.quit()
            sys.exit()








    def boundary_detection(self):
        for boundary in map_boundaries.boundaries:
            if self.hitbox_rect.colliderect(boundary):
                if self.hitbox_rect.bottom > boundary.top and self.hitbox_rect.top < boundary.top:
                    self.pos.y = boundary.top - 30

                elif self.hitbox_rect.top < boundary.bottom and self.hitbox_rect.bottom > boundary.bottom:
                    self.pos.y = boundary.bottom + 30

                elif self.hitbox_rect.right > boundary.left and self.hitbox_rect.left < boundary.left:
                    self.pos.x = boundary.left - 30

                elif self.hitbox_rect.left < boundary.right and self.hitbox_rect.right > boundary.right:
                    self.pos.x = boundary.right + 30



    def display_coordinates(self, surface):
        coordinates_text = self.font.render(f'X: {int(self.pos.x)}, Y: {int(self.pos.y)}', True, (255, 255, 255))
        surface.blit(coordinates_text, (10, 10))




    def update(self):
        self.Movement()
        self.boundary_detection()
        self.Move()
        self.Animate()
        self.Aiming()
        #self.display_coordinates(window)
        self.Reload()
        self.draw_ammo(window)
        self.new_speed()
        self.draw_score(window)
        self.time_survived_score()
        self.game_over_screen(window)
        self.draw_kill_count(window)


        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.is_boosted and pygame.time.get_ticks() > self.boost_end_time:
            self.is_boosted = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = BULLET_1.convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center =(x, y)
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_speed = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_speed = math.sin(self.angle * (2*math.pi/360)) * self.speed
        self.bullet_life = BULLET_LIFE
        self.spawn_time = pygame.time.get_ticks()
        self.strength_boost_time = STRENGTH_TIME
        self.last_time = 0
        if player.is_boosted:
            self.damage = STRENGTH_BOOST_VALUE * DIFFICULTY_MULTIPLIER
            self.image = BULLET_3
            self.image = pygame.transform.rotozoom(self.image, -player.angle , BULLET_SCALE)

        else:
            self.damage = BULLET_DAMAGE




    def bullet_movement(self):
        self.x += self.x_speed
        self.y += self.y_speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_life:
            self.kill()

    def collision_detect(self):
        for enemy in EnemyGroup:
            if self.rect.colliderect(enemy.rect):
                enemy.damage_taken(self.damage)
                self.kill()
        for boundary in map_boundaries.boundaries:
            if self.rect.colliderect(boundary):
                self.kill()




    def update(self):
        self.bullet_movement()
        self.collision_detect()





class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(EnemyGroup, CharacterGroup)
        self.frames = [ENEMY_1_FRAME_1.convert_alpha(),
                       ENEMY_1_FRAME_2.convert_alpha(),
                       ENEMY_1_FRAME_3.convert_alpha(),
                       ENEMY_1_FRAME_4.convert_alpha(),
                       ENEMY_1_FRAME_5.convert_alpha(),
                       ENEMY_1_FRAME_6.convert_alpha(),
                       ENEMY_1_FRAME_7.convert_alpha(),
                       ENEMY_1_FRAME_8.convert_alpha()]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.base_enemy_image = self.image
        self.frame_speed = ENEMY_FRAME_SPEED
        self.frame_count = 0
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = ENEMY_SPEED * DIFFICULTY_MULTIPLIER
        self.health = ENEMY_HEALTH * DIFFICULTY_MULTIPLIER
        self.shoot_cooldown = 1000
        self.last_shot_time = pygame.time.get_ticks()
        self.idle = True
        self.patrol_timer = 0
        self.patrol_cooldown = 3000
        self.patrol_direction = pygame.math.Vector2(1, 0)
        self.damage = ENEMY_DAMAGE
        self.gun_sound = GUN_SOUND2
        self.points = 20


    def rotate_towards_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))

        if not self.idle and self.line_of_sight(player):
            self.image = pygame.transform.rotate(self.base_enemy_image, -angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)

    def check_idle(self, player):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.enemy_distance(player_vector, enemy_vector)

        if distance < 550:
            self.idle = False
        else:
            self.idle = True

    def idle_behavior(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.patrol_timer > self.patrol_cooldown:
            self.patrol_timer = current_time
            random_angle = random.uniform(0, 2 * math.pi)
            self.patrol_direction = pygame.math.Vector2(math.cos(random_angle), math.sin(random_angle)).normalize()


        idle_speed = 1
        self.velocity = self.patrol_direction * idle_speed
        self.rect.center += self.velocity

        angle = math.degrees(math.atan2(self.patrol_direction.y, self.patrol_direction.x))
        self.image = pygame.transform.rotate(self.base_enemy_image, -angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def follow_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.enemy_distance(player_vector, enemy_vector)
        self.check_idle(player)

        if 100 < distance and not self.idle and self.line_of_sight(player):
            self.direction = (player_vector - enemy_vector).normalize()
            self.velocity = self.direction * self.speed
            self.rect.center += self.velocity
        elif self.idle:
            self.idle_behavior()



    def enemy_distance(self, player_vector_distance, enemy_vector_distance):
        return (player_vector_distance - enemy_vector_distance).magnitude()



    def Animate(self):
        self.frame_count += self.frame_speed
        if self.frame_count >= len(self.frames):
            self.frame_count = 0

        self.current_frame = int(self.frame_count)
        self.base_enemy_image = self.frames[self.current_frame]

    def damage_taken(self, damage):
        self.health -= damage
        HITMARKER.play()
        if self.health <= 0:
            self.kill()
            ENEMY_DEATH_SOUND.play()
            player.increase_score(self.points)
            player.kills += 1
            if player.health <= 90:
                player.health += 10

    def shoot_player(self, player):
        current_time = pygame.time.get_ticks()


        if not self.idle and self.line_of_sight(player):
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.last_shot_time = current_time

                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                angle = math.degrees(math.atan2(dy, dx))

                new_bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, self.damage)
                BulletGroup.add(new_bullet)
                self.gun_sound.play()

    def boundary_detection(self):
        for boundary in map_boundaries.boundaries:
            if self.rect.colliderect(boundary):
                if self.rect.bottom > boundary.top and self.rect.top < boundary.top:
                    self.rect.bottom = boundary.top
                elif self.rect.top < boundary.bottom and self.rect.bottom > boundary.bottom:
                    self.rect.top = boundary.bottom
                elif self.rect.right > boundary.left and self.rect.left < boundary.left:
                    self.rect.right = boundary.left
                elif self.rect.left < boundary.right and self.rect.right > boundary.right:
                    self.rect.left = boundary.right

    def line_of_sight(self, player):

        player_vector = pygame.math.Vector2(player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        step = 5

        direction = (player_vector - enemy_vector).normalize()
        distance = self.enemy_distance(player_vector, enemy_vector)

        for i in range(0, int(distance), step):
            point = enemy_vector + direction * i

            for boundary in map_boundaries.boundaries:
                if boundary.collidepoint(point):
                    return False

        return True



    def update(self):
        self.Animate()
        self.follow_player()
        self.idle_behavior()
        self.boundary_detection()
        self.rotate_towards_player(player)
        self.shoot_player(player)



class EnemySpawner:
    def __init__(self, spawn_time, enemy_group):
        self.spawn_time = spawn_time
        self.last_spawn_time = pygame.time.get_ticks()
        self.enemy_group = enemy_group


    def enemy_spawn(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_time:
            self.last_spawn_time = current_time

            spawn_point = random.choice(ENEMY_SPAWN_LOCATIONS)
            enemy_type = random.choice(["Enemy", "Enemy2", "Enemy3"])

            if enemy_type == "Enemy":
                new_enemy = Enemy(spawn_point)
            elif enemy_type == "Enemy2":
                new_enemy = Enemy2(spawn_point)
            elif enemy_type == "Enemy3":
                new_enemy = Enemy3(spawn_point)

            EnemyGroup.add(new_enemy)





class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage):
        super().__init__()
        self.image = BULLET_2.convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED / 2
        self.angle = angle
        self.bullet_life = BULLET_LIFE
        self.spawn_time = pygame.time.get_ticks()
        self.x_speed = math.cos(math.radians(self.angle)) * self.speed
        self.y_speed = math.sin(math.radians(self.angle)) * self.speed
        self.damage = damage

    def collision_detect(self):
        if self.rect.colliderect(player.rect):
            player.damage_taken(self.damage)
            self.kill()
        for boundary in map_boundaries.boundaries:
            if self.rect.colliderect(boundary):
                self.kill()


    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.collision_detect()

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_life:
            self.kill()



class Camera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = MainMap.get_rect(topleft=(0, 0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        floor_offset_pos = self.floor_rect.topleft - self.offset
        window.blit(MainMap, floor_offset_pos)

        for powerup in PowerupsGroup:
            offset_powerup_pos = powerup.rect.topleft - self.offset
            window.blit(powerup.image, offset_powerup_pos)

        for sprite in CharacterGroup:
            offset_pos = sprite.rect.topleft - self.offset
            window.blit(sprite.image, offset_pos)

        for bullet in BulletGroup:
            offset_bullet_pos = bullet.rect.topleft - self.offset
            window.blit(bullet.image, offset_bullet_pos)




class HealthBar():
    def __init__(self, player, x, y, w, h):
        self.player = player
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.background_image = pygame.transform.scale(HEALTH_BAR_1, (self.w, self.h))  # Empty health bar
        self.foreground_image = pygame.transform.scale(HEALTH_BAR_2, (self.w, self.h))  # Filled health bar

    def draw(self, surface):
        ratio = self.player.health / PLAYER_HEALTH

        surface.blit(self.background_image, (self.x, self.y))
        filled_width = int(self.w * ratio)

        if filled_width > 0:
            filled_bar = self.foreground_image.subsurface((0, 0, filled_width, self.h))
            surface.blit(filled_bar, (self.x, self.y + 31))


class MapBoundaries:
    def __init__(self):
        self.boundaries = [
            pygame.Rect(380, 650, 308, 20),
            pygame.Rect(365, 660, 20, 500),
            pygame.Rect(355, 1154, 325, 20),
            pygame.Rect(680, 970, 20, 250),
            pygame.Rect(680, 970, 260, 20),
            pygame.Rect(937, 977, 20, 380),
            pygame.Rect(945, 1345, 260, 20),
            pygame.Rect(1161, 1065, 20, 380),
            pygame.Rect(1161, 1055, 180, 20),
            pygame.Rect(1323, 1070, 20, 380),
            pygame.Rect(1330, 1440, 540, 20),
            pygame.Rect(1454, 1054, 470, 20),
            pygame.Rect(1441, 1062, 20, 180),
            pygame.Rect(1439, 1231, 470, 20),
            pygame.Rect(669, 664, 20, 100),
            pygame.Rect(942, 664, 20, 100),
            pygame.Rect(683, 743, 268, 20),
            pygame.Rect(940, 363, 20, 380),
            pygame.Rect(940, 363, 220, 20),
            pygame.Rect(1152, 361, 20, 310),
            pygame.Rect(1823, 1243, 20, 200),
            pygame.Rect(1153, 660, 140, 20),
            pygame.Rect(1248, 678, 20, 186),
            pygame.Rect(1256, 847, 760, 20),
            pygame.Rect(1901, 1155, 760, 20),
            pygame.Rect(1901, 1052, 20, 120),
            pygame.Rect(2000, 678, 20, 186),
            pygame.Rect(1256, 671, 760, 20),
            pygame.Rect(1327, 272, 500, 20),
            pygame.Rect(1327, 272, 20, 420),
            pygame.Rect(1829, 272, 20, 200),
            pygame.Rect(1441, 550, 1080, 20),
            pygame.Rect(1441, 387, 20, 180),
            pygame.Rect(1441, 387, 400, 20),
            pygame.Rect(2500, 550, 20, 200),
            pygame.Rect(2500, 1061, 20, 200),
            pygame.Rect(2509, 749, 120, 20),
            pygame.Rect(2689, 767, 120, 20),
            pygame.Rect(2601, 965, 120, 20),
            pygame.Rect(2595, 845, 220, 20),
            pygame.Rect(2596, 760, 20, 100),
            pygame.Rect(2595, 961, 20, 100),
            pygame.Rect(2690, 854, 20, 120),
            pygame.Rect(2500, 1055, 120, 20),
            pygame.Rect(2109, 940, 100, 20),
            pygame.Rect(2109, 865, 100, 20),
            pygame.Rect(2109, 865, 20, 100),
            pygame.Rect(2192, 865, 20, 100),
        ]

    def draw(self, surface):
        for boundary in self.boundaries:
            pygame.draw.rect(surface, (255, 0, 0), boundary)

class Energy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = [ENERGY_FRAME_1.convert_alpha(),
                       ENERGY_FRAME_2.convert_alpha(),
                       ENERGY_FRAME_3.convert_alpha(),
                       ENERGY_FRAME_4.convert_alpha(),
                       ENERGY_FRAME_5.convert_alpha(),
                       ENERGY_FRAME_6.convert_alpha(),
                       ENERGY_FRAME_7.convert_alpha(),]

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.frame_speed = ENERGY_FRAME_SPEED

        self.frame_count = 0
        self.rect.center = pos
        self.health = ENERGY_HEALTH

    def Animate(self):
        self.frame_count += self.frame_speed
        if self.frame_count >= len(self.frames):
            self.frame_count = 0

        self.current_frame = int(self.frame_count)
        self.image = self.frames[self.current_frame]

    def collision_detect(self):
        if self.rect.colliderect(player.rect):
            player.energy_power_up(self.health)
            self.kill()
            ENERGY_SOUND.play()
            player.increase_score(5)


    def update(self):
        self.Animate()
        self.collision_detect()

map_boundaries = MapBoundaries()


class StrengthBoost(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = STRENGTH_BOOST.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = STRENGTH_TIME

    def collision_detect(self):
        if self.rect.colliderect(player.rect):
            player.strength_boosted(self.duration)
            self.kill()
            STRENGTH_SOUND.play()
            player.increase_score(5)

    def update(self):
        self.collision_detect()

class SpeedBoots(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = SPEED_BOOTS.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.duration = SPEED_BOOTS_TIME


    def collision_detect(self):
        if self.rect.colliderect(player.rect):
            player.speed_boots(self.duration)
            self.kill()
            SPEED_BOOTS_SOUNDS.play()
            player.increase_score(5)

    def update(self):
        self.collision_detect()



class PowerupSpawner:
    def __init__(self, spawn_time, powerups_group, spawn_locations):
        self.spawn_time = spawn_time
        self.last_spawn_time = pygame.time.get_ticks()
        self.powerups_group = powerups_group
        self.spawn_locations = spawn_locations

    def spawn_powerup(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_time:
            self.last_spawn_time = current_time
            spawn_point = random.choice(self.spawn_locations)
            new_powerup = self.create_powerup(spawn_point)
            self.powerups_group.add(new_powerup)

    def update(self):
        self.spawn_powerup()

class EnergySpawner(PowerupSpawner):
    def create_powerup(self, position):
        return Energy(position)

class StrengthBoostSpawner(PowerupSpawner):
    def create_powerup(self, position):
        return StrengthBoost(position)

class SpeedBootsSpawner(PowerupSpawner):
    def create_powerup(self, position):
        return SpeedBoots(position)

mute_button_pressed = False
mute_text_message = 'MUTE'
mute_audio = False
quit_button_pressed = False
restart_button_pressed =False

def pause_screen(surface):
    global mute_button_pressed, mute_text_message, mute_audio, quit_button_pressed, restart_button_pressed
    pause_text = LARGE_FONT.render('PAUSED', True, WHITE)
    mute_text = FONT.render(mute_text_message, True, WHITE)
    mute_button = pygame.Rect(300, 230, 420, 100)
    mouse_pos = pygame.mouse.get_pos()
    if mute_button_pressed:
        mute_button_image = BUTTON_PRESSED
    else:
        mute_button_image = BUTTON_IDLE
    surface.blit(pause_text, (WIDTH / 2 - (pause_text.get_width() / 2), HEIGHT / 2 + (pause_text.get_height() / 2) - 300))
    surface.blit(mute_button_image, (mute_button.x, mute_button.y))
    surface.blit(mute_text, (WIDTH / 2 - (50), 250))

    if mute_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            BUTTON_CLICK_SOUND.play()
            if not mute_button_pressed:
                    mute_button_pressed = True
                    mute_audio = not mute_audio
                    mute_text_message = 'UNMUTE' if mute_text_message == 'MUTE' else 'MUTE'
                    mute_sounds()
        elif pygame.mouse.get_pressed() == (0, 0, 0):
            mute_button_pressed = False

    quit_button = pygame.Rect(300, 530, 420, 100)
    quit_text = FONT.render('QUIT', True, WHITE)
    if quit_button_pressed:
        quit_button_image = BUTTON_PRESSED
    else:
        quit_button_image = BUTTON_IDLE
    surface.blit(quit_button_image, (quit_button.x, quit_button.y))
    surface.blit(quit_text, (WIDTH / 2 - (50), 550))

    if quit_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            BUTTON_CLICK_SOUND.play()
            if not quit_button_pressed:
                quit_button_pressed = True
                pygame.quit()
                sys.exit()

    restart_button = pygame.Rect(300, 380, 420, 100)
    restart_text = FONT.render('RESTART', True, WHITE)
    if restart_button_pressed:
        restart_button_image = BUTTON_PRESSED
    else:
        restart_button_image = BUTTON_IDLE
    surface.blit(restart_button_image, (restart_button.x, restart_button.y))
    surface.blit(restart_text, (WIDTH / 2 - (75), 400))

    if restart_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            BUTTON_CLICK_SOUND.play()
            if not restart_button_pressed:
                restart_button_pressed = True
                time.sleep(0.5)
                restart_game()
        elif pygame.mouse.get_pressed() == (0, 0, 0):
            restart_button_pressed = False



def restart_game():
    global player, enemies, score, start_time, paused, difficulty_start_time, DIFFICULTY_MULTIPLIER

    for enemy in EnemyGroup:
        enemy.kill()
    for powerup in PowerupsGroup:
        powerup.kill()

    player.score = 0
    player.ammo = MAX_AMMO
    player.pos = pygame.math.Vector2(START_X, START_Y)
    player.kills = 0
    DIFFICULTY_MULTIPLIER = 1.0
    paused = not paused
    start_time = pygame.time.get_ticks()
    difficulty_start_time = pygame.time.get_ticks()









sound_group = [GUN_SOUND, GUN_SOUND2, FOOTSTEPS, ENEMY_DEATH_SOUND, GAME_OVER, HITMARKER, HURT, RELOAD_SOUND,
               ENERGY_SOUND, STRENGTH_SOUND, SPEED_BOOTS_SOUNDS, BUTTON_CLICK_SOUND, GUN_SOUND3, GUN_SOUND4, ERROR_SOUND]

def mute_sounds():
    if mute_audio:
        for sound in sound_group:
            sound.set_volume(0)
    elif not mute_audio:
        GUN_SOUND.set_volume(0.3)
        GUN_SOUND2.set_volume(0.15)
        FOOTSTEPS.set_volume(0.15)
        ENEMY_DEATH_SOUND.set_volume(0.4)
        HITMARKER.set_volume(0.3)
        HURT.set_volume(0.2)
        GAME_OVER.set_volume(1)
        RELOAD_SOUND.set_volume(1)
        ENERGY_SOUND.set_volume(1)
        STRENGTH_SOUND.set_volume(1)
        SPEED_BOOTS_SOUNDS.set_volume(1)
        BUTTON_CLICK_SOUND.set_volume(0.5)
        GUN_SOUND3.set_volume(0.15)
        GUN_SOUND4.set_volume(0.15)
        ERROR_SOUND.set_volume(1)





class Enemy2(Enemy):
    def __init__(self, position):
        super().__init__(position)

        self.frames = [ENEMY_2_FRAME_1.convert_alpha(),
                       ENEMY_2_FRAME_2.convert_alpha(),
                       ENEMY_2_FRAME_3.convert_alpha(),
                       ENEMY_2_FRAME_4.convert_alpha(),]
        self.damage = 3.0 * DIFFICULTY_MULTIPLIER
        self.speed = 2.5 * DIFFICULTY_MULTIPLIER
        self.shoot_cooldown = 300
        self.health = 75.0
        self.gun_sound = GUN_SOUND4

class Enemy3(Enemy):
    def __init__(self, position):
        super().__init__(position)

        self.frames = [ENEMY_3_FRAME_1.convert_alpha(),
                       ENEMY_3_FRAME_2.convert_alpha(),
                       ENEMY_3_FRAME_3.convert_alpha(),
                       ENEMY_3_FRAME_4.convert_alpha(),
                       ENEMY_3_FRAME_5.convert_alpha(),
                       ENEMY_3_FRAME_6.convert_alpha(),
                       ENEMY_3_FRAME_7.convert_alpha(),
                       ENEMY_3_FRAME_8.convert_alpha()]
        self.damage = 25.0 * DIFFICULTY_MULTIPLIER
        self.health = 150.0 * DIFFICULTY_MULTIPLIER
        self.shoot_cooldown = 3000
        self.gun_sound = GUN_SOUND3
        self.points = 30












def increase_difficulty():
    global DIFFICULTY_MULTIPLIER, difficulty_start_time
    current_time = pygame.time.get_ticks()

    if current_time - difficulty_start_time >= 60000:
        DIFFICULTY_MULTIPLIER += 0.25
        difficulty_start_time += 60000



color_blind_list = ['None','Deuteranopia','Protanopia','Tritanopia' ]
pointer = 0

def apply_deuteranopia_filter(screen):
    pixels = pygame.surfarray.pixels3d(screen)
    pixels[:, :, 1] = 0


def apply_protanopia_filter(surface):
    pixels = pygame.surfarray.pixels3d(surface)
    pixels[:, :, 0] = 0


def apply_tritanopia_filter(surface):
    pixels = pygame.surfarray.pixels3d(surface)
    pixels[:, :, 2] = 0


music_muted = False

def mute_music():
    global  music_muted
    if music_muted:
        MAIN_MENU_MUSIC.set_volume(0)
        GAME_MUSIC_AUDIO.set_volume(0)
    elif not music_muted:
        MAIN_MENU_MUSIC.set_volume(1)
        GAME_MUSIC_AUDIO.set_volume(0.1)


game_music_playing = True

def play_game_music():
    global current_state, game_music_playing, music_time
    if current_state == GAME and game_music_playing:
        GAME_MUSIC_AUDIO.play(100)
        game_music_playing = False


pressed = False

def KeybindsMenu(window):
    global keybinds, current_state, pressed, mouse_pos, current_state
    window.fill((0, 0, 0))
    window.blit(MENU_3, (0, 0))

    actions = ["move_left", "move_right", "move_up", "move_down", "shoot", "reload", "pause"]
    labels = ["Move Left", "Move Right", "Move Up", "Move Down", "Shoot", "Reload", "Pause"]

    key_rects = []

    for i, action in enumerate(actions):
        if pressed:
            button_image = SMALL_BUTTON_PRESSED
        else:
            button_image = SMALL_BUTTON_IDLE
        label_message = f"{labels[i]}: {pygame.key.name(keybinds[action])}"
        label_text = FONT.render(label_message, True, (255, 255, 255))
        rect = pygame.Rect(300, 135 + i * 70, 300, 40)
        key_rects.append((rect, action))
        window.blit(button_image, (rect.x + 10, rect.y + 5))
        window.blit(label_text, (rect.x + 45, rect.y + 12))

    EXIT_BUTTON = pygame.Rect(900, 55, 100, 100)
    window.blit(CROSS_IMAGE.convert_alpha(), (EXIT_BUTTON.x, EXIT_BUTTON.y))

    error_text1 = FONT.render('INCORRECT DETAILS', True, 'red')



    pygame.display.update()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if EXIT_BUTTON.collidepoint(mouse_pos):
                    BUTTON_CLICK_SOUND.play()
                    current_state = SETTINGS

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in key_rects:
                    if rect.collidepoint(mouse_pos):
                        BUTTON_CLICK_SOUND.play()
                        new_key = get_new_key()
                        if new_key:
                            if new_key in keybinds.values():
                                ERROR_SOUND.play()
                                display_message(window, "Key already in use")
                            else:
                                keybinds[action] = new_key



def display_message(window, message):
    text_surface = FONT.render(message, True, WHITE)
    window.blit(text_surface, (300, 650))
    pygame.display.update()
    pygame.time.delay(2000)



def get_new_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                return event.key


def update_stats():
    global high_score, total_enemy_kills

    if player.score > high_score:
        high_score = player.score

    total_enemy_kills += player.kills
    player.kills = 0

def save_stats(player_username):
    global high_score, total_enemy_kills

    try:
        with open("stats.json", "r") as file:
            stats = json.load(file)
    except FileNotFoundError:
        stats = {}

    stats[player_username] = {
        "high_score": high_score,
        "total_enemy_kills": total_enemy_kills
    }

    with open("stats.json", "w") as file:
        json.dump(stats, file, indent=4)

def load_stats(player_username):
    global high_score, total_enemy_kills

    try:
        with open("stats.json", "r") as file:
            stats = json.load(file)

        if player_username in stats:
            high_score = stats[player_username]["high_score"]
            total_enemy_kills = stats[player_username]["total_enemy_kills"]
    except FileNotFoundError:
        pass







camera = Camera()
player = Player()
enemy3 = Enemy3(random.choice(ENEMY_SPAWN_LOCATIONS))
enemy2 = Enemy2(random.choice(ENEMY_SPAWN_LOCATIONS))
enemy = Enemy(random.choice(ENEMY_SPAWN_LOCATIONS))
enemy_spawner = EnemySpawner(spawn_time= ENEMY_SPAWN_TIME, enemy_group= EnemyGroup)
health_bar = HealthBar(player, 2, -50, 300, 300)
map_boundaries = MapBoundaries()
energy_spawner = EnergySpawner(spawn_time=ENERGY_SPAWN_TIME, powerups_group= PowerupsGroup, spawn_locations=POWERUPS_SPAWN_LOCATIONS)
strength_boost_spawner = StrengthBoostSpawner(spawn_time=STRENGTH_SPAWN_TIME, powerups_group= PowerupsGroup, spawn_locations=POWERUPS_SPAWN_LOCATIONS)
speed_boots_spawner = SpeedBootsSpawner(spawn_time=SPEED_BOOTS_SPAWN_TIME, powerups_group= PowerupsGroup, spawn_locations=POWERUPS_SPAWN_LOCATIONS)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def username_exists(username):
    return os.path.exists(f"{username.lower()}.json")



def create_user(username, password):
    user_data = {
        "username": username,
        "password": hash_password(password)
    }
    with open(f"{username.lower()}.json", "w") as file:
        json.dump(user_data, file)



def validate_login(username, password):
    if not username_exists(username):
        return False
    with open(f"{username.lower()}.json", "r") as file:
        user_data = json.load(file)
    return user_data["password"] == hash_password(password)


def get_text_input(prompt, x, y):
    text = ''
    input_box = pygame.Rect(x, y, 200, 50)
    color_inactive = pygame.Color(WHITE)
    color_active = pygame.Color(255, 0, 255)
    color = color_inactive
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        window.fill((0, 0, 0))
        window.blit(BLANK_MENU, (0, 0))
        text_surface = FONT.render(prompt + ": " + text, True, WHITE)
        width = max(600, text_surface.get_width() + 10)
        input_box.w = width
        window.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(window, color, input_box, 2)

        pygame.display.update()



def sign_in_page(window):
    global current_state
    while True:
        window.fill((0, 0, 0))
        window.blit(BLANK_MENU, (0, 0))

        login_text = MEDIUM_FONT.render("Log In", True, WHITE)
        signup_text = MEDIUM_FONT.render("Sign Up", True, WHITE)
        error_text1 = FONT.render('INCORRECT DETAILS', True, 'red')
        error_text2 = FONT.render('USERNAME ALREADY EXISTS', True, 'red')
        success_text = FONT.render('ACCOUNT CREATED', True, 'green')

        log_in_button = pygame.Rect(300, 275, 420, 100)
        sign_up_button = pygame.Rect(300, 425, 420, 100)

        window.blit(BUTTON_IDLE, (log_in_button.x, log_in_button.y))
        window.blit(BUTTON_IDLE, (sign_up_button.x, sign_up_button.y))

        window.blit(login_text, (WIDTH / 2 - login_text.get_width() / 2, HEIGHT / 2 - 100))
        window.blit(signup_text, (WIDTH / 2 - signup_text.get_width() / 2, HEIGHT / 2 + 50))

        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if log_in_button.collidepoint(mouse_pos):
                    BUTTON_CLICK_SOUND.play()
                    username = get_text_input("Enter username", 200, 275)
                    player.name = username
                    password = get_text_input("Enter password", 200, 275)
                    if validate_login(username, password):
                        current_state = MAIN_MENU
                        return username
                    else:
                        window.blit(error_text1, (200, 345))
                        pygame.display.update()
                        time.sleep(3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sign_up_button.collidepoint(mouse_pos):
                    BUTTON_CLICK_SOUND.play()
                    username = get_text_input("Enter username", 200, 275)
                    password = get_text_input("Enter password", 200, 275)
                    if username_exists(username):
                        window.blit(error_text2, (200, 345))
                        pygame.display.update()
                        time.sleep(3)
                    else:
                        create_user(username, password)
                        player.name = username
                        window.blit(success_text, (200, 345))
                        pygame.display.update()
                        time.sleep(3)
                        current_state = MAIN_MENU
                        return username



def MainMenu(window):
    global current_state, start_time, difficulty_start_time
    window.fill((0, 0, 0))
    window.blit(MENU_1, (0, 0))

    START_BUTTON = pygame.Rect(380, 460, 260, 90)
    SETTINGS_BUTTON = pygame.Rect(75, 470, 210, 78)
    STATS_BUTTON = pygame.Rect(735, 470, 210, 78)

    pygame.display.update()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                time.sleep(0.3)
                start_time = pygame.time.get_ticks()
                difficulty_start_time = pygame.time.get_ticks()
                current_state = GAME
        if event.type == pygame.MOUSEBUTTONDOWN:
            if SETTINGS_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                current_state = SETTINGS
        if event.type == pygame.MOUSEBUTTONDOWN:
            if STATS_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                current_state = STATS


def StatsMenu(window):
    global current_state
    window.fill((0, 0, 0))
    window.blit(MENU_2, (0, 0))
    EXIT_BUTTON = pygame.Rect(780, 55, 100, 100)
    window.blit(CROSS_IMAGE.convert_alpha(), (EXIT_BUTTON.x, EXIT_BUTTON.y))

    leaderboard_text = FONT.render('LEADERBOARD', True, WHITE)
    window.blit(leaderboard_text, (370, 350))
    player.display_leaderboard(window)

    highscore_text = FONT.render('HIGHSCORE: ', True, WHITE)
    totalkills_text = FONT.render('ALL TIME KILLS: ', True, WHITE)

    highscore_value = FONT.render(str(high_score), True, WHITE)
    totalkills_value = FONT.render(str(total_enemy_kills), True, WHITE)

    window.blit(highscore_text, (300, 200))
    window.blit(totalkills_text, (185, 250))

    window.blit(highscore_value, (550, 200))
    window.blit(totalkills_value, (550, 250))


    pygame.display.update()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if EXIT_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                current_state = MAIN_MENU


COLOUR_BLIND_BUTTON_PRESSED = False
mute_sfx_message = 'MUTE SFX'
mute_music_message = 'MUTE MUSIC'
MUTE_MUSIC_BUTTON_PRESSED = False

def SettingsMenu(window):
    global current_state, color_blind_mode, COLOUR_BLIND_BUTTON_PRESSED, color_blind_list, pointer, mute_audio,\
        mute_button_pressed, mute_sfx_message, mute_music_message, MUTE_MUSIC_BUTTON_PRESSED, music_muted
    window.fill((0, 0, 0))
    window.blit(MENU_3, (0, 0))
    EXIT_BUTTON = pygame.Rect(900, 55, 100, 100)
    window.blit(CROSS_IMAGE.convert_alpha(), (EXIT_BUTTON.x, EXIT_BUTTON.y))
    COLOUR_BLIND_BUTTON = pygame.Rect(300, 170, 420, 100)
    COLOUR_BLIND_BUTTON_TEXT = FONT.render(color_blind_list[pointer], True, WHITE)

    if COLOUR_BLIND_BUTTON_PRESSED:
        COLOUR_BLIND_BUTTON_IMAGE = BUTTON_PRESSED
    else:
        COLOUR_BLIND_BUTTON_IMAGE = BUTTON_IDLE
    window.blit(COLOUR_BLIND_BUTTON_IMAGE, (COLOUR_BLIND_BUTTON.x, COLOUR_BLIND_BUTTON.y))
    window.blit(COLOUR_BLIND_BUTTON_IMAGE, (COLOUR_BLIND_BUTTON.x, COLOUR_BLIND_BUTTON.y))
    window.blit(COLOUR_BLIND_BUTTON_TEXT, (WIDTH/2 - 120, 190))

    MUTE_SFX_BUTTON = pygame.Rect(300, 290, 420, 100)
    mute_sfx_text = FONT.render(mute_sfx_message, True, WHITE)
    if mute_button_pressed:
        mute_button_image = BUTTON_PRESSED
    else:
        mute_button_image = BUTTON_IDLE
    window.blit(mute_button_image, (MUTE_SFX_BUTTON.x, MUTE_SFX_BUTTON.y))
    window.blit(mute_sfx_text, (WIDTH / 2 - 120, MUTE_SFX_BUTTON.y + 20))

    MUTE_MUSIC_BUTTON = pygame.Rect(300, 410, 420, 100)
    mute_music_text = FONT.render(mute_music_message, True, WHITE)
    if MUTE_MUSIC_BUTTON_PRESSED:
        mute_music_button_image = BUTTON_PRESSED
    else:
        mute_music_button_image = BUTTON_IDLE
    window.blit(mute_music_button_image, (MUTE_MUSIC_BUTTON.x, MUTE_MUSIC_BUTTON.y))
    window.blit(mute_music_text, (WIDTH / 2 - 120, MUTE_MUSIC_BUTTON.y + 20))

    KEYBIND_BUTTON = pygame.Rect(300, 530, 420, 100)
    keybind_button_text = FONT.render('KEYBINDINGS', True, WHITE)
    window.blit(BUTTON_IDLE, (KEYBIND_BUTTON.x, KEYBIND_BUTTON.y))
    window.blit(keybind_button_text, (WIDTH / 2 - 120, KEYBIND_BUTTON.y + 20))


    pygame.display.update()
    mouse_pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if EXIT_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                current_state = MAIN_MENU
            if COLOUR_BLIND_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                COLOUR_BLIND_BUTTON_PRESSED = not COLOUR_BLIND_BUTTON_PRESSED

        if event.type == pygame.MOUSEBUTTONUP:
            if COLOUR_BLIND_BUTTON.collidepoint(mouse_pos):
                COLOUR_BLIND_BUTTON_PRESSED = False
                if pointer < len(color_blind_list)- 1:
                    pointer += 1
                else:
                    pointer = 0

        if MUTE_SFX_BUTTON.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed() == (1, 0, 0):
                BUTTON_CLICK_SOUND.play()
                if not mute_button_pressed:
                    mute_button_pressed = True
                    mute_audio = not mute_audio
                    mute_sfx_message = 'UNMUTE SFX' if mute_sfx_message == 'MUTE SFX' else 'MUTE SFX'
                    mute_sounds()
            elif pygame.mouse.get_pressed() == (0, 0, 0):
                mute_button_pressed = False

        if MUTE_MUSIC_BUTTON.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed() == (1, 0, 0):
                BUTTON_CLICK_SOUND.play()
                if not MUTE_MUSIC_BUTTON_PRESSED:
                    MUTE_MUSIC_BUTTON_PRESSED = True
                    music_muted = not music_muted
                    mute_music_message = 'UNMUTE MUSIC' if mute_music_message == 'MUTE MUSIC' else 'MUTE MUSIC'
                    mute_music()
            elif pygame.mouse.get_pressed() == (0, 0, 0):
                MUTE_MUSIC_BUTTON_PRESSED = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if KEYBIND_BUTTON.collidepoint(mouse_pos):
                BUTTON_CLICK_SOUND.play()
                current_state = KEYBINDING







#Sprite Groups

CharacterGroup.add(player)
EnemyGroup.add(enemy2)





def game_loop():
    global paused, current_state, start_time, difficulty_start_time

    if current_state != GAME:
        MAIN_MENU_MUSIC.play()


    while True:
        if current_state == SIGN_IN:
            username = sign_in_page(window)
        elif current_state == MAIN_MENU:
            MainMenu(window)
            load_stats(username)
        elif current_state == STATS:
            StatsMenu(window)
        elif current_state == SETTINGS:
            SettingsMenu(window)
        elif current_state == KEYBINDING:
            KeybindsMenu(window)
        elif current_state == GAME:
            MAIN_MENU_MUSIC.stop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if not paused:
                        paused = True
                        paused_time = pygame.time.get_ticks()
                    else:
                        paused = False
                        start_time += pygame.time.get_ticks() - paused_time
                        difficulty_start_time += pygame.time.get_ticks() - paused_time

            if not paused:

                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - start_time) // 1000
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                timer = f"{minutes:02}:{seconds:02}"
                timer_surface = FONT.render(timer, True, WHITE)

                window.fill((0, 0, 0))
                camera.custom_draw()
                # map_boundaries.draw(MainMap)
                window.blit(timer_surface, (window.get_width() - timer_surface.get_width() - 100, 110))
                health_bar.draw(window)
                enemy_spawner.enemy_spawn()
                CharacterGroup.update()
                EnemyGroup.update()
                BulletGroup.update()
                PowerupsGroup.update()
                energy_spawner.update()
                strength_boost_spawner.update()
                speed_boots_spawner.update()
                increase_difficulty()
                play_game_music()
                if pointer == 1:
                    apply_deuteranopia_filter(window)
                elif pointer == 2:
                    apply_protanopia_filter(window)
                elif pointer == 3:
                    apply_tritanopia_filter(window)
                else:
                    pass

                if player.dead:
                    player.game_over_screen(window)

                pygame.display.update()
                GameClock.tick(FPS)

            else:
                pause_screen(window)
                pygame.display.update()


game_loop()