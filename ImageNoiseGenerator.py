import numpy as np, cv2
from matplotlib import pyplot as plt

class ImageNoiseGenerator:
    def __init__(self):
        pass

    def GuassNoise(self, img, miu, theta, noiseNum):
        sz = img.shape
        noiseImg = np.zeros(sz, np.int16)
        pdf = self.GuassianPDF(miu, theta)
        for i in xrange(0, noiseNum):
            x = np.random.random() * (sz[0] - 1)
            y = np.random.random() * (sz[1] - 1)
            noise = self.PDFMap(pdf, np.random.random())
            noiseImg[x, y] = noise
        return noiseImg

    def GuassNoiseDemo(self, img, miu, theta, noiseNum):
        sz = img.shape
        noiseImg = self.GuassNoise(img, miu, theta, noiseNum)
        gImg = img + noiseImg
        #pdf = self.GuassianPDF(miu, theta)
        # for i in xrange(0, noiseNum):
        #     x = np.random.random() * (sz[0] - 1)
        #     y = np.random.random() * (sz[1] - 1)
        #     noise = self.PDFMap(pdf, np.random.random())
        #     print noise
        #     noiseImg[x, y] = noiseImg[x, y] + noise
        cv2.namedWindow("lena")
        cv2.namedWindow("gauss noise")
        cv2.namedWindow("dst")
        cv2.imshow("lena", img)
        cv2.imshow("gauss noise", np.uint8(noiseImg))
        cv2.imshow("dst", np.uint8(gImg))
        cv2.waitKey(0)


    def GuassianPDF(self, miu = 0, theta = 5):
        dataX=[]
        dataY=[]
        pdf = [0]
        for i in xrange(-256, 256):
            x = i
            y = 1.0 / (np.sqrt(2.0 * np.pi) * theta) * np.exp(-(x-miu) ** 2.0/ (2.0 * theta ** 2.0))
            dataX.append(x)
            dataY.append(y)
            pdf.append(pdf[-1]+y)
        return pdf

    def PDFMap(self, pdf, val):
        for i in xrange(0, len(pdf) - 1):
            if pdf[i] < val and pdf[i+1] > val:
                return i - len(pdf) / 2
        return 0


