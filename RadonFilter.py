import os, numpy as np, cv2

class RadonFilter:
    def __init__(self):
        pass

    def RadonDemo(self):
        origimg = cv2.imread('./SheppLogan_Phantom.tif', cv2.IMREAD_UNCHANGED)
        longaxis = np.round(np.sqrt(origimg.shape[0] ** 2.0 + origimg.shape[1] ** 2.0))
        img = np.zeros((longaxis, longaxis), origimg.dtype)
        xoffset = (longaxis - origimg.shape[0]) / 2
        yoffset = (longaxis - origimg.shape[1]) / 2
        img[xoffset:xoffset + origimg.shape[0], yoffset:yoffset + origimg.shape[1]] = origimg
        angleStep = 1.0
        rimg = self.RadonFilter(img, angleStep)
        iimg = self.IRadonFilter(rimg, origimg.shape, img.shape, angleStep)
        #cv2.namedWindow('orig')
        #cv2.imshow('orig', img)
        #cv2.waitKey(0)

    def RadonFilter(self, img, angleStep):
        # img -= 128
        angleNum = np.int32(180.0 / angleStep)
        rotateImg = np.zeros(img.shape, np.int32)
        radonImg = np.zeros((img.shape[0], angleNum), np.int32)
        for i in xrange(1, angleNum + 1):
            angle = np.float(i) * angleStep
            M = cv2.getRotationMatrix2D((img.shape[0] / 2, img.shape[1] / 2), angle, 1.0)
            rotateImg = cv2.warpAffine(img, M, img.shape)
            radonImg[:, i - 1] = np.sum(rotateImg, axis=0)
        # cv2.namedWindow('radon')
        # cv2.imshow('radon', radonImg)
        # cv2.waitKey(0)
        return radonImg

    def IRadonFilter(self, rimg, origImgSZ, imgSZ, angleStep):
        iimg = np.zeros(imgSZ, np.float)
        longaxis = imgSZ
        xoffset = (longaxis[0] - origImgSZ[0]) / 2
        yoffset = (longaxis[1] - origImgSZ[1]) / 2
        center = [imgSZ[0] / 2, imgSZ[1] / 2]
        for angleindex in xrange(1, rimg.shape[1] + 1, 5):
            print "angle:", angleindex
            theta = angleindex * angleStep / 180.0 * np.pi
            calCos = np.cos(theta)
            calSin = np.sin(theta)
            for i in xrange(xoffset, imgSZ[0] - xoffset):
                for j in xrange(yoffset, imgSZ[1] - yoffset):
                    rou = np.int32((i - center[0]) * calCos + (j - center[1]) * calSin) + rimg.shape[0] / 2
                    if rou < 0 or rou > rimg.shape[0] - 1:
                        print (i, j, np.cos(theta), np.sin(theta), rou)
                        continue
                    ftheta = rimg[rou, angleindex - 1]
                    iimg[j, i] += ftheta
        maxVal = np.max(iimg)
        iimg /= maxVal
        cv2.namedWindow('iradon')
        cv2.imshow('iradon', iimg)
        cv2.waitKey(0)
        return iimg

