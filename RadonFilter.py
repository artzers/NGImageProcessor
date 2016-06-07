import os, numpy as np, cv2

class RadonFilter:
    def __init__(self):
        pass


    def RadonDemo(self):
        img = cv2.imread('./SheppLogan_Phantom.tif',cv2.IMREAD_UNCHANGED)
        angleStep = 1.0
        rimg = self.RadonFilter(img, angleStep)
        iimg = self.IRadonFilter(rimg, img.shape, angleStep)
        #cv2.namedWindow('orig')
        #cv2.imshow('orig', img)
        #cv2.waitKey(0)

    def RadonFilter(self, img, angleStep):
        #img -= 128
        angleNum = np.int32(180.0 / angleStep)
        rotateImg = np.zeros(img.shape, np.int32)
        radonImg = np.zeros((angleNum, img.shape[0]),np.int32)
        for i in xrange(0, angleNum):
            angle = np.float(i) * angleStep
            M = cv2.getRotationMatrix2D((img.shape[0]/2, img.shape[1]/2), angle, 1.0)
            rotateImg=cv2.warpAffine(img, M, img.shape)
            radonImg[i,:] = np.sum(rotateImg, axis=0)
        # cv2.namedWindow('radon')
        # cv2.imshow('radon', radonImg)
        # cv2.waitKey(0)
        return radonImg


    def IRadonFilter(self, rimg, imgsz, angleStep):
        iimg = np.zeros(imgsz, np.float)
        #print imgsz
        #angleNum = np.int32(180.0 / angleStep)
        for i in xrange(0, imgsz[0]/2):
            print i
            for j in xrange(0,imgsz[1]):
                ftheta = 0
                for angleindex in xrange(0, rimg.shape[0]):
                    rou = np.abs(np.int32(i*np.cos(angleindex * angleStep)+ j * np.sin(angleindex* angleStep)))
                    if rou < 0 or rou > rimg.shape[1]-1:
                        print (angleindex * angleStep, rou)
                        continue
                    ftheta += rimg[angleindex, rou]
                iimg[i,j]=ftheta
        maxVal = np.max(iimg)
        iimg /= maxVal
        cv2.namedWindow('iradon')
        cv2.imshow('iradon', iimg)
        cv2.waitKey(0)
        return iimg

