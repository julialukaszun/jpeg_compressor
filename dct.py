# this is to test the dct algorithm!
import numpy as np

matrix_a = np.arange(1, 65).reshape(8, 8)
print(matrix_a)

m = 6.0
n = 2.0
k = 0 # frequency
l = 0 # frequency
Mt = 8.0
Nt = 8.0

def dct(m,n,k,l,Mt,Nt):
    return np.cos((k*np.pi/(2*Mt)) * (2*m+1)) * np.cos((l*np.pi/(2*Nt)) * (2*n+1))

def dctx(k,l,Mt,Nt,matrix_a):
    rows, cols = matrix_a.shape
    total = 0
    for m in range(rows):
        for n in range(cols):
            total += matrix_a[m, n] * np.cos((k*np.pi /(2*Mt)) * (2*m+1)) * np.cos((l*np.pi / (2*Nt)) * (2*n+1))
            total = total * (2 * np.sqrt(Mt * Nt)) # normalization factor
    return total

print(dctx(k,l,Mt,Nt,matrix_a))