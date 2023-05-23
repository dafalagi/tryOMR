import cv2
import numpy as np
from utils import Utils as utils

path = "sample/majalaya-2.jpeg"
width = 700
height = 700

img = cv2.imread(path)

# Preprocessing
img = cv2.resize(img, (width, height))
imgContour = img.copy()
imgBiggestContour = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

# Find Contours
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 5)

# Find Biggest Contour
rectCont = utils.rectContour(contours)
biggestContour = utils.getCornerPoints(rectCont[0])

# print(biggestContour)
if biggestContour.size != 0:
    cv2.drawContours(imgBiggestContour, biggestContour, -1, (0, 255, 0), 20)

    biggestContour = utils.reorder(biggestContour)

    pts1 = np.float32(biggestContour)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))
    
    imgWarpedGray = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2GRAY)

    # imgThre = cv2.adaptiveThreshold(imgWarpedGray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,2) #25 untuk tegak
    imgThre = cv2.adaptiveThreshold(imgWarpedGray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,25,2) #47 untuk tegak

    # blur = cv2.GaussianBlur(imgWarpedGray,(5,5),0)
    # imgThre = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # imgThre = cv2.threshold(imgWarpedGray, 150, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow('Images', imgThre)

imgBlank = np.zeros_like(img)
imgArray = ([img, imgGray, imgBlur, imgCanny],
            [imgContour, imgBiggestContour, imgOutput, imgThre])
imgStack = utils.stackImages(imgArray, 0.5)

# cv2.imshow('Images', imgStack)
cv2.waitKey(0)