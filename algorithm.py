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
    
def getDirectionByCostMap(game, alpha=1, threshold=5):
    current_point = Point(game.current_player.x, game.current_player.y)
    logger_alg.debug('Current pos: (%d, %d)' % (current_point.x, current_point.y))
    home = game.current_player.home
    matrix = game.matrix
    width, height = len(matrix), len(matrix)
    walls = game.walls
    jobs = game.jobs
    h_matrix = np.zeros([len(jobs), height, width])
    queue = Queue()
    for j in range(len(jobs)):
        queue.put(Point(jobs[j].x, jobs[j].y))
        step_matrix = np.ones([height, width])
        step_matrix[jobs[j].x, jobs[j].y] = 0.9 
        while not queue.empty():
            cur_pt = queue.get()
            for direction in DIRECTIONS:
                new_pt = getNextNearPoint(cur_pt, direction)
                if isReachPoint(new_pt, matrix) and step_matrix[new_pt.x,new_pt.y] == 1:
                    queue.put(new_pt)
                    step_matrix[new_pt.x, new_pt.y] = step_matrix[cur_pt.x, cur_pt.y] + 1
        job_value = np.ones(step_matrix.shape) * (jobs[j].value)**2 / (np.power(step_matrix, 2))
        for wall in walls: job_value[wall.x, wall.y] = 0
        if game.player1 == game.current_player:
            job_value[game.player2.home.x, game.player2.home.y] = 0
        else:
            job_value[game.player1.home.x, game.player1.home.y] = 0
        h_matrix[j] = job_value
    h_matrix = np.sum(h_matrix, axis=0)
    h_matrix = h_matrix / np.max(h_matrix)
    
    queue.put(Point(home.x, home.y))
    g_matrix = np.ones([height, width])
    g_matrix[home.x, home.y] = 0.9
    while not queue.empty():
        cur_pt = queue.get()
        for direction in DIRECTIONS:
            new_pt = getNextNearPoint(cur_pt, direction)
            if isReachPoint(new_pt, matrix) and g_matrix[new_pt.x,new_pt.y] == 1:
                queue.put(new_pt)
                g_matrix[new_pt.x, new_pt.y] = g_matrix[cur_pt.x, cur_pt.y] + 1
    weights = np.exp(game.current_player.nJobs-threshold)
    if weights < 0: weights = 0.0
    g_matrix = alpha * np.ones(g_matrix.shape) * weights / np.power(g_matrix, 2)
    for wall in walls: g_matrix[wall.x, wall.y] = 0
    if game.player1 == game.current_player: g_matrix[game.player2.home.x, game.player2.home.y] = 0
    else: g_matrix[game.player1.home.x, game.player1.home.y] = 0
    g_matrix = -1 * g_matrix / (np.max(g_matrix) + .0001)
                
    cost_map = g_matrix + h_matrix
    for row in matrix:
        for cell in row:
            print('%2d '% (cell.cell_type), end='')
        print()
    print()
    print(h_matrix)
    print(g_matrix)
    print(cost_map)
    return getMaxScoreDirection(current_point, cost_map, matrix)
            
def getNextNearPoint(point, direction):
    return Point(point.x + direction.x, point.y + direction.y)
            
def isReachPoint(point, matrix):
    WALL_LEN = len(matrix)
    if point.x < 0 or point.x >= WALL_LEN or point.y < 0 or point.y >= WALL_LEN or \
        matrix[point.x][point.y].cell_type in [CELL_TYPE_WALL, CELL_TYPE_HOME2]:
        return False
    return True
    
def getMaxScoreDirection(current_point, value_matrix, raw_matrix):
    max_score = value_matrix[current_point.x, current_point.y]
    cur_direction = STAY
    logger_alg.debug('Current score: %.4f' % max_score)
    for direction in DIRECTIONS:
        next_pt = getNextNearPoint(current_point, direction)
        if isReachPoint(next_pt, raw_matrix) and value_matrix[next_pt.x, next_pt.y] > max_score:
            max_score = value_matrix[next_pt.x, next_pt.y]
            cur_direction = direction
    return cur_direction.value
    
