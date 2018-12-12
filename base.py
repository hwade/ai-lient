class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Player(Point):

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.name = ''
        self.home = None
        self.nJobs = 0
        self.value = 0
        self.score = 0


class Wall(Point):

    def __init__(self, x, y):
        super().__init__(x, y)


class Job(Point):

    def __init__(self, x, y, value=0):
        super().__init__(x, y)
        self.value = value


class Cell(Point):
    def __init__(self, x, y, cell_type, cell_value=None):
        super().__init__(x, y)
        self.cell_type = cell_type
        self.cell_value = cell_value

