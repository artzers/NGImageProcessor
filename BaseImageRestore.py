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

    def WienerFilterDemo(self, img):
        img = np.int16(img)
        noise = self.noiseGenerator.GuassNoise(img, 0, 10, np.int32(img.size*0.2))
        nImg = img + noise
        fn = np.fft.fftshift(np.fft.fft2(noise))
        Sn = np.abs(fn) ** 2.0
        ffImg = np.fft.fftshift(np.fft.fft2(img))
        Sf = np.abs(ffImg) ** 2.0
        H = self.GenerateHDemo(img.shape)
        fImg = np.fft.fftshift(np.fft.fft2(img))
        gImg = np.fft.ifft2(np.fft.ifftshift(fImg * H))
        gImg += noise
        fgImg = np.fft.fftshift(np.fft.fft2(gImg))
        wH = (H * (np.abs(H) ** 2.0 + Sn / Sf)) / np.abs(H) ** 2.0
        H1 = self.IdeaLowHInverse(wH, 500)
        ggImg = np.fft.ifft2(np.fft.ifftshift(fgImg * H1))
        cv2.namedWindow("orig")
        cv2.imshow("orig", np.uint8(img))
        cv2.namedWindow("g")
        cv2.imshow("g", np.uint8(gImg))
        cv2.namedWindow("inverse filter restore")
        cv2.imshow("inverse filter restore", np.uint8(ggImg))
        cv2.waitKey(0)

    def CLQFilterDemo(self, img):
        # Constrained least square filter
        img = np.int16(img)
        noise = self.noiseGenerator.GuassNoise(img, 0, 10, np.int32(img.size))
        nImg = img + noise
        H = self.GenerateHDemo(img.shape)
        fImg = np.fft.fftshift(np.fft.fft2(img))
        gImg = np.fft.ifft2(np.fft.ifftshift(fImg * H))
        gImg += noise
        fgImg = np.fft.fftshift(np.fft.fft2(gImg))
        gamma = 0.1
        l = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        p = np.zeros(img.shape)
        p[0:3, 0:3] = l
        P = np.fft.fftshift(np.fft.fft2(p))
        N = 512 * 512 * (np.std(noise) ** 2.0 - np.mean(noise) ** 2.0)
        a = 0.25
        ggImg = self.CLSFilterOptimal(fgImg, gamma, H, P, N, a)
        #ggImg = self.CLSFilter(fgImg, gamma, H, P)
        cv2.namedWindow("orig")
        cv2.imshow("orig", np.uint8(img))
        cv2.namedWindow("g")
        cv2.imshow("g", np.uint8(gImg))
        cv2.namedWindow("CLQ filter restore")
        cv2.imshow("CLQ filter restore", np.uint8(ggImg))
        cv2.waitKey(0)

    def CLSFilter(self, fgImg, gamma, H, P):
        wH = (np.abs(H) ** 2.0 + gamma * np.abs(P) ** 2.0) / H.conj()
        H1 = self.IdeaLowHInverse(wH, 1000)
        ggImg = np.fft.ifft2(np.fft.ifftshift(fgImg * H1))
        return ggImg

    def CLSFilterOptimal(self, fgImg, gamma, H, P,  N, a):
        r = 0
        diff = 1e-6
        H1=np.zeros((1,1))
        while np.abs(r - N) > a:
            print "gamma:",gamma
            wH = (np.abs(H) ** 2.0 + gamma * np.abs(P) ** 2.0) / H.conj()
            H1 = self.IdeaLowHInverse(wH, 1000)
            F = fgImg * H1
            R = fgImg - H * F
            r = np.sum(np.abs((np.fft.ifft2(np.fft.ifftshift(R)))) ** 2.0)
            print "r-n:",r-N
            if r - N < -a:
                gamma -= diff * (r - N)
            elif r - N > a:
                gamma += diff * (r - N)
            else:
                break
        ggImg = np.fft.ifft2(np.fft.ifftshift(fgImg * H1))
        return ggImg

