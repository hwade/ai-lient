class Array2D:
    """
        说明：
            1.构造方法需要两个参数，即二维数组的宽和高
            2.成员变量w和h是二维数组的宽和高
            3.使用：‘对象[x][y]’可以直接取到相应的值
            4.数组的默认值都是0
    """
    def __init__(self,w,h):
        self.w=w
        self.h=h
        self.data=[]
        self.data=[[0 for y in range(h)] for x in range(w)]
 
 
    def showArray2D(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.data[x][y],end=' ')
            print("")
 
    def __getitem__(self, item):
        return self.data[item]
        
class Point:
    """
    表示一个点
    """
    def __init__(self,x,y):
        self.x=x;self.y=y
 
    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False
    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)
        
class AStar:
    """
    AStar算法的Python3.x实现
    """
    class Node:    #描述AStar算法中的节点数据
        def __init__(self,point,endPoint,g=0):
            self.point=point        #自己的坐标
            self.father=None        #父节点
            self.g=g                #g值，g值在用到的时候会重新算
            self.h=(abs(endPoint.x-point.x)+abs(endPoint.y-point.y))*10  #计算h值
 
    def __init__(self, map2d, startPoint, endPoint, passTag=0):
        """
        构造AStar算法的启动条件
        :param map2d: Array2D类型的寻路数组
        :param startPoint: Point类型的寻路起点
        :param endPoint: Point类型的寻路终点
        :param passTag: int类型的可行走标记（若地图数据!=passTag即为障碍）
        """
        #开启表
        self.openList=[]
        #关闭表
        self.closeList=[]
        #寻路地图
        self.map2d=map2d
        #起点终点
        self.startPoint=startPoint
        self.endPoint=endPoint
        #可行走标记
        self.passTag=passTag
 
    def getMinNode(self):
        """
        获得openlist中F值最小的节点
        :return: Node
        """
        currentNode=self.openList[0]
        for node in self.openList:
            if node.g+node.h < currentNode.g+currentNode.h:
                currentNode=node
        return currentNode
 
    def pointInCloseList(self,point):
        for node in self.closeList:
            if node.point==point:
                return True
        return False
 
    def pointInOpenList(self,point):
        for node in self.openList:
            if node.point==point:
                return node
        return None
 
    def endPointInCloseList(self):
        for node in self.openList:
            if node.point==self.endPoint:
                return node
        return None
 
    def searchNear(self,minF,offsetX,offsetY):
        """
        搜索节点周围的点
        :param minF:
        :param offsetX:
        :param offsetY:
        :return:
        """
        #越界检测
        if minF.point.x+offsetX<0 or minF.point.x+offsetX>self.map2d.w-1 or minF.point.y + offsetY < 0 or minF.point.y + offsetY > self.map2d.h - 1:
            return
        #如果是障碍，就忽略
        if self.map2d[minF.point.x+offsetX][minF.point.y+offsetY]!=self.passTag:
            return
        #如果在关闭表中，就忽略
        if self.pointInCloseList(Point(minF.point.x+offsetX,minF.point.y+offsetY)):
            return
        #设置单位花费
        if offsetX==0 or offsetY==0:
            step=10
        else:
            step=14
        #如果不再openList中，就把它加入openlist
        currentNode=self.pointInOpenList(Point(minF.point.x+offsetX,minF.point.y+offsetY))
        if not currentNode:
            currentNode=AStar.Node(Point(minF.point.x+offsetX,minF.point.y+offsetY),self.endPoint,g=minF.g+step)
            currentNode.father=minF
            self.openList.append(currentNode)
            return
        #如果在openList中，判断minF到当前点的G是否更小
        if minF.g+step<currentNode.g: #如果更小，就重新计算g值，并且改变father
            currentNode.g = minF.g + step
            currentNode.father = minF
 
    def start(self):
        '''
        开始寻路
        :return: None或Point列表（路径）
        '''
        #1.将起点放入开启列表
        startNode=AStar.Node(self.startPoint,self.endPoint)
        self.openList.append(startNode)
        #2.主循环逻辑
        while True:
            #找到F值最小的点
            minF=self.getMinNode()
            #把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)
            #判断这个节点的上下左右节点
            self.searchNear(minF,0,-1)
            self.searchNear(minF, 0, 1)
            self.searchNear(minF, -1, 0)
            self.searchNear(minF, 1, 0)
            #判断是否终止
            point=self.endPointInCloseList()
            if point:  #如果终点在关闭表中，就返回结果
                # print("关闭表中")
                cPoint=point
                pathList=[]
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint=cPoint.father
                    else:
                        # print(pathList)
                        # print(list(reversed(pathList)))
                        # print(pathList.reverse())
                        return list(reversed(pathList))
            if len(self.openList)==0:
                return None
if __name__ == '__main__':
    import time
    WALL_X, WALL_Y = 12, 12
    map2d=Array2D(WALL_X, WALL_Y)
    
    map2d[6][0]= '='
    map2d[1][0]= '='
    map2d[1][1] = '='
    map2d[1][2] = '='
    map2d[1][5] = '='
    map2d[1][8] = '='
    map2d[4][1] = '='
    map2d[4][6] = '='
    map2d[4][7] = '='
    map2d[5][7] = '='
    map2d[6][0] = '='
    map2d[2][10] = '='
    map2d[3][9] = '='
    map2d[7][2] = '='
    map2d[7][6] = '='
    map2d[8][2] = '='
    map2d[8][3] = '='
    map2d[8][10] = '='
    map2d[8][11] = '='
    map2d[10][2] = '='
    map2d[10][6] = '='
    map2d[10][7] = '='
    map2d[11][1] = '='
    map2d[11][10] = '='
    
    map2d.showArray2D()
    s_t = time.time()
    start = (0,0)
    for x in range(WALL_X):
        for y in range(WALL_Y):
            #map2d[start[0]][start[1]] = 'B'
            #map2d[x][y] = 'E'
            print('-'*30)
            aStar = None
            aStar = AStar(map2d,Point(start[0],start[1]),Point(x,y))
            pathList = aStar.start()
            if pathList is None: 
                print('(%d, %d)->(%d, %d) no path!' % (start[0], start[1], x, y))
                continue
            for point in pathList:
                map2d[point.x][point.y] = '*'
                # print(point)
            map2d.showArray2D()
            for point in pathList:
                map2d[point.x][point.y] = 0
    print('cost: %.4fs' % (time.time() - s_t))
