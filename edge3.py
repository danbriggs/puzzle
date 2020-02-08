#pip3 install opencv-python
import os
import sys
import time
import cv2
import random
import numpy as np
from PIL import Image
import edgestats as es
import pixelpath as pp
import find_pieces as f_p
import fillinthepieces as fp
import listofpuzzles as lofp
import findedges as fed
import color_sobel as c_s
import intersect1 as int1
import comparison as cp
from matplotlib import pyplot as plt

filename = input('Filename of image:')

img = cv2.imread(filename, 0)
print('shape of img', img.shape)
print('type of img(0,0)', type(img[0,0]))

imgcolordave = cv2.imread(filename)
RGB_img = cv2.cvtColor(imgcolordave, cv2.COLOR_BGR2RGB)

imgcolor_pre = cv2.imread(filename)
imgcolor = cv2.cvtColor(imgcolor_pre, cv2.COLOR_BGR2RGB)
imgcolor2 = cv2.cvtColor(imgcolor_pre, cv2.COLOR_BGR2RGB)
img1 = cv2.imread(filename, 0)
print('shape of image', img1.shape)
print('shape of color', imgcolor.shape)

def find_background(image0):
    """Returns a numpy matrix of booleans corresponding to whether each
    pixel is to be considered a background pixel."""
    b_c_s = es.border_color_statistics(image0)
    img1 = cv2.imread(image0)

ans =  es.border_color_statistics(filename)
print("Standard Deviation of color of sample is % s ", ans[0])
print("Mean color of sample is ", ans[1])
print("Median color of sample is ", ans[2])
print("Interquartile range of sample is ", ans[3])
img_median = ans[2]
img_iqr = ans[3]

laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
#sobelxred = cv2.Sobel(imgcolor[:,:,0],cv2.CV_64F,1,0,ksize=5)
#sobelxgreen = cv2.Sobel(imgcolor[:,:,1],cv2.CV_64F,1,0,ksize=5)
#sobelxblue = cv2.Sobel(imgcolor[:,:,2],cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
#sobelyred = cv2.Sobel(imgcolor[:,:,0],cv2.CV_64F,0,1,ksize=5)
#sobelygreen = cv2.Sobel(imgcolor[:,:,1],cv2.CV_64F,0,1,ksize=5)
#sobelyblue = cv2.Sobel(imgcolor[:,:,2],cv2.CV_64F,0,1,ksize=5)
sobel = (sobelx*sobelx + sobely*sobely)**.5
#sobelred = (sobelxred*sobelxred + sobelyred*sobelyred)**.5
#sobelgreen = (sobelxgreen*sobelxgreen + sobelygreen*sobelygreen)**.5
#sobelblue = (sobelxblue*sobelxblue + sobelyblue*sobelyblue)**.5
#sobelredd = sobelred[:,:,np.newaxis]
#sobelgreenn = sobelgreen[:,:,np.newaxis]
#sobelbluee = sobelblue[:,:,np.newaxis]
#sobelcolor = np.concatenate((sobelredd,sobelgreenn,sobelbluee),axis=2)
sobelcopy = np.copy(sobel)
sobelcopycopy = np.copy(sobel)
theta  = np.arctan(sobelx/sobely)
highs = sobel[sobel>6000]
print('shape of sobel', sobel.shape)
print('size of sobel', sobel.shape[0]*sobel.shape[1])
print('shape of highs', highs.shape)
indicators = np.multiply(sobel>6000,1)
print('shape of indicators', indicators.shape)
restricted_theta = indicators*np.pi + theta*indicators
print('shape of restricted theta', restricted_theta.shape)

print('max of sobel:', np.max(sobel))
print('min of sobel:', np.max(sobel))

def determine_if_above_cutoff(y,x, cutoff):
    if(sobel[y,x] < cutoff):
        return False
    return True
height = sobel.shape[0]
width = sobel.shape[1]
"""start0 = time.time()
ycord = [random.randint(0, height-1) for i in range(1000000)]
xcord = [random.randint(0, width-1) for i in range(1000000)]
for i in range(1000000):
    determine_if_above_cutoff(ycord[i], xcord[i], 2000)
end0 = time.time()
print("Time to determine: ", end0 - start0)"""

hasbeenchecked = np.zeros((height, width), dtype=bool)
hasbeenchecked_copy = np.copy(hasbeenchecked)


height2 = imgcolor.shape[0]
width2 = imgcolor.shape[1]

is_enough_edge = np.zeros((height2, width2), dtype=bool)
is_background = np.zeros((height2, width2), dtype=bool)

#sobelx2 = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize = 5)
#sobely2 = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize = 5)
#sobel2 = (sobelx2 * sobelx2 + sobely2 * sobely2) ** 0.5

#fp.fill_in_pieces('dave.jpg',hasbeenchecked,2000)
#for i in range(height):
#    for j in range(width):
#        if (hasbeenchecked[i,j]):
#            RGB_img[i,j]=(0,0,0)

scaled_color_sobels = c_s.make_color_sobels(filename, False)
scaled_color_sobel_y = scaled_color_sobels[0]
scaled_color_sobel_x = scaled_color_sobels[1]
scaled_color_sobel = scaled_color_sobels[2]
sum_y = np.sum(scaled_color_sobel_y,axis=2)
sum_x = np.sum(scaled_color_sobel_x,axis=2)
sum = (sum_x*sum_x + sum_y*sum_y)**.5
single_scaled_color_sobel = np.linalg.norm(scaled_color_sobel,axis=2)/1.733
"""Turns the three-channel sobel into a single number less than 1 at each pair of indices."""

fp.fill_in_pieces(filename,is_enough_edge,is_background,.1,single_scaled_color_sobel) #was .1
for i in range(height2):
    for j in range(width2):
        if (is_background[i,j]):
            #print("type(imgcolor[",i,",",j,"]): ",type(imgcolor[i,j]))
            #print("imgcolor[",i,",",j,"].shape: ",imgcolor[i,j].shape)
            imgcolor[i,j]=(0,0,0)

#fed.find_edges(hasbeenchecked_copy,filename,2000)
#print(hasbeenchecked_copy)
is_background_copy = np.copy(is_background)
list_of_pieces = lofp.list_of_puzzles(is_background_copy,imgcolor2,sobely,sobelx,sobel,scaled_color_sobel,False)
print("len(list_of_pieces): ",len(list_of_pieces))
starting_points = []
path = []
for i in range(len(list_of_pieces)):
    if (len(list_of_pieces[i])>0):
        starting_points.append(list_of_pieces[i][0])
    else:
        starting_points.append("empty")
    print("starting_points[",i,"]: ",starting_points[i])
    print("len(list_of_pieces[",i,"]): ",len(list_of_pieces[i]))
#print("list_of_pieces: ",list_of_pieces)

"""rotated_array = f_p.rotation_piece(list_of_pieces, "whole_puzzle.jpg", filename)
print(rotated_array)
compare = rotated_array[0]
for i in range(len(rotated_array)):
    if rotated_array[i] < compare:
        compare = rotated_array
cp.comparison(compare, "whole_puzzle.jpg", filename)"""

plt.subplot(2,2,1),plt.imshow(sobelcopy[:,:,],cmap = 'gray')
plt.title('Sobel Copy'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(sobel[:, :,],cmap = 'gray')
plt.title('sobel'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelcopycopy[:, :,],cmap = 'gray')
plt.title('Sobel Recurse'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(imgcolor[:, :,])
plt.title('imgcolor'), plt.xticks([]), plt.yticks([])

plt.show()
