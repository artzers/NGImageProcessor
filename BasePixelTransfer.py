import numpy as np
import cv2


class BasePixelTransfer:

    def __init__(self):
        pass

    def _NumericMax(self, type):
        if type == np.uint8:
            return 255
        if type == np.uint16:
            return 65535

    def RGB2Gray(self, img):
        dImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return dImg

    def InvertImage(self, img):
        if img.dtype == np.uint8:
            invertImg = 255 - img
        if img.dtype == np.uint16:
            invertImg = 65535 - img
        return invertImg


    def LogImage(self, img, logNum):
        dImg = np.float32(img)
        dImg = np.log(1.0+dImg) / np.log(logNum)
        dImg = np.uint8(dImg / np.max(dImg) * 255)
        return dImg

    def PowerImage(self, img, powerNum):
        dImg = np.float32(img)
        dImg = np.power(img, powerNum)
        dImg = np.uint8(dImg / np.max(dImg) * 255)
        return dImg

    def Imhist(self, img, limitPixel):
        dimension = len(img.shape)
        if dimension == 2:
            hist = self.Imhist2(img, limitPixel)
        if dimension == 3:
            hist = self.Imhist3(img, limitPixel)
        return  hist

    def Imhist2(self, img, limitPixel):
        hist = np.zeros((1, limitPixel + 1), np.uint32)
        for i in xrange(0, img.shape[0]):
            for j in xrange(0, img.shape[1]):
                hist[0, img[i,j]] = hist[0, img[i, j]] + 1
        return hist

    def Imhist3(self, img, limitPixel):
        hist = np.zeros((3, limitPixel + 1), np.uint32)
        hist[0, :] = self.Imhist2(img[:, :, 0], limitPixel)
        hist[1, :] = self.Imhist2(img[:, :, 1], limitPixel)
        hist[2, :] = self.Imhist2(img[:, :, 2], limitPixel)
        return hist

    def HistEQ(self, img):
        dImg = np.zeros(img.shape,img.dtype)
        dimension = len(img.shape)
        if dimension == 2:
            hist = self.Imhist2(img, self._NumericMax(img.dtype))
            eqmap = self.GetHistEQMap(hist)
            for i in xrange(0,img.shape[0]):
                for j in xrange(0,img.shape[1]):
                    dImg[i,j] = eqmap[img[i,j]]
        if dimension == 3:
            hist = self.Imhist3(img, self._NumericMax(img.dtype))
            eqmap = np.zeros(hist.shape, hist.dtype)
            eqmap[0,:] = self.GetHistEQMap(hist[0,:])
            eqmap[1,:] = self.GetHistEQMap(hist[1,:])
            eqmap[2,:] = self.GetHistEQMap(hist[2,:])
            for i in xrange(0,img.shape[0]):
                for j in xrange(0,img.shape[1]):
                    for ij in xrange(0,img.shape[2]):
                        dImg[i,j,ij] = eqmap[ij,img[i,j,ij]]
        return dImg

    def GetHistEQMap(self, hist):
        hist=np.float32(hist)
        sum = np.float32(np.sum(hist))
        eqmap=np.uint8(np.cumsum(hist) / sum * 255)
        return eqmap

    def RegulateHist(self, img, dstRegHist):
        dImg = np.zeros(img.shape, img.dtype)
        dimension = len(img.shape)
        regMap = np.zeros(dstRegHist.shape, dstRegHist.dtype)
        if dimension == 2:
            hist = self.Imhist2(img, self._NumericMax(img.dtype))
            eqmap = self.GetHistEQMap(hist)
            regMap = self.GetHistEQMap(dstRegHist)
            revMap = self.ReverseHistMap(regMap)
            dstMap = self.Integrate2Hist(eqmap, revMap)
            for i in xrange(0,img.shape[0]):
                for j in xrange(0,img.shape[1]):
                    dImg[i,j] = dstMap[img[i,j]]
        if dimension == 3:
            hist = self.Imhist3(img, self._NumericMax(img.dtype))
            eqmap = np.zeros(hist.shape, hist.dtype)
            eqmap[0, :] = self.GetHistEQMap(hist[0, :])
            eqmap[1, :] = self.GetHistEQMap(hist[1, :])
            eqmap[2, :] = self.GetHistEQMap(hist[2, :])
            regMap[0, :] = self.GetHistEQMap(dstRegHist[0, :])
            regMap[1, :] = self.GetHistEQMap(dstRegHist[1, :])
            regMap[2, :] = self.GetHistEQMap(dstRegHist[2, :])
            revMap = self._ReverseHistMap(regMap)
            dstMap = self._Integrate2Hist(eqmap, revMap)
            for i in xrange(0, img.shape[0]):
                for j in xrange(0, img.shape[1]):
                    for ij in xrange(0, img.shape[2]):
                        dImg[i, j, ij] = dstMap[ij, img[i, j, ij]]
        return dImg, dstMap

    def _ReverseHistMap(self, hist):
        reverseMap = np.zeros(hist.shape, hist.dtype)
        for x in xrange(0, hist.shape[0]):
            for y in xrange(0, hist.shape[1]):
                reverseMap[x, hist[x, y]] = y
        return reverseMap

    def _Integrate2Hist(self, hist1, hist2):
        dstHist = np.zeros(hist1.shape, hist1.dtype)
        for x in xrange(0, hist1.shape[0]):
            for y in xrange(0, hist1.shape[1]):
                dstHist[x,y] = hist2[x, hist1[x, y]]
        return dstHist