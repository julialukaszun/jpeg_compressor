import os
import cv2 as cv
import numpy as np

img = cv.imread(os.path.join('.', 'data', 'cat.jpg'))

# convert image from R,G,B to Y,Cb,Cr colorspace
img_ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)

# split each color channel
y,cb,cr = cv.split(img_ycrcb)

# chrominance downsampling
h, w = y.shape
half_h, half_w = h // 2, w // 2

cr_downsampled = cv.resize(cr, (half_w, half_h), interpolation=cv.INTER_AREA)
cb_downsampled = cv.resize(cb, (half_w, half_h), interpolation=cv.INTER_AREA)

cr_upscaled = cv.resize(cr, (w,h), interpolation=cv.INTER_AREA)
cb_upscaled = cv.resize(cb, (w,h), interpolation=cv.INTER_AREA)

merged_ycrcb = cv.merge([y, cr_upscaled, cb_upscaled])

compressed_img = cv.cvtColor(merged_ycrcb, cv.COLOR_YCrCb2RGB)

cv.imwrite("compressed_img.jpg", compressed_img)

cv.imshow('img', img)
cv.imshow('new img', compressed_img)
cv.waitKey(0)