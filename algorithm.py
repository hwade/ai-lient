import random


class Direction(object):

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value


directions = [Direction(-1, 0, 'U'), Direction(0, 1, 'R'), Direction(1, 0, 'D'), Direction(0, -1, 'L')]
stay = Direction(0, 0, 'S')


def random_action():
    index = random.randint(0, len(directions) - 1)
    return directions[index].value
