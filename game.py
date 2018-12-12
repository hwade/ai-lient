import random
from constants import *
from algorithm import *
from base import *
import logging

logger = logging.getLogger("SERVER.GAME")

class Game(object):

    def __init__(self, player1=None, player2=None, walls=None, jobs=None):
        self.matrix = [[Cell(x, y, CELL_TYPE_EMPTY) for y in range(GAME_BOARD_SIZE)] for x in range(GAME_BOARD_SIZE)]
        self.current_player = Player()
        self.player1 = player1
        self.player2 = player2
        self.walls = walls
        self.jobs = jobs
    
    def refresh(self, player_name):
        self.refresh_matrix()
        self.refresh_player(player_name)
        logger.debug("刷新棋盘完成，current_player: %s", self.current_player.name)
        for row in self.matrix:
            for cell in row:
                print('%2d ' % (cell.cell_type), end='')
            print()
        print()

    def refresh_matrix(self):
        for row in self.matrix:
            for cell in row:
                cell.cell_type = CELL_TYPE_EMPTY
                cell.cell_value = None

        c1 = self.matrix[self.player1.x][self.player1.y]
        c1.cell_type = CELL_TYPE_PLAYER
        c1.cell_value = self.player1
        
        c1h = self.matrix[self.player1.home.x][self.player1.home.y]
        c1h.cell_type = CELL_TYPE_HOME1

        c2 = self.matrix[self.player2.x][self.player2.y]
        c2.cell_type = CELL_TYPE_PLAYER
        c2.cell_value = self.player2
        
        c2h = self.matrix[self.player2.home.x][self.player2.home.y]
        c2h.cell_type = CELL_TYPE_HOME2

        for wall in self.walls:
            self.matrix[wall.x][wall.y].cell_type = CELL_TYPE_WALL

        for job in self.jobs:
            cell = self.matrix[job.x][job.y]
            cell.cell_type = CELL_TYPE_JOB
            cell.cell_value = job

    def refresh_player(self, player_name):
        if player_name == self.player1.name:
            player = self.player1
        else:
            player = self.player2
        self.current_player.name = player.name
        self.current_player.x = player.x
        self.current_player.y = player.y
        self.current_player.home = player.home
        self.current_player.nJobs = player.nJobs
        self.current_player.value = player.value
        self.current_player.score = player.score

    def step(self):
        if self.player1.name == self.current_player.name:
            return getDirectionByCostMap(self, alpha=1, threshold=6)
        return getDirectionByCostMap(self, alpha=1, threshold=7)


game = Game()
