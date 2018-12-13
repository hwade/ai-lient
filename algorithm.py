import random
from queue import Queue
from constants import *
from base import Point
import numpy as np
import logging

logger_alg = logging.getLogger("SERVER.ALGORITHM")
         
class Direction(object):

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

DIRECTIONS = [Direction(-1, 0, 'U'), Direction(0, 1, 'R'), Direction(1, 0, 'D'), Direction(0, -1, 'L')]
STAY = Direction(0, 0, 'S')


def random_action():
    index = random.randint(0, len(DIRECTIONS) - 1)
    return DIRECTIONS[index].value
    
