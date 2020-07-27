import SegmentClass
import GameArt

standard_wid = 170
standard_hie = 60
bricks = [[400, 200, 1, 0, False, 0, standard_wid, standard_hie],
          [400, 400, 0, 0, False, 0, standard_wid, standard_hie],
          [600, 400, 2, 1, False, 0, standard_wid, standard_hie]]

enemies = [[800, 300, 1, 1, True, 0, 50, 50]]


def load_elements(type):
    elem_obj = []
    items = []
    sprites = []
    if type == "bricks":
        items = bricks
        sprites = GameArt.bricks
    elif type == "enemies":
        items = enemies
        sprites = GameArt.enemies

    for x in items:
        obj = SegmentClass.PlayerSegment(x[0], x[1], sprites[x[2]], rotate=x[4], angle1=x[5], wid=x[6],
                                         hie=x[7], tl=True)
        elem_obj.append([obj, x[3], x[0], x[1]])
    return elem_obj

