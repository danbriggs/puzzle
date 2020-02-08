from PIL import Image, ImageChops
from fractions import Fraction
import time

#1
im1 = Image.open('whole_puzzle.jpg')
im2 = Image.open('piece_puzzle.jpg')
width, height = im2.size
width1, height1 = im1.size
back_im = im1.copy()
compared = []

def root(m):
    # Get initial approximation
    n, a, k = m, 1, 0
    while n > a:
        n >>= 1
        a <<= 1
        k += 1
        #print k, ':', n, a

    # Go back one step & average
    a = n + (a>>2)
    #print a

    # Apply Newton's method
    while k:
        a = (a + m // a) >> 1
        k >>= 1
        #print k, ':', a
    return a

def compare(file1, file2):
    diff = ImageChops.difference(file1, file2)
    h = diff.histogram()
    sq = (value**(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    size = file1.size[0] * file1.size[1]
    rms = Fraction(sum_of_squares, size)
    return rms

for i in range(width1):
    for j in range(height1):
        for k in range(360):
            im2 = im2.rotate(k) #3
            back_im.paste(im2, (i, j)) #2
            start = time.time()
            compared = [compare(im1, im2), i, j, k] #4
            end = time.time()
            print(end -start)

holder = compared[0][0]
pivot = 0
#5
for m in range(len(compared)):
    if compared[m][0] < holder:
        holder = compared[m][0]
        pivot = compared[m]
#6
im2 = im2.rotate(pivot[3])
back_im.paste(im2, (pivot[1], pivot[2]))
back_im.show()
