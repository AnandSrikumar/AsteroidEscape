import SegmentClass
import GameArt

standard_wid = 170
standard_hie = 60
bricks = [[400, 200, 1, 0, False, 0, standard_wid, standard_hie],
          [1000, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [1600, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [2200, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [2800, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [3400, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [4000, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [4600, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [5200, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [5800, 100, 1, 0, False, 0, standard_wid, standard_hie]]

enemies = [[800, 300, 1, 1, True, 0, 50, 50, 10, 10]]
objects = [[485, 280, 2, 0,  True, 180, 80, 50, 10, 10, 1],
           [1085, 180, 2, 0, True, 180, 80, 50, 10, 10, 1],
           [2885, 180, 2, 0, True, 180, 80, 50, 10, 10, 1],
           [4085, 180, 2, 0, True, 180, 80, 50, 10, 10, 1],
           [5885, 180, 2, 0, True, 180, 80, 50, 10, 10, 1]]


def generate_builders():
    global bricks, enemies, objects
    y = 500
    x = -1
    while x < 6000:
        bricks.append([x, y, 1, 0, False, 0, standard_wid, standard_hie])
        x += standard_wid
    x = 8200
    y = -10
    while y < 6410:
        if not 4600 < y < 4800:
            bricks.append([x, y, 1, 0, True, 90, standard_wid, standard_hie])
        y += standard_hie


def load_elements(type):
    elem_obj = []
    items = []
    sprites = []
    top_left = True
    if type == "bricks":
        items = bricks
        sprites = GameArt.bricks
    elif type == "enemies":
        items = enemies
        sprites = GameArt.enemies
        top_left = False
    elif type == "objects":
        items = objects
        sprites = GameArt.objects
        top_left = False
    for x in items:
        obj = SegmentClass.PlayerSegment(x[0], x[1], sprites[x[2]], rotate=x[4], angle1=x[5], wid=x[6],
                                         hie=x[7], tl=top_left)
        if type == "bricks":
            elem_obj.append([obj, x[3], x[0], x[1]])
        elif type == "enemies":
            elem_obj.append([obj, x[3], x[0], x[1], x[8], x[9], [-1, -1], 0, 0, False, 15])
        elif type == "objects":
            elem_obj.append([obj, x[3], x[0], x[1], x[8], x[9], x[10]])
    return elem_obj


#enemies [sprite object, shoots bullet, x, y, bullet_reload, wait till next bullet, movement bonds, dx, slope, did appear, their health]
