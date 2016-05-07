import numpy as np, cv2
from matplotlib import pyplot as plt
import BasePixelTransfer

class BaseFFTProcessor:
    def __init__(self):
        pass

    def FFTDemo(self):
        img = cv2.imread("lena.jpg")
        baseTransfer = BasePixelTransfer.BasePixelTransfer()
        img = baseTransfer.RGB2Gray(img)
        fimg = img.copy()
        fimg = np.float32(fimg)
        # for i in xrange(0, img.shape[0]):
        #     for j in xrange(0, img.shape[1]):
        #         fimg[i, j] *= (-1) ** (i + j)

        fftimg = np.fft.fftshift(np.fft.fft2(fimg))
        ifft = np.real(np.fft.ifft2(fftimg))
        for i in xrange(0, ifft.shape[0]):
            for j in xrange(0, ifft.shape[1]):
                ifft[i, j] *= (-1) ** (i + j)
        cv2.namedWindow("lena")
        cv2.imshow("lena", img)
        cv2.namedWindow("fft")
        cv2.imshow("fft", np.real(fftimg))
        cv2.imshow("ifft", np.uint8(ifft))
        cv2.waitKey(0)

    def PrepareFFT(self):
        img = cv2.imread("lena.jpg")
        baseTransfer = BasePixelTransfer.BasePixelTransfer()
        img = baseTransfer.RGB2Gray(img)
        fimg = img.copy()
        fimg = np.float64(fimg)
        # for i in xrange(0, img.shape[0]):
        #     for j in xrange(0, img.shape[1]):
        #         fimg[i, j] *= (-1) ** (i + j)
        fftimg = np.fft.fft2(fimg)
        fftimg = np.fft.fftshift(fftimg)
        return fftimg

    def GetIFFT(self, fftimg):
        fftimg = np.fft.ifftshift(fftimg)
        ifft = np.real(np.fft.ifft2(fftimg))
        # for i in xrange(0, ifft.shape[0]):
        #     for j in xrange(0, ifft.shape[1]):
        #         ifft[i, j] *= (-1) ** (i + j)
        return np.uint8(ifft)


    def IdeaLowPassDemo(self, radius):
        fftimg = self.PrepareFFT()
        center = np.mat(fftimg.shape) / 2.0
        for i in xrange(0, fftimg.shape[0]):
            for j in xrange(0, fftimg.shape[1]):
                if np.linalg.norm([i,j] - center) > radius:
                    fftimg[i, j] *= 0
        ifft = self.GetIFFT(fftimg)
        cv2.namedWindow("fft")
        cv2.imshow("fft", np.real(fftimg))
        cv2.imshow("ifft", np.uint8(ifft))
        cv2.waitKey(0)


    def IdeaHighPassDemo(self, radius):
        fftimg = self.PrepareFFT()
        center = np.mat(fftimg.shape) / 2.0
        for i in xrange(0, fftimg.shape[0]):
            for j in xrange(0, fftimg.shape[1]):
                if np.linalg.norm([i,j] - center) < radius:
                    fftimg[i, j] *= 0
        ifft = self.GetIFFT(fftimg)
        cv2.namedWindow("fft")
        cv2.imshow("fft", np.real(fftimg))
        cv2.imshow("ifft", np.uint8(ifft))
        cv2.waitKey(0)

    def GLPFDemo(self, radius):
        fftimg = self.PrepareFFT()
        center = np.mat(fftimg.shape) / 2.0
        r2 = 2.0 * radius ** 2.0
        distance = 0
        for i in xrange(0, fftimg.shape[0]):
            for j in xrange(0, fftimg.shape[1]):
                distance = np.linalg.norm([i,j] - center)
                fftimg[i, j] *= np.exp(- distance ** 2.0 / (r2))
        ifft = self.GetIFFT(fftimg)
        cv2.namedWindow("fft")
        cv2.imshow("fft", np.real(fftimg))
        cv2.imshow("ifft", np.uint8(ifft))
        cv2.waitKey(0)

    def GHPFDemo(self, radius):
        fftimg = self.PrepareFFT()
        center = np.mat(fftimg.shape) / 2.0
        r2 = 2.0 * radius ** 2.0
        distance = 0
        for i in xrange(0, fftimg.shape[0]):
            for j in xrange(0, fftimg.shape[1]):
                distance = np.linalg.norm([i,j] - center)
                fftimg[i, j] *= (1 - np.exp(- distance ** 2.0 / (r2)))
        ifft = self.GetIFFT(fftimg)
        cv2.namedWindow("fft")
        cv2.imshow("fft", np.real(fftimg))
        cv2.imshow("ifft", np.uint8(ifft))
        cv2.waitKey(0)


    def LaplaceFFTDemo(self):
        origfftimg = self.PrepareFFT()
        fftimg = origfftimg.copy()
        sz = fftimg.shape
        center = np.mat(fftimg.shape) / 2.0
        for i in xrange(0, 512):
            for j in xrange(0, 512):
                #pass
                #print -(np.float64(i - center[0, 0]) ** 2.0 + np.float64(j - center[0, 1]) ** 2.0)
                fftimg[i, j] *= - 0.00001* (np.float64(i - 256) ** 2.0 + np.float64(j - 256) ** 2.0)
        ifft = self.GetIFFT(fftimg)
        #plt.imshow(np.real(fftimg))
        #plt.show()
        # cv2.namedWindow("fft1")
        # cv2.imshow("fft1", np.real(origfftimg))
        cv2.namedWindow("fft")
        cv2.imshow("fft", np.real(fftimg))
        # cv2.imshow("ifft", np.uint8(ifft))
        cv2.namedWindow("ifft")
        cv2.imshow("ifft", ifft)
        cv2.waitKey(0)

    def LaplaceFFTDemo2(self):
        fimg = self.PrepareFFT()
        kernel=[[0,-1,0],[-1,4,-1],[0,-1,0]]
        fkernel = np.zeros(fimg.shape)
        fkernel[0:3,0:3]=kernel
        fkernel = np.fft.fftshift(np.fft.fft2(fkernel))
        filterimg = fimg * fkernel
        rimg = self.GetIFFT(filterimg)
        cv2.namedWindow("laplace")
        cv2.imshow("laplace", np.uint8(rimg))
        cv2.waitKey(0)
