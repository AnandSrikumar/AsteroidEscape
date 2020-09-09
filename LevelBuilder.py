import SegmentClass
import GameArt

standard_wid = 110
standard_hie = 30
e_wid, e_hie = 40, 40
ob_w, ob_h = 60, 30
bricks = [[400, 200, 1, 0, False, 0, standard_wid, standard_hie],
          [1000, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [1600, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [2200, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [2800, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [3400, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [4000, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [4600, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [5200, 100, 1, 0, False, 0, standard_wid, standard_hie],
          [5800, 100, 1, 0, False, 0, standard_wid, standard_hie],
          ]

enemies = [[800, 300, 1, 1, True, 0, e_wid, e_hie, 10, 10, 15, 30]]
objects = [[455, 245, 2, 0,  True, 180, ob_w, ob_h, 10, 10, 1, 0],
           [1055, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0],
           [2855, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0],
           [4055, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0],
           [5855, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0]]


def generate_builders(w, h, st_x, level):
    global bricks, objects, enemies
    if level == 0:
        y = h-standard_hie
        y2 = -25
        x = -1
        while x < st_x+2*standard_wid:
            bricks.append([x, y, 1, 0, False, 0, standard_wid, standard_hie])
            bricks.append([x, y2, 1, 0, False, 0, standard_wid, standard_hie])
            x += standard_wid


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
            elem_obj.append([obj, x[3], x[0], x[1], x[8], x[9], [-1, -1], 0, 0, False, x[10], x[11]])
        elif type == "objects":
            elem_obj.append([obj, x[3], x[0], x[1], x[8], x[9], x[10], x[11]])
    return elem_obj


#enemies [sprite object, shoots bullet, x, y, bullet_reload, wait till next bullet, movement bonds, dx, slope, did appear, their health]
