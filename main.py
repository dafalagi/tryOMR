import cv2
import numpy as np
from PIL import Image
from utils import Utils as utils

path = "4.jpeg"
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
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 10)

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
    # imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    # imgCropped = cv2.resize(imgCropped, (width, height))

    imgWarpedGray = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2GRAY)
    imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpedGray, 255, 1, 1, 7, 2)
    imgThre = cv2.threshold(imgWarpedGray, 150, 255, cv2.THRESH_BINARY_INV)[1]
    # imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
    # imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)

    # imgArray = ([img, imgGray, imgBlur, imgCanny],
    #             [imgContour, imgOutput, imgWarpedGray, imgAdaptiveThre])

imgBlank = np.zeros_like(img)
imgArray = ([img, imgGray, imgBlur, imgCanny],
            [imgContour, imgBiggestContour, imgOutput, imgThre])
imgStack = utils.stackImages(imgArray, 0.5)

cv2.imshow('Images', imgStack)
cv2.waitKey(0)