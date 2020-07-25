import SegmentClass
import GameArt

bricks = [[400, 200, 1, 0, False, 0], [400, 400, 0, 0, False, 0]]


def load_bricks():
    brick_obj = []
    for x in bricks:
        obj = SegmentClass.PlayerSegment(x[0], x[1], GameArt.bricks[x[2]], rotate=x[4], angle1=x[5])
        brick_obj.append([obj, x[3], x[0], x[1]])
    return brick_obj
