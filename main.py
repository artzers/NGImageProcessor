import os,sys
import cv2
import numpy as np
import BasePixelTransfer
import BaseSpatialFilter

baseTransfer = BasePixelTransfer.BasePixelTransfer()
#baseTransfer.HistDemo()
img = cv2.imread("lena.jpg")
img = baseTransfer.RGB2Gray(img)
baseSpacer = BaseSpatialFilter.BaseSpatialFilter()
#baseSpacer.LaplacianDemo(img)
#baseSpacer.LoGDemo(img, 5, 1)
#baseSpacer.DoGDemo(img, 5, 0.3, 0.4)
baseSpacer.DoGCornerDetectDemo(img, 5, (0.3, 0.4, 0.4, 0.5, 0.5, 0.6), 5)
