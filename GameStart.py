import math
import GameArt
import pygame
import SegmentClass
import sys
import random
import psutil
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
pygame.init()
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()

player_x, player_y = w / 2, h - 60
player_w, player_h = 0, 0
ast_list = []
ast_event, ast_time = pygame.USEREVENT+1, 400
ast_add = True
ast_w, ast_h = 70, 80
sprite_no = 0
right, left, shift = False, False, False
mv_speed = 12
mouse_pressed = False
game_start = False
angle, slope, dx = 0, 0, 0
bullets = np.array([-1, -1, -1, -1, -1])
can_fire = True
bullet_event, bullet_event_time = pygame.USEREVENT+2, 100
end_sound, end_sound_time = pygame.USEREVENT + 2, 100
bullet_speed = 30
ast_speed = 30
player_lives = 4
destroy_meter = 100
score = 0
time_played = 0
paused = False
music_playing = False
song_no = 0
can_play_sound = True
bgr_y, bgr_y2 = 0, -h
sound_play = [True, True, True, True]
expl_no = 0
dead = False
counter = 0
expl_x = 0
explosions = []
fuel_event, fuel_event_time = pygame.USEREVENT+3, 20000
fuel_send = True
one_up_counter = 0


def generate_random_x():
    global ast_add, fuel_send
    if ast_add and cpu_limit():
        x = random.randrange(0, w-100)
        sp = random.randrange(0, 4)
        mv = random.randrange(-5, 5)
        ast_list.append([x, -400, sp, mv, 0, 0])
        ast_add = False
        pygame.time.set_timer(ast_event, ast_time)
        if fuel_send:
            x = random.randrange(0, w-100)
            ast_list.append([x, -400, 4, mv, 0, 1])
            fuel_send = False
            pygame.time.set_timer(fuel_event, fuel_event_time)


def load_bullets():
    global can_fire, bullets, can_play_sound
    if can_fire and mouse_pressed:
        arr2 = np.array([player_x, player_y, slope, angle, dx])
        bullets = np.vstack((bullets, arr2))
        pygame.time.set_timer(bullet_event, bullet_event_time)
        can_fire = False
        if can_play_sound:
            play_sound(GameArt.bullet_sound)
            can_play_sound = False


def event_handling():
    global ast_add, mouse_pressed, can_fire, paused, can_play_sound, fuel_send
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
                sys.exit()
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == ast_event:
            ast_add = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

        if event.type == end_sound:
            can_play_sound = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

        if event.type == bullet_event:
            can_fire = True
        if event.type == fuel_event:
            fuel_send = True


def draw_background():
    global bgr_y, bgr_y2
    backgr = SegmentClass.PlayerSegment(0, bgr_y, GameArt.background, wid=w, hie=h, tl=True)
    backgr2 = SegmentClass.PlayerSegment(0, bgr_y2, GameArt.background, wid=w, hie=h, tl=True)
    display_surface.blit(backgr.image, backgr.rect)
    display_surface.blit(backgr2.image, backgr2.rect)

    bgr_y += 25
    bgr_y2 += 25
    if bgr_y >= h:
        bgr_y = -h
    if bgr_y2 > h:
        bgr_y2 = -h


def draw_player():
    global sprite_no, player_w, player_h
    if dead:
        return
    plyr = SegmentClass.PlayerSegment(player_x, player_y, GameArt.spaceship[sprite_no], tl=False,
                                      angle1=angle, rotate=True, wid=70, hie=70)
    display_surface.blit(plyr.image, plyr.rect)
    player_w, player_h = plyr.rect[2], plyr.rect[3]
    if sprite_no < len(GameArt.spaceship)-1:
        sprite_no += 1
    else:
        sprite_no = 0


def draw_bullets():
    global bullets
    rem = []
    dim = bullets.shape
    if len(dim) == 1:
        return
    x_speed = bullet_speed
    for x in range(bullets.shape[0]):
        if x == 0:
            continue
        bull = SegmentClass.PlayerSegment(bullets[x][0], bullets[x][1], GameArt.bullet, angle1=bullets[x][3]
                                          , rotate=True, wid=30, hie=40)
        display_surface.blit(bull.image, bull.rect)
        collision_detection_bullet(bull.rect , x)
        y_speed = bullets[x][2] * x_speed
        if bullets[x][2] > 1:
            y_speed = bullet_speed
            x_speed = y_speed / bullets[x][2]
        elif bullets[x][2] < -1:
            y_speed = -bullet_speed
            x_speed = y_speed / bullets[x][2]
        if bullets[x][4] > 0:
            bullets[x][0] += x_speed
            bullets[x][1] += y_speed
        else:
            bullets[x][0] -= x_speed
            bullets[x][1] -= y_speed
        if bullets[x][0] > w or bullets[x][0] < -40 or bullets[x][1] < -40 or bullets[x][1] > h:
            rem.append(x)
    for r in rem:
        try:
            bullets = np.delete(bullets, r, 0)
        except:
            pass


def key_press_handle(key):
    global right, left, shift
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        right = True
        left = False

    if key[pygame.K_a] or key[pygame.K_LEFT]:
        left = True
        right = False

    if key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT]:
        shift = True


def key_release_handle(key):
    global right, left, shift
    if not key[pygame.K_d] and not key[pygame.K_RIGHT]:
        right = False

    if not key[pygame.K_a] and not key[pygame.K_LEFT]:
        left = False

    if not key[pygame.K_RSHIFT] and not key[pygame.K_LSHIFT]:
        shift = False


def draw_player_health():
    health = SegmentClass.PlayerSegment(20, h-40, GameArt.spaceship[0], wid=40, hie=40)
    display_surface.blit(health.image, health.rect)
    write_text("X"+str(player_lives), x=45, y=h-40)


def draw_destroy_meter():
    global destroy_meter
    pygame.draw.rect(display_surface, WHITE, (w-130, h-30, 100, 10), 5)
    pygame.draw.rect(display_surface, RED, (w - 130, h - 30, destroy_meter, 10))
    destroy_meter -= 0.05


def draw_score():
    write_text(score, x=w/2, y=25, size=18)


def draw_timer():
    pass


def play_music():
    if music_playing:
        pygame.mixer.music.load(GameArt.background_songs[song_no])
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.3)
    write_text("Song: " + GameArt.background_songs[song_no][20: -4], w - 200, 20)


def play_sound(sound):
    fire = pygame.mixer.Sound(sound)
    fire.play()
    pygame.time.set_timer(end_sound, end_sound_time)


def song_init():
    global music_playing, song_no
    if pygame.mixer.music.get_busy() == 0:
        song_no = random.randrange(0, len(GameArt.background_songs))
        music_playing = True
    play_music()
    if music_playing:
        music_playing = False


def movements():
    global mv_speed, player_x
    if right:
        if player_x + player_w/2 < w:
            if shift:
                player_x += mv_speed*1.5
            else:
                player_x += mv_speed
    if left:
        if player_x - player_w/2 > 0:
            if shift:
                player_x -= mv_speed * 1.5
            else:
                player_x -= mv_speed


def calc_angle():
    global angle, slope, dx

    points2 = pygame.mouse.get_pos()
    dx = points2[0] - player_x
    dy = points2[1] - player_y
    if dx != 0:
        slope = dy / dx
    angle = math.atan2(dy, dx)
    angle = math.degrees(-angle) - 90


def draw_asteroids():
    global ast_list, destroy_meter
    remover = []
    for item in ast_list:
        if item[1]+80 > 0:
            img = SegmentClass.PlayerSegment(item[0], item[1], GameArt.asteroids[item[2]], tl=True, wid=ast_w,
                                             hie=ast_h, rotate=True, angle1=item[4])
            display_surface.blit(img.image, img.rect)
            collision_detection(img.rect, item)
        item[1] += ast_speed
        item[0] += item[3]
        item[4] += 4
        if item[1] > h+100:
            remover.append(item)
    for rem in remover:
        ast_list.remove(rem)


def write_text(text, x=w/2, y=h-150, font_name='freesansbold.ttf', size=14, color=(255, 255, 255)):
    text = str(text)
    font = pygame.font.Font(font_name, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    display_surface.blit(text, text_rect)


def draw_stage():
    draw_background()


def cpu_limit():
    return psutil.cpu_percent() < 70


def collision_detection(ast_rect, index=0):
    global expl_no, dead, player_lives, player_x, counter, expl_x, ast_list, destroy_meter
    player_rect = pygame.Rect(player_x-player_w/2, player_y-player_h/2, player_w, player_h)
    if ast_rect.colliderect(player_rect):
        if (ast_rect[0]+ast_rect[2] >= player_rect[0] + player_rect[2]/2)\
                and (ast_rect[0] <= player_rect[0] + player_rect[2]*0.75):
            if index[5] == 1:
                if destroy_meter + 15 > 100:
                    destroy_meter = 100
                else:
                    destroy_meter += 15
                index[1] = 5000
                return
            dead = True
            player_lives -= 1
            ast_list.remove(index)


def collision_detection_bullet(bullet_rect, index=0):
    global ast_list, explosions, score, bullets, one_up_counter, player_lives
    for ast in ast_list:
        ast_rect = pygame.Rect(ast[0], ast[1], ast_w, ast_h)
        if bullet_rect.colliderect(ast_rect):
            center_diff = abs((ast_rect[0]+ast_rect[2]/2)-(bullet_rect[0]+bullet_rect[2]/2))
            if center_diff <= 20:
                explosions.append([ast_rect[0], ast_rect[1], 160, 160, 0, 0])
                ast[1] = 2000
                score += 1
                one_up_counter += 1
                if one_up_counter == 15:
                    player_lives += 1
                    one_up_counter = 0
                bullets[index][0] = -2000


def draw_explosion(whose):
    global expl_no, dead, player_lives, player_x, counter, explosions
    if whose == "player" and dead:
        exp = SegmentClass.PlayerSegment(player_x, player_y, GameArt.explosions[expl_no], wid=160, hie=160)
        display_surface.blit(exp.image, exp.rect)
        if expl_no < len(GameArt.explosions) - 1:
            expl_no += 1
        else:
            counter += 1
        if counter >= 15:
            reset()
        play_sound(GameArt.explosion_sound)
    exp_rem = []
    if whose == "ast":
        for e in explosions:
            ex = SegmentClass.PlayerSegment(e[0], e[1], GameArt.explosions[e[4]], wid=e[2], hie=e[3])
            display_surface.blit(ex.image, ex.rect)
            if e[4] < len(GameArt.explosions)-1:
                e[4] += 1
            else:
                e[5] += 1
            if e[5] >= 15:
                exp_rem.append(e)
            play_sound(GameArt.explosion_sound)
        for e in exp_rem:
            explosions.remove(e)


def check_fuel():
    if destroy_meter <= 0:
        draw_explosion("player")


def check_game_over():
    if player_lives == 0:
        write_text("GAME OVER", w/2, h/2, size=20)


def reset():
    global dead, counter, player_x, expl_no, destroy_meter, ast_list
    if player_lives > 0:
        counter = 0
        player_x = w/2
        expl_no = 0
        dead = False
        destroy_meter = 100
        ast_list = []


def game_init():
    display_surface.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    key_press_handle(keys)
    key_release_handle(keys)
    event_handling()


def run_game():
    game_init()
    draw_stage()
    draw_player()
    draw_player_health()
    draw_score()
    draw_timer()
    draw_bullets()
    draw_explosion("player")
    draw_explosion("ast")
    check_game_over()
    if not paused and not dead:
        movements()
        load_bullets()
        calc_angle()
        draw_destroy_meter()
        draw_asteroids()
        generate_random_x()
        song_init()
    elif paused:
        write_text("PAUSED", w/2, h/2, size=20)
    pygame.display.update()
    clock.tick(30)


def check_selector(x):
    global game_start
    if x == 0:
        game_start = True
    elif x == 1:
        pass
    elif x == 2:
        pass
    elif x == 3:
        pygame.quit()
        quit()
        sys.exit()


def gui_loader():
    global sound_play
    game_init()
    x_ = w/2
    y_ = h/2
    for x in range(len(GameArt.menu_items)):
        mous_pos = pygame.mouse.get_pos()
        w_ = 200
        h_ = 100
        rect_cords = (x_-75, y_-25, w_-50, h_-50)
        if (rect_cords[0] < mous_pos[0] < rect_cords[0]+rect_cords[2]) and \
                (rect_cords[1] < mous_pos[1] < rect_cords[1]+rect_cords[3]):
            w_ = 220
            h_ = 110
            if sound_play[x]:
                play_sound(GameArt.hover)
                sound_play[x] = False
            if mouse_pressed:
                play_sound(GameArt.bullet_sound)
                check_selector(x)
        else:
            sound_play[x] = True

        item = SegmentClass.PlayerSegment(x_, y_, GameArt.menu_items[x], wid=w_, hie=h_)
        display_surface.blit(item.image, item.rect)
        y_ += 70

    pygame.display.update()
    clock.tick(30)


while True:
    if game_start:
        run_game()
    else:
        gui_loader()

