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
    cur_player = game.current_player
    enemy = game.player2 if game.player1.name == cur_player.name else game.player1
    logger_alg.info('Current pos: (%d, %d)' % (current_point.x, current_point.y))
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
                if isReachPoint(new_pt, matrix, enemy) and step_matrix[new_pt.x,new_pt.y] == 1:
                    queue.put(new_pt)
                    step_matrix[new_pt.x, new_pt.y] = step_matrix[cur_pt.x, cur_pt.y] + 1
        job_value = np.ones(step_matrix.shape) * (jobs[j].value)**2 / (np.power(step_matrix, 2))
        for wall in walls: job_value[wall.x, wall.y] = 0
        job_value[enemy.home.x, enemy.home.y] = 0
        #printHotMap(job_value)
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
            if isReachPoint(new_pt, matrix, enemy) and g_matrix[new_pt.x,new_pt.y] == 1:
                queue.put(new_pt)
                g_matrix[new_pt.x, new_pt.y] = g_matrix[cur_pt.x, cur_pt.y] + 1
    if game.current_player.nJobs == 10: h_matrix = np.ones(h_matrix.shape)
    
    g_matrix = alpha * np.ones(g_matrix.shape) * np.power(g_matrix, 5)
    g_matrix = g_matrix / (np.max(g_matrix) - np.min(g_matrix) + .0001)
    for wall in walls: g_matrix[wall.x, wall.y] = 1
    g_matrix[enemy.home.x, enemy.home.y] = 1
                
    weight = (game.current_player.nJobs - threshold) / 10.#float(10 + - threshold) 
    
    g_matrix[home.x, home.y] = -weight
    cost_map = (1 - weight) * h_matrix - (1 + weight) * g_matrix
    
    for row in matrix:
        for cell in row:
            print('%2d '% (cell.cell_type), end='')
        print()
    print()
    printHotMap(h_matrix)
    printHotMap(g_matrix)
    printHotMap(cost_map)
    return getMaxScoreDirection(game.current_player, enemy, cost_map, matrix)
            
def getNextNearPoint(point, direction):
    return Point(point.x + direction.x, point.y + direction.y)
            
def isReachPoint(point, matrix, player):
    WALL_LEN = len(matrix)
    if point.x < 0 or point.x >= WALL_LEN or point.y < 0 or point.y >= WALL_LEN or \
        matrix[point.x][point.y].cell_type in [CELL_TYPE_WALL, matrix[player.home.x][player.home.y].cell_type]:
        return False
    return True
    
def getMaxScoreDirection(player, enemy, value_matrix, raw_matrix):
    max_score = value_matrix[player.x, player.y]
    cur_direction = STAY
    logger_alg.info('Current score: %.4f' % max_score)
    for direction in DIRECTIONS:
        next_pt = getNextNearPoint(player, direction)
        if isReachPoint(next_pt, raw_matrix, enemy) and value_matrix[next_pt.x, next_pt.y] > max_score:
            logger_alg.info('Direction %s: %.4f' % (direction.value, value_matrix[next_pt.x, next_pt.y]))
            max_score = value_matrix[next_pt.x, next_pt.y]
            cur_direction = direction
    if cur_direction == STAY:
        logger_alg.info('Njobs: %d' % (player.nJobs))
    return cur_direction.value

def printHotMap(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix)):
            print('%.2f ' % matrix[x][y], end='')
        print()
    print('-'*20)
