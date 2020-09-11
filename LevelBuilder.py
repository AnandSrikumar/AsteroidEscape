import SegmentClass
import GameArt

standard_wid = 110
standard_hie = 30
e_wid, e_hie = 40, 40
ob_w, ob_h = 60, 30
c_w, c_h = 20, 20
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
          [6345, 390, 1, 0, False, 0, standard_wid, standard_hie],
          [14000, 0, 1, 0, True, 90, standard_wid, standard_hie],
          [14000, 110, 1, 0, True, 90, standard_wid, standard_hie],
          [14000, 220, 1, 0, True, 90, standard_wid, standard_hie],
          [14000, 330, 1, 0, True, 90, standard_wid, standard_hie],
          [14000, 550, 1, 0, True, 90, standard_wid, standard_hie],
          [14000, 660, 1, 0, True, 90, standard_wid, standard_hie],
          [14000, 440, 3, 2, False, 0, standard_hie, standard_wid],
          [15650, 0, 1, 0, True, 90, standard_wid, standard_hie],
          [15650, 110, 1, 0, True, 90, standard_wid, standard_hie],
          [15650, 220, 1, 0, True, 90, standard_wid, standard_hie],
          [15650, 330, 1, 0, True, 90, standard_wid, standard_hie],
          [15650, 440, 1, 0, True, 90, standard_wid, standard_hie],
          [15650, 550, 1, 0, True, 90, standard_wid, standard_hie],
          [15650, 660, 1, 0, True, 90, standard_wid, standard_hie],
          ]

enemies = [[800, 300, 1, 1, True, 0, e_wid, e_hie, 10, 10, 15, 30, 1, 0, 10, [10, 20]],
           [7590, 580, 2, 1, True, 0, e_wid+10, e_hie+10, 10, 10, 25, 40, 0, 1, 15, [30, 30]],
           [7985, 400, 0, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [8285, 720, 2, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [8585, 400, 0, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [8885, 720, 2, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [9185, 400, 0, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [9485, 720, 3, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [9785, 400, 2, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [10085, 720, 1, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [10385, 400, 0, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [10685, 720, 1, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [10985, 400, 2, 1, True, 0, e_wid, e_hie, 15, 15, 10, 40, 0, 0, 10, [10, 20]],
           [13500, 100, 1, 1, True, 0, e_wid, e_hie, 10, 10, 10, 40, 0, 0, 10, [10, 20]],
           [13500, 700, 0, 1, True, 0, e_wid, e_hie, 10, 10, 10, 40, 0, 0, 10, [10, 20]],
           [13900, 400, 3, 1, True, 0, e_wid, e_hie, 10, 10, 10, 40, 0, 0, 10, [10, 20]],
           [15400, 100, 3, 1, True, 0, e_wid, e_hie, 10, 10, 10, 40, 0, 0, 10, [10, 20]],
           [15400, 400, 0, 1, True, 0, e_wid*2, e_hie*2, 10, 10, 160, 100, 0, 1, 15, [40, 40]],
           [15400, 700, 3, 1, True, 0, e_wid, e_hie, 10, 10, 10, 40, 0, 0, 10, [10, 20]]
           ]
objects = [[455, 245, 2, 0,  True, 180, ob_w, ob_h, 10, 10, 1, 0, 0, 10],
           [1055, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0, 0, 10],
           [2855, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0, 0, 10],
           [4055, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0, 0, 10],
           [5855, 145, 2, 0, True, 180, ob_w, ob_h, 10, 10, 1, 0, 0, 10],
           [6400, 350, 4, 1, False, 0, c_w, c_h, 0, 0, 0, -50, -1, -1],
           [7720, 150, 6, 2, False, 0, c_w*2, c_h*2, 0, 0, 0, -50, -1, -1],
           [12020, 440, 5, 4, False, 0, c_w*2, c_h*2, 0, 0, 0, 0, -1, -1],
           [11000, 25, 2, 0,  True, 180, ob_w, ob_h, 15, 15, 1, 0, 0, 10],
           [10000, 25, 2, 0,  True, 180, ob_w, ob_h, 15, 15, 1, 0, 0, 10],
           [15650, 400, 0, 5, True, 90, ob_w, ob_h*4, 0, 0, 0, 0, -1, -1]]

event_trigger = [[14100, 0, 0, 0]]
#[x, y, type, verticle/horizontal]


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

        x = 510
        y = h/2
        low, high = 700, 400
        adder = 1
        while x < 5855:
            objects.append([x, y, 3, 1, False, 0, c_w, c_h, 0, 0, 0, 10, -1, -1])
            x += 2*c_w
            if adder > 0:
                y += 2*c_h
            else:
                y -= 2*c_h
            if y > low:
                adder = -1
            if y < high:
                adder = 1
        x, y = 7655, 0
        i, sp, bt = 0, 1, 0
        while y < h:
            if i == 5:
                bt = 1
                sp = 2
            bricks.append([x, y, sp, bt, True, 90, standard_wid, standard_hie])
            y += standard_wid
            i += 1
            if bt == 1:
                bt = 0
                sp = 1

        x, y = 7685, h/2-75
        while x < 12000:
            bricks.append([x, y, 0, 0, False, 0, standard_wid, standard_hie])
            x += standard_wid
        x, y, i = 7790, 150, 1
        while x < 11950:
            objects.append([x, y, 3, 1, False, 0, c_w, c_h, 0, 0, 0, 10, -1, -1])
            x += 2*c_w
            if i > 0:
                y += 2*c_h
                i = -1
            else:
                y -= 2*c_h
                i = 1


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
            elem_obj.append([obj, x[3], x[0], x[1], x[8], x[9], [-1, -1], 0, 0, False, x[10], x[11],
                             x[12], x[13], x[14], x[15]])
        elif type == "objects":
            elem_obj.append([obj, x[3], x[0], x[1], x[8], x[9], x[10], x[11], x[12], x[13]])
    return elem_obj


#enemies [sprite object, shoots bullet, x, y, bullet_reload, wait till next bullet, movement bonds, dx, slope, did appear, their health]
