# jpeg compressor - CURRENTLY IN PROGRESS!

import os
import cv2 as cv
import numpy as np

def dct(k,l,matrix_a,channel_index=0):
    rows, cols, channels = matrix_a.shape
    total = 0
    for m in range(rows):
        for n in range(cols):
            total += matrix_a[m, n,channel_index] * np.cos((k*np.pi /(2*rows)) * (2*m+1)) * np.cos((l*np.pi / (2*cols)) * (2*n+1))
    total = total * (2 * np.sqrt(rows * cols))  # normalization factor
    return total

quantization_table = [[16,11,10,16,24,40,51,61],
                      [12,12,14,19,26,58,60,55],
                      [14,13,16,24,40,57,69,56],
                      [14,17,22,29,51,87,80,62],
                      [18,22,37,56,68,109,103,77],
                      [24,35,55,64,81,104,113,92],
                      [49,64,78,87,103,121,120,101],
                      [72,92,95,98,112,100,103,99]]

img = cv.imread(os.path.join('.', 'data', 'blackbuck.bmp'))

h,w,_ = img.shape

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

downsampled_img = cv.cvtColor(merged_ycrcb, cv.COLOR_YCrCb2RGB)

# seperate image into 8x8 grid
step_y = h // 8
step_x = w // 8

grid = []

for i in range(8):
    for j in range(8):
        # make the boundaries
        start_y = i * step_y
        end_y = (i + 1) * step_y if i < 7 else h
        start_x = j * step_x
        end_x = (i + 1) * step_x if i < 7 else w

        tile = img[start_y:end_y, start_x:end_x]
        tile = dct(0,0,tile)
        grid.append(tile)

        print(type(grid))

# quantization

#cv.imwrite("compressed_img.bmp", compressed_img)

#cv.imshow('img', img)
#cv.imshow('new img', compressed_img)
#cv.waitKey(0)