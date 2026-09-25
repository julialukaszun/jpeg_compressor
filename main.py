# jpeg compressor - CURRENTLY IN PROGRESS!

import os
import cv2 as cv
import numpy as np

# normalization factor
def alpha(u, N):
    return np.sqrt(1/N) if u == 0 else np.sqrt(2/N)

def dct(k, l, matrix_a, channel_index=0):
    rows, cols, channels = matrix_a.shape
    total = 0
    for m in range(rows):
        for n in range(cols):
            total += (matrix_a[m, n, channel_index] *
                      np.cos((k * np.pi / (2*rows)) * (2*m + 1)) *
                      np.cos((l * np.pi / (2*cols)) * (2*n + 1)))
    total = total * alpha(k, rows) * alpha(l, cols)
    return total

def inv_dct(m, n, matrix_a, channel_index=0):
    rows, cols = matrix_a.shape
    total = 0
    for k in range(rows):
        for l in range(cols):
            total += (alpha(k, rows) * alpha(l, cols) *
                      matrix_a[k, l] *
                      np.cos((2*m + 1) * k * np.pi / (2*rows)) *
                      np.cos((2*n + 1) * l * np.pi / (2*cols)))
    return total

def rebuild_channel(grid):
    channel = np.zeros((H, W), dtype=np.float64)
    idx = 0
    for i in range(0, H, 8):
        for j in range(0, W, 8):
            block = np.array(grid[idx])
            channel[i:i + 8, j:j + 8] = block
            idx += 1
    return channel

Q_TABLE = [[16,11,10,16,24,40,51,61],
                      [12,12,14,19,26,58,60,55],
                      [14,13,16,24,40,57,69,56],
                      [14,17,22,29,51,87,80,62],
                      [18,22,37,56,68,109,103,77],
                      [24,35,55,64,81,104,113,92],
                      [49,64,78,87,103,121,120,101],
                      [72,92,95,98,112,100,103,99]]

img = cv.imread(os.path.join('.', 'data', 'img.png'))

h,w,_ = img.shape

# convert image from R,G,B to Y,Cb,Cr colorspace
img_ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)

# split each color channel
y,cr,cb = cv.split(img_ycrcb)

# chrominance downsampling
h, w = y.shape
half_h, half_w = h // 2, w // 2
H, W = h - h % 8, w - w % 8
Q = np.array(Q_TABLE)

cr_downsampled = cv.resize(cr, (half_w, half_h), interpolation=cv.INTER_AREA)
cb_downsampled = cv.resize(cb, (half_w, half_h), interpolation=cv.INTER_AREA)

cr_upscaled = cv.resize(cr_downsampled, (w,h), interpolation=cv.INTER_AREA)
cb_upscaled = cv.resize(cb_downsampled, (w,h), interpolation=cv.INTER_AREA)

downsampled_img = cv.merge([y, cr_upscaled, cb_upscaled])

# seperate image into 8x8 grid
step_y = h // 8
step_x = w // 8

grid_y = []
grid_cb = []
grid_cr = []

# channel y
for i in range(0, h - h % 8, 8):
    for j in range(0, w - w % 8, 8):
        tile = downsampled_img[i:i+8, j:j+8]
        dct_tile = np.zeros((8, 8))
        for k in range(8):
            for l in range(8):
                dct_tile[k, l] = dct(k, l, tile)  # channel_index=0
        quantized_tile = np.round(dct_tile / Q_TABLE).astype(int)
        grid_y.append(quantized_tile)

for i in range(len(grid_y)):
    block = grid_y[i]
    dequantized = block * np.array(Q_TABLE)
    new_block = [[0]*8 for _ in range(8)]
    for k in range(8):
        for j in range(8):
            new_block[k][j] = inv_dct(k, j, dequantized)
    grid_y[i] = new_block

# channel cr
for i in range(0, h - h % 8, 8):
    for j in range(0, w - w % 8, 8):
        tile = downsampled_img[i:i+8, j:j+8]
        dct_tile = np.zeros((8, 8))
        for k in range(8):
            for l in range(8):
                dct_tile[k, l] = dct(k, l, tile,1)
        quantized_tile = np.round(dct_tile / Q_TABLE).astype(int)
        grid_cr.append(quantized_tile)

for i in range(len(grid_cr)):
    block = grid_cr[i]
    dequantized = block * np.array(Q_TABLE)
    new_block = [[0]*8 for _ in range(8)]
    for k in range(8):
        for j in range(8):
            new_block[k][j] = inv_dct(k, j, dequantized)
    grid_cr[i] = new_block

# channel cb
for i in range(0, h - h % 8, 8):
    for j in range(0, w - w % 8, 8):
        tile = downsampled_img[i:i+8, j:j+8]
        dct_tile = np.zeros((8, 8))
        for k in range(8):
            for l in range(8):
                dct_tile[k, l] = dct(k, l, tile,2)
        quantized_tile = np.round(dct_tile / Q_TABLE).astype(int)
        grid_cb.append(quantized_tile)

for i in range(len(grid_cb)):
    block = grid_cb[i]
    dequantized = block * np.array(Q_TABLE)
    new_block = [[0]*8 for _ in range(8)]
    for k in range(8):
        for j in range(8):
            new_block[k][j] = inv_dct(k, j, dequantized)
    grid_cb[i] = new_block

y_out  = rebuild_channel(grid_y)
cb_out = rebuild_channel(grid_cb)
cr_out = rebuild_channel(grid_cr)

reconstructed_ycrcb = cv.merge([
    np.clip(y_out, 0, 255).astype(np.uint8),
    np.clip(cr_out, 0, 255).astype(np.uint8),
    np.clip(cb_out, 0, 255).astype(np.uint8),
])

reconstructed_bgr = cv.cvtColor(reconstructed_ycrcb, cv.COLOR_YCrCb2BGR)
cv.imwrite('reconstructed.png', reconstructed_bgr)