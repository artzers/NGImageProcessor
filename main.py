import os,sys
import cv2
import numpy as np
import BasePixelTransfer

img=cv2.imread("lena.jpg")
baseTransfer = BasePixelTransfer.BasePixelTransfer()
#invertImg=baseTransfer.InvertImage(img)
#logImg = baseTransfer.LogImage(img, 10)
#powerImg = baseTransfer.PowerImage(img, 2.0)
eqimg = baseTransfer.HistEQ( img)
#gray = baseTransfer.RGB2Gray(img)
#eqgray = baseTransfer.HistEQ(gray)

reghist = baseTransfer.Imhist3(img, 255)
dImg, regMap = baseTransfer.RegulateHist(eqimg, reghist)

cv2.imwrite("eq.jpg",eqimg)
cv2.namedWindow("lena")
cv2.imshow("lena",img)
cv2.namedWindow("eq")
cv2.imshow("eq",eqimg)
cv2.namedWindow("reg")
cv2.imshow("reg",dImg)
cv2.waitKey(0)
