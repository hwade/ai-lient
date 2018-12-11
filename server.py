from sanic import Sanic
from sanic import response
import sys
import time
from game import *
from config import *
from logger import *

import logging

logger = logging.getLogger("SERVER")

app = Sanic()


@app.post("/start")
async def start(req):
    logger.info("比赛开始, req: %s", req.json)
    return response.json({})


@app.post("/end")
async def end(req):
    logger.info("比赛结束, req: %s", req.json)
    return response.json({})


@app.post("/step")
async def step(req):
    start_time = time.time()
    data = req.json

    player1 = get_player(data['player1'])
    player2 = get_player(data['player2'])
    walls = get_walls(data['walls'])
    jobs = get_jobs(data['jobs'])

    game.player1 = player1
    game.player2 = player2
    game.walls = walls
    game.jobs = jobs

    game.refresh(player_name)
    action = game.step()
    logger.info("action: %s", action)

    logger.info("耗时：%ss", time.time() - start_time)
    return response.json({'action': action})


def get_player(p):
    player = Player(p['x'], p['y'])
    player.name = p['name']
    player.home = Point(p['home_x'], p['home_y'])
    player.nJobs = p['n_jobs']
    player.value = p['value']
    player.score = p['score']
    return player


def get_walls(walls_data):
    return [Wall(w['x'], w['y']) for w in walls_data]


def get_jobs(jobs_data):
    return [Job(j['x'], j['y'], j['value']) for j in jobs_data]


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    logger.info("started")

if __name__ == "__main__":
    if sys.argv[1].isdigit():
        port = int(sys.argv[1])
    init_logger('SERVER', 'DEBUG')
    app.run(host="0.0.0.0", port=port)
