import os,sys
import cv2
import numpy as np
import BasePixelTransfer
import BaseSpatialFilter
import BaseFFTProcessor

# baseTransfer = BasePixelTransfer.BasePixelTransfer()
# img = cv2.imread("lena.jpg")
# #baseTransfer.HistDemo()
# img = baseTransfer.RGB2Gray(img)
# baseSpacer = BaseSpatialFilter.BaseSpatialFilter()
# baseSpacer.LaplacianDemo(img)
#baseSpacer.LoGDemo(img, 5, 1)
#baseSpacer.DoGDemo(img, 5, 0.3, 0.4)
#baseSpacer.DoGCornerDetectDemo(img, 5, (0.3, 0.4, 0.6, 0.7, 0.7, 0.8), 2)

ffter = BaseFFTProcessor.BaseFFTProcessor()
#ffter.FFTDemo()
# ffter.IdeaLowPassDemo(50)
#ffter.IdeaHighPassDemo(50)
#ffter.GLPFDemo(50)
# ffter.GHPFDemo(50)
ffter.LaplaceFFTDemo()