import cv2, numpy as np
import ImageNoiseGenerator

class BaseImageRestore:
    def __init__(self):
        self.noiseGenerator = ImageNoiseGenerator.ImageNoiseGenerator()


    def GenerateHDemo(self, sz):
        u = sz[0]
        v = sz[1]
        H = np.zeros(sz, np.float64)
        k=0.0025
        for i in xrange(0, u):
            for j in xrange(0, v):
                H[i, j] = np.exp(-k * ( (i-u/2.0) ** 2.0 + (j-v/2.0) ** 2.0 ) ** (5.0/6.0))
        return H

    def IdeaLowHInverse(self, H, radius):
        [u,v] = H.shape
        for i in xrange(0, u):
            for j in xrange(0, v):
                if np.sqrt((i-u/2.0) ** 2.0 + (j - v / 2.0) ** 2.0) > radius or H[i, j] < 1e-5:
                    H[i, j] = 0
                else:
                    H[i, j] =  1.0 / H[i, j]
        return H

    def InverseFilterDemo(self, img):
        #img = np.uint8(np.random.random((100, 100)) * 255)
        H = self.GenerateHDemo(img.shape)
        #H = np.float64(H)
        fImg = np.fft.fftshift(np.fft.fft2(img))
        gImg = np.fft.ifft2(np.fft.ifftshift(fImg*H))#(fImg.dot(H))
        fgImg = np.fft.fftshift(np.fft.fft2(gImg))
        H1 = self.IdeaLowHInverse(H, 500)
        ggImg = np.fft.ifft2(np.fft.ifftshift(fgImg*H1))
        cv2.namedWindow("g")
        cv2.imshow("g", np.uint8(gImg))
        cv2.namedWindow("inverse filter restore")
        cv2.imshow("inverse filter restore", np.uint8(ggImg))
        cv2.waitKey(0)


