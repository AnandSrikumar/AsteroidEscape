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
ast_event, ast_time = pygame.USEREVENT+1, 200
ast_add = True
ast_w, ast_h = 70, 80
sprite_no = 0
right, left, up, down, shift = False, False, False, False, False
mv_speed = 12
mouse_pressed = False
game_start = False
angle, slope, dx = 0, 0, 0

bullets2 = []
can_fire = True
bullet_event, bullet_event_time = pygame.USEREVENT+2, 100
end_sound, end_sound_time = pygame.USEREVENT + 2, 100
bullet_speed = 30
ast_speed = 40
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
ast_list2 = []

background_loader = SegmentClass.PlayerSegment(0, 0, GameArt.background, wid=w, hie=h, tl=True)
background_loader2 = SegmentClass.PlayerSegment(0, -h, GameArt.background, wid=w, hie=h, tl=True)
player_loader = SegmentClass.PlayerSegment(player_x, player_y, GameArt.spaceship[sprite_no], tl=False,
                                      angle1=angle, rotate=True, wid=70, hie=70)
player_sprites = GameArt.spaceship
player_objects = []
other_gui = False
gui_no = 0
health = SegmentClass.PlayerSegment(20, h-40, GameArt.spaceship[0], wid=40, hie=40)
campaign = False
loaded = False
stage_x, stage_y = 0, 0
background_camp = GameArt.background2


def loading_player():
    global player_objects
    for sprite in player_sprites:
        obj = SegmentClass.PlayerSegment(player_x, player_y, sprite, tl=False,
                                      angle1=angle, rotate=True, wid=70, hie=70)
        player_objects.append(obj)


loading_player()


def load_campaign():
    global player_x, player_y, background_camp, campaign, loaded
    player_x = 40
    player_y = h/2
    loading_player()
    background_camp = SegmentClass.PlayerSegment(0, 0, GameArt.background2, wid=w, hie=h, tl=True)
    campaign = True
    loaded = True


def generate_random_x():
    global ast_add, fuel_send
    if ast_add and cpu_limit():
        x = random.randrange(0, w-100)
        sp = random.randrange(0, 4)
        mv = random.randrange(-5, 5)

        ast_seg = SegmentClass.PlayerSegment(x, -400, GameArt.asteroids[sp], wid=ast_w, hie=ast_h, tl=True,
                                             rotate=True, angle1=0)
        ast_list2.append([ast_seg, mv, 0])
        ast_add = False
        pygame.time.set_timer(ast_event, ast_time)
        if fuel_send:
            x = random.randrange(0, w-100)

            fuel_seg = SegmentClass.PlayerSegment(x, -400, GameArt.asteroids[4], wid=ast_w, hie=ast_h, tl=True,
                                         rotate=True, angle1=0)
            ast_list2.append([fuel_seg, mv, 1])
            fuel_send = False
            pygame.time.set_timer(fuel_event, fuel_event_time)


def load_bullets():
    global can_fire, bullets, can_play_sound, bullets2
    if can_fire and mouse_pressed:
        bull = SegmentClass.PlayerSegment(player_x, player_y, GameArt.bullet, angle1=angle
                                          , rotate=True, wid=30, hie=40)
        bullets2.append([bull, slope, dx])
        pygame.time.set_timer(bullet_event, bullet_event_time)
        can_fire = False
        if can_play_sound:
            play_sound(GameArt.bullet_sound)
            can_play_sound = False
            #slope, dx


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
    global bgr_y, bgr_y2, background_loader, background_loader2
    background_loader.get_image()
    background_loader2.get_image()
    display_surface.blit(background_loader.image, background_loader.rect)
    display_surface.blit(background_loader2.image, background_loader2.rect)
    background_loader.y += 40
    background_loader2.y += 40
    if background_loader.y >= h:
        background_loader.y = -h
    if background_loader2.y > h:
        background_loader2.y = -h


def draw_background2():
    background_camp.get_image()
    display_surface.blit(background_camp.image, background_camp.rect)


def draw_player():
    global sprite_no, player_w, player_h, player_loader, player_objects
    if dead:
        return
    display_surface.blit(player_objects[sprite_no].image_copy, player_objects[sprite_no].rect)
    if sprite_no < len(GameArt.spaceship) - 1:
        sprite_no += 1
    else:
        sprite_no = 0
    for spr in player_objects:
        spr.get_image()
        player_w, player_h = spr.rect[2], spr.rect[3]
        spr.x, spr.y = player_x, player_y
        spr.angle1 = angle


def draw_bullets():
    global bullets2
    rem = []

    x_speed = bullet_speed
    for bull in bullets2:
        bull[0].get_image()
        display_surface.blit(bull[0].image, bull[0].rect)
        collision_detection_bullet(bull[0].rect, bull)
        y_speed = bull[1] * x_speed
        if bull[1] > 1:
            y_speed = bullet_speed
            x_speed = y_speed / bull[1]
        elif bull[1] < -1:
            y_speed = -bullet_speed
            x_speed = y_speed / bull[1]
        if bull[2] > 0:
            bull[0].x += x_speed
            bull[0].y += y_speed
        else:
            bull[0].x -= x_speed
            bull[0].y -= y_speed
        if bull[0].x > w or bull[0].x < -40 or bull[0].y < -40 or bull[0].y > h:
            rem.append(bull)
    for r in rem:
        try:
            bullets2.remove(r)
        except:
            pass


def key_press_handle(key):
    global right, left, shift, other_gui, up, down
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        right = True
        left = False

    if key[pygame.K_a] or key[pygame.K_LEFT]:
        left = True
        right = False

    if key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT]:
        shift = True

    if key[pygame.K_BACKSPACE] and other_gui:
        other_gui = False

    if key[pygame.K_w] or key[pygame.K_UP]:
        up = True
        down = False
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        down = True
        up = False


def key_release_handle(key):
    global right, left, shift, up, down
    if not key[pygame.K_d] and not key[pygame.K_RIGHT]:
        right = False

    if not key[pygame.K_a] and not key[pygame.K_LEFT]:
        left = False

    if not key[pygame.K_RSHIFT] and not key[pygame.K_LSHIFT]:
        shift = False
    if not key[pygame.K_w] and not key[pygame.K_UP]:
        up = False
    if not key[pygame.K_s] and not key[pygame.K_DOWN]:
        down = False


def draw_player_health():
    display_surface.blit(health.image, health.rect)
    write_text(" "+str(player_lives), x=45, y=h-40)


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


def movements2():
    global mv_speed, player_x, player_y
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

    if up:
        if player_y - player_h/2 > 0:
            if shift:
                player_y -= mv_speed*1.5
            else:
                player_y -= mv_speed

    if down:
        if player_y + player_h/2 < h:
            if shift:
                player_y += mv_speed*1.5
            else:
                player_y += mv_speed


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
    global destroy_meter, ast_list2
    remover = []
    indx = 0
    for item in ast_list2:
        if item[0].y + 80 > 0:
            item[0].get_image()
            display_surface.blit(item[0].image_copy, item[0].rect)
            collision_detection(item[0].rect, item[2], indx)
        item[0].y += ast_speed
        item[0].x += item[1]
        item[0].angle1 += 4
        if item[0].y > h+100:
            remover.append(item)
        indx += 1
    for rem in remover:
        ast_list2.remove(rem)


def draw_enemies():
    pass


def write_text(text, x=w/2, y=h-150, font_name=GameArt.fonts[0], size=14, color=(255, 255, 255)):
    text = str(text)
    font = pygame.font.Font(font_name, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    display_surface.blit(text, text_rect)


def draw_stage():
    if not loaded:
        draw_background()
    else:
        draw_background2()


def cpu_limit():
    return psutil.cpu_percent() < 70


def collision_detection(ast_rect, index=0, rem=0):
    global expl_no, dead, player_lives, player_x, counter, expl_x, destroy_meter, ast_list2
    player_rect = pygame.Rect(player_x-player_w/2, player_y-player_h/2, player_w, player_h)
    if ast_rect.colliderect(player_rect):
        if (ast_rect[0]+ast_rect[2] >= player_rect[0] + player_rect[2]/2)\
                and (ast_rect[0] <= player_rect[0] + player_rect[2]*0.75):
            if index == 1:
                if destroy_meter + 15 > 100:
                    destroy_meter = 100
                else:
                    destroy_meter += 15
                ast_list2[rem][0].y = 5000
                return
            dead = True
            player_lives -= 1
            ast_list2[rem][0].y = 5000


def collision_detection_bullet(bullet_rect, index=0):
    global explosions, score, one_up_counter, player_lives, ast_list2
    for ast in ast_list2:
        ast_rect = pygame.Rect(ast[0].x, ast[0].y, ast_w, ast_h)
        if bullet_rect.colliderect(ast_rect):
            center_diff = abs((ast_rect[0]+ast_rect[2]/2)-(bullet_rect[0]+bullet_rect[2]/2))
            if center_diff <= 20:
                explosions.append([ast_rect[0], ast_rect[1], 160, 160, 0, 0, True])
                ast[1] = 2000
                score += 1
                one_up_counter += 1
                if one_up_counter == 50:
                    player_lives += 1
                    one_up_counter = 0
                index[0].x = -2000


def draw_explosion(whose):
    global expl_no, dead, player_lives, player_x, counter, explosions
    if whose == "player" and dead:
        exp = SegmentClass.PlayerSegment(player_x, player_y, GameArt.explosions[expl_no], wid=160, hie=160)
        exp.get_image()
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
            ex.get_image()
            display_surface.blit(ex.image, ex.rect)
            if e[4] < len(GameArt.explosions)-1:
                e[4] += 1
            else:
                e[5] += 1
            if e[5] >= 15:
                exp_rem.append(e)
            if e[6]:
                play_sound(GameArt.explosion_sound)
                e[6] = False
        for e in exp_rem:
            explosions.remove(e)


def check_fuel():
    if destroy_meter <= 0:
        draw_explosion("player")


def check_game_over():
    if player_lives == 0:
        write_text("GAME OVER", w/2, h/2, size=20)


def reset():
    global dead, counter, player_x, expl_no, destroy_meter, ast_list2
    if player_lives > 0:
        counter = 0
        player_x = w/2
        expl_no = 0
        dead = False
        destroy_meter = 100
        ast_list2 = []


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
        if not loaded:
            movements()
            draw_asteroids()
            generate_random_x()
            draw_destroy_meter()
        elif loaded:
            movements2()
            draw_enemies()
        load_bullets()
        calc_angle()

        song_init()
    elif paused:
        write_text("PAUSED", w/2, h/2, size=20)
    pygame.display.update()
    clock.tick(30)


def check_selector(x):
    global game_start, gui_no
    if x == 0:
        gui_no = 0
    elif x == 1:
        gui_no = 1
    elif x == 2:
        gui_no = 2
    elif x == 3:
        pygame.quit()
        quit()
        sys.exit()


def profiler():
    write_text(len(ast_list2), 1280, 700)
    write_text(len(bullets2), 1320, 700)
    write_text(psutil.cpu_percent(), 1240, 700)


def gui_loader():
    global sound_play, other_gui, game_start
    game_init()
    x_ = w/2
    y_ = h/2
    mous_pos = pygame.mouse.get_pos()
    if other_gui:
        if gui_no == 2:
            write_text("**********A simple game made using python*********", x=330, y=340, size=20)
            write_text("Art downloaded from", x=330, y=370, size=20)
            write_text("1)opengameart.net    2)craftpix.net", x=360, y=400, size=16)
            write_text("Music credit goes to \"neffex\" and \"two steps from hill\"", x=330, y=430, size=20)
            write_text("For songs used in game, visit \"GameArt/Music/Songs\" in the game's folder", x=330,y=460, size=20)
            write_text("Made by Anand", x=330, y=490, size=20)
            write_text("Press backspace to go back", x=330, y=520, size=20)

        if gui_no == 1:
            write_text("*********Controls*********", x=330, y=340, size=20)
            write_text("Controls", x=330, y=370, size=20)
            write_text("\"d\" for moving right, \"a\" for moving left", x=360, y=400, size=16)
            write_text("We can't move up and down, we can only move left and right", x=330, y=430, size=20)
            write_text("We have to shoot and escape from asteroids", x=330, y=460,
                       size=20)
            write_text("Press ESC to exit the game", x=330, y=490, size=20)
            write_text("Press backspace to go back", x=330, y=520, size=20)
        if gui_no == 0:
            pygame.draw.rect(display_surface, (0, 0, 255), (x_-90, y_+40, 220, 70))
            pygame.draw.rect(display_surface, (0, 0, 255), (x_-90, y_+190, 220, 70))
            write_text("ARCADE", x=x_-20, y=y_+50)
            write_text("CAMPAIGN", x=x_-20, y=y_+200)
            rect1 = pygame.Rect(x_-90, y_+40, 220, 70)
            rect2 = pygame.Rect(x_-90, y_+190, 220, 70)
            if rect1.collidepoint(mous_pos) and mouse_pressed:
                game_start = True
            if rect2.collidepoint(mous_pos) and mouse_pressed:
                if not loaded:
                    load_campaign()
                    game_start = True
        pygame.display.update()
        clock.tick(30)
        return
    for x in range(len(GameArt.menu_items)):
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
                other_gui = True
        else:
            sound_play[x] = True

        item = SegmentClass.PlayerSegment(x_, y_, GameArt.menu_items[x], wid=w_, hie=h_)
        item.get_image()
        display_surface.blit(item.image, item.rect)
        y_ += 70

    pygame.display.update()
    clock.tick(30)


while True:
    if game_start:
        run_game()
    else:
        gui_loader()

