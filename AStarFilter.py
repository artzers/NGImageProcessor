import os, numpy as np, cv2

class PathNode:
    def __init__(self, x,y,g,h,pnode=(0,0)):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.val = self.h + self.g
        self.pnode = pnode


class AStarFilter:
    def __init__(self):
        pass

    def AStarDemo(self):
        img = cv2.imread("Astar.jpg", cv2.IMREAD_UNCHANGED)
        initPos = ( 200, 127)
        endPos = (210,400)#(180, 400)
        img = self.AStar(img, initPos, endPos)
        img[initPos] = 255
        img[endPos] = 255
        cv2.namedWindow("img")
        cv2.imshow("img", img)
        cv2.waitKey(0)

    def AStar(self, img, initPos, endPos):
        #I suppose that path cost is 1 all of the image
        openList = dict()
        openImg = np.zeros(img.shape, np.uint8)#0 is not used, 1 is opened, 2 is closed
        #fImg = np.zeros(img.shape, np.uint8)
        curPos = initPos
        openList[(curPos[0],curPos[1])]=PathNode(curPos[0],curPos[1],0,0, curPos)
        allList = openList.copy()
        openList, openImg = self.SearchOpenNode(img, openImg, curPos, endPos, openList, allList)
        allList.update(openList)
        openImg[curPos] = 2
        openList.pop(curPos)
        ind = 0
        flag = True
        while not self.IsGetEndPos(allList, endPos) and openList:
            ind +=1
            if np.mod(ind, 1000) == 0:
                print ind
            if ind == 3000:
                flag = False
                break
            sortedOpenList = sorted(openList.items(), lambda x,y:cmp(x[1].val, y[1].val))
            curPos = sortedOpenList[0][0]
            #print curPos
            openList, openImg = self.SearchOpenNode(img, openImg, curPos, endPos, openList, allList)
            allList.update(openList)
            openImg[curPos] = 2
            openList.pop(curPos)
        for i in allList:
            img[i[0],i[1]] += 50
        #get path
        if flag:
            pathWay=list()
            pathIter = endPos
            while pathIter != initPos:
                pathWay.append(pathIter)
                pathIter = allList[pathIter].pnode
            for i in pathWay:
                img[i[0],i[1]] = 255
        return img

    def IsGetEndPos(self, openList, endPos):
        if openList.has_key(endPos):
            return True
        else:
            return False

    def CalDistance(self, i,j,endPos):
        return 0.0 * (np.abs(i-endPos[0]) +np.abs(j-endPos[1]))

    def SearchOpenNode(self, img, openImg, curPos, endPos, openList, allList):
        for i in xrange(curPos[0]-1, curPos[0] + 2):
            for j in xrange(curPos[1] - 1, curPos[1] + 2):
                if img[i,j] != 0 or (i,j) == curPos or i < 0 or i > img.shape[0]-1 or j < 0 or j > img.shape[1] - 1:
                    continue
                if openImg[i,j] == 0:
                    openImg[i,j] == 1
                    #val = 1+ allList[(curPos[0],curPos[1])].val#+ np.sqrt((i-endPos[0]) ** 2.0 +(j-endPos[1]) ** 2.0)
                    openList[(i,j)] = PathNode(i,j,1+ allList[(curPos[0],curPos[1])].g, self.CalDistance(i,j,endPos) ,curPos)
                if openImg[i,j] == 1:
                    tmpWet = 1+allList[(curPos[0],curPos[1])].g+ self.CalDistance(i,j,endPos)
                    #np.sqrt((i-endPos[0]) ** 2.0 +(j-endPos[1]) ** 2.0)
                    if tmpWet < openList[(i,j)].val :
                        openList[(i,j)].pnode = curPos
                        openList[(i, j)].g = 1+allList[(curPos[0],curPos[1])].g
                        openList[(i, j)].h = np.abs(i-endPos[0]) +self.CalDistance(i,j,endPos) #np.sqrt((i-endPos[0]) ** 2.0 +(j-endPos[1]) ** 2.0)
                        openList[(i, j)].val = openList[(i, j)].g + openList[(i, j)].h
        return openList, openImg

astar = AStarFilter()
astar.AStarDemo()
