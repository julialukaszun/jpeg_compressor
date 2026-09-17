import os
import cv2 as cv
import numpy as np

img = cv.imread(os.path.join('.', 'data', 'cat.png'))

cv.imshow('cat', img)
cv.waitKey(0)