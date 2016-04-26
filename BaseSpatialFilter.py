import cv2
import numpy as np
from matplotlib import pyplot as plt
import BasePixelTransfer

class BaseSpatialFilter:
    def __init__(self):
        pass

    def Mean(self, img, size):
        kernel = np.ones((size, size), np.int32)
        dImg = cv2.filter2D(img, -1, kernel)
        return dImg

    def Median(self, img, size):
        dImg = cv2.medianBlur(img, size)
        return dImg

    def GenerateGaussian(self, size, sigma, flag=True):
        kernel = np.zeros((size, size), np.float64)
        radius = (size - 1) / 2
        for x in xrange(-radius, radius + 1):
            for y in xrange(-radius, radius + 1):
                kernel[x + radius, y + radius] = \
                    np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2)) / (2 * np.pi * sigma ** 2)
        if flag == True:
            beishu = np.sum(kernel)
            kernel /= beishu
        return kernel


    def Gaussian(self, img, size, sigma):
        kernel = self.GenerateGaussian(size, sigma)
        dImg = cv2.filter2D(img, -1, kernel)
        return dImg

    def SobelDemo(self, img):
        dImg = self.Sobel(img)
        cv2.namedWindow("lena")
        cv2.imshow("lena", img)
        cv2.namedWindow("sobel")
        cv2.imshow("sobel", dImg)
        cv2.waitKey(0)


    def Sobel(self, img):
        karr = np.array([-1, -2 , -1, 0, 0, 0, 1, 2, 1])
        kernel1 = karr.reshape(3,3)
        kernel2 = kernel1.transpose()
        img1 = cv2.filter2D(img, -1, kernel1)
        img2 = cv2.filter2D(img, -1, kernel2)
        dImg = img1 + img2
        return dImg

    def LaplacianDemo(self, img):
        dImg = self.Laplacian(img)
        cv2.namedWindow("lena")
        cv2.imshow("lena", img)
        cv2.namedWindow("laplace")
        cv2.imshow("laplace", dImg)
        cv2.waitKey(0)

    def Laplacian(self,img):
        karr = np.array([0, 1, 0, 1, -4, 1, 0, 1, 0])
        kernel1 = karr.reshape(3, 3)
        kernel2 = kernel1.transpose()
        img1 = cv2.filter2D(img, -1, kernel1)
        img2 = cv2.filter2D(img, -1, kernel2)
        dImg = img1 + img2
        return dImg

    def LoGDemo(self, img, size, sigma):
        dImg = self.LoG(img, size, sigma)
        cv2.namedWindow("lena")
        cv2.imshow("lena", img)
        cv2.namedWindow("LoG")
        cv2.imshow("LoG", dImg)
        cv2.waitKey(0)

    def GenerateLoG(self, size, sigma):
        kernel = np.zeros((size, size), np.float64)
        radius = (size - 1) / 2
        for x in xrange(-radius, radius + 1):
            for y in xrange(-radius, radius + 1):
                kernel[x + radius, y + radius] = \
                    np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2)) * (x ** 2 + y ** 2 - 2 * sigma ** 2) \
                    / (sigma ** 4) #2 ** (size - 2)
        beishu = 1.0 / np.sum(kernel)
        kernel = beishu * kernel
        kernel[radius, radius] -= 1
        return beishu * kernel

    def LoG(self, img, size, sigma):
        kernel = self.GenerateLoG(size, sigma)
        dImg = cv2.filter2D(img, -1, kernel)
        return dImg

    def DoGDemo(self, img, size, sigma1, sigma2):
        dImg = self.DoG(img, size, sigma1, sigma2)
        cv2.namedWindow("lena")
        cv2.imshow("lena", img)
        cv2.namedWindow("DoG")
        cv2.imshow("DoG", dImg)
        cv2.waitKey(0)


    def DoG(self, img, size, sigma1, sigma2):
        img = np.float64(img)
        if sigma1 == 0:
            img1 = img
        else:
            kernel1 = self.GenerateGaussian(5, sigma1, True)
            img1 = cv2.filter2D(img, -1, kernel1)
        if sigma2 == 0:
            img2 = img
        else:
            kernel2 = self.GenerateGaussian(5, sigma2, True)
            img2 = cv2.filter2D(img, -1, kernel2)
        dImg = img1 - img2
        return dImg

    def DoGCornerDetectDemo(self, img, size, sigmaList, threv):
        dImg = self.DoGCornerDetect(img, size, sigmaList, threv)
        cv2.namedWindow("lena")
        cv2.imshow("lena", img)
        cv2.namedWindow("Corner")
        cv2.imshow("Corner", dImg)
        cv2.waitKey(0)

    def DoGCornerDetect(self, img, size, sigmaList, threv):
        if len(sigmaList) != 6:
            return
        dImg = img.copy() / 2
        radius = 1
        zRadius = 1
        dogImg = np.zeros((img.shape[0], img.shape[1], len(sigmaList) / 2), np.float64)
        for i in xrange(0, len(sigmaList) / 2 ):
            dogImg[:, :, i] = self.DoG(img, size, sigmaList[i * 2], sigmaList[i * 2 + 1])
        for x in xrange(radius, dogImg.shape[0] - radius):
            for y in xrange(radius, dogImg.shape[1] - radius):
                if dogImg[x,y,zRadius] >= np.max(dogImg[x-radius:x+radius+1, y-radius:y+radius+1, [0,2]]) or \
                    dogImg[x, y, zRadius] <= np.min(dogImg[x - radius:x + radius + 1, y - radius:y + radius + 1, \
                                                [0, 2]]):
                    if threv < dogImg[x, y, zRadius] or dogImg[x, y, zRadius] < -threv:
                        dImg[x, y] = 255
        return dImg


