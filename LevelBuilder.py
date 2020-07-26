import SegmentClass
import GameArt

standard_wid = 170
standard_hie = 60
bricks = [[400, 200, 1, 0, False, 0, standard_wid, standard_hie], [400, 400, 0, 0, False, 0, standard_wid, standard_hie]]


def load_bricks():
    brick_obj = []
    for x in bricks:
        obj = SegmentClass.PlayerSegment(x[0], x[1], GameArt.bricks[x[2]], rotate=x[4], angle1=x[5], wid=x[6],
                                         hie=x[7], tl=True)
        brick_obj.append([obj, x[3], x[0], x[1]])
    return brick_obj
