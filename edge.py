# pip install opencv-python

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('dave.jpg',0)

laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
sobel = (sobelx*sobelx+sobely*sobely)**.5
sobelcopy = np.copy(sobel)
theta = np.arctan(sobelx/sobely)
highs = sobel[sobel>6000]
print(np.multiply(False,1))
print('shape of sobel',sobel.shape)
print('size of sobel',sobel.shape[0]*sobel.shape[1])
print('shape of highs',highs.shape)
indicators=np.multiply(sobel>6000,1)
print('shape of indicators',indicators.shape)
restricted_theta = indicators*np.pi+theta*indicators
print('shape of restricted theta',restricted_theta.shape)

print('max of sobel:',np.max(sobel))
print('min of sobel:',np.min(sobel))

def pixel_path(y,x,cutoff):
    #Takes the y and x coordinates of a pixel in the image
    #If the sobel at that location is less than cutoff, return []
    #Otherwise, return a sequence of pixel positions drawing a path following
    #the edge.
    #NOTE: important to stop when you come back somewhere "near enough"
    #Use theta and sobel
    if (sobel[y,x]<cutoff):
        return []
    ycoord=y
    xcoord=x
    returnlist=[]
    for i in range(2000):
        yint=int(round(ycoord))
        xint=int(round(xcoord))
        ypart=sobely[yint,xint]
        xpart=sobelx[yint,xint]
        size =sobel[yint,xint]
        ycoord=ycoord-xpart/size
        xcoord=xcoord+ypart/size
        sobelcopy[yint,xint]=0
        returnlist.append([ycoord,xcoord,sobel[yint,xint]])
        if (i>10):
            if ((ycoord-y)*(ycoord-y)+(xcoord-x)*(xcoord-x)<25):
                break
    return returnlist

print('pixel_path 1:',pixel_path(42,36,2000))
print('pixel_path 2:',pixel_path(54,32,2000))

plt.subplot(2,2,1),plt.imshow(sobelcopy[:100,:100],cmap = 'gray')
plt.title('Sobel Copy'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(sobel[:100,:100],cmap = 'gray')
plt.title('Sobel'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx[:100,:100],cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely[:100,:100],cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()


