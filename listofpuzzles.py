import pixelpath as pp
import cv2
import numpy as np
import color_sobel as c_s
from matplotlib import pyplot as plt

def list_of_puzzles(list, img, sobely,sobelx,sobel,scaled_color_sobel,loud):
    """
    list should be a 2D numpy array of type bool
    consisting of trues wherever it is background or the outer 1-pixel boundary of an edge.
    Returns a list of lists of pixels corresponding to the edges
    of all suspected puzzles pieces.
    loud determines whether to make more output
    """
    #sobel_counter = c_s.make_color_sobels(filename, False)
    #sobel_counter_reg = sobel_counter[2]
    puzzle_list = []
    pathx = []
    pathy = []
    #img = cv2.imread(filename, 0)
    #obelx = cv2.Sobel(img, cv2.CV_64F, 1,0,ksize = 5)
    #sobely = cv2.Sobel(img,cv2.CV_64F, 0,1, ksize = 5)
    #sobel = (sobelx * sobelx + sobely * sobely) ** 0.5
    sobelcopy = np.copy(sobel)
    height = sobel.shape[0]
    width = sobel.shape[1]
    counter = 0
    print('scaled_color_sobel', scaled_color_sobel[0][1])
    for i in range (height):
        for j in range (width):
            if(np.any(scaled_color_sobel[i][j] > [0.3, 0.3, 0.3])):
                if(list[i,j]):
                    counter += 1
                    if(counter%100==0):
                        print("Counter is ", counter, " and (i, j) = (", i, ", ", j, ")")
                    path = pp.pixel_path_recurse(i,j,i,j,.01,0,False,0,sobely,sobelx,sobel,sobelcopy, height, width)
                    #.01?
                    length = len(path)
                    if (length < 100 or length>890):
                        continue
                    if (loud):
                        imgcopy=np.copy(img)
                        for triple in path:
                            yc = int(round(triple[0]))
                            xc = int(round(triple[1]))
                            if (xc<0 or xc>=width or yc<0 or yc>=height):
                                continue
                            imgcopy[yc,xc]=(0,0,0)
                        plt.subplot(2, 2, 1), plt.imshow(imgcopy[:, :, ])
                        plt.title('imgcopy'), plt.xticks([]), plt.yticks([])
                        plt.show()
                    puzzle_list.append(path)
                    if (counter %10 == 0):
                        print ("len(puzzle_list): ",len(puzzle_list))
                        print ("len(path): ",len(path))
                    for k in range(length):
                        pathpath = path[k]
                        pathy = int(pathpath[0])
                        pathx = int(pathpath[1])
                        list[pathy,pathx] = False
                        if(pathy >0):
                            list[pathy - 1, pathx] = False
                        if(pathy > 1):
                            list[pathy - 2, pathx] = False
                        if(pathy < height-1):
                            list[pathy+1, pathx] = False
                        if(pathy < height-2):
                            list[pathy + 2, pathx] = False
                        if(pathx> 0):
                            list[pathy, pathx-1] = False
                        if(pathx > 1):
                            list[pathy, pathx -2] = False
                        if(pathx < width-1):
                            list[pathy, pathx+1] = False
                        if(pathx < width-2):
                            list[pathy, pathx+2] = False
                        if(pathx > 0 and pathy > 0):
                            list[pathy -1, pathx -1] = False
                        if(pathx > 0 and pathy < height -1):
                            list[pathy +1, pathx -1] = False
                        if(pathx < width-1 and pathy > 0):
                            list[pathy -1, pathx + 1] = False
                        if(pathx < width-1 and pathy < height-1):
                            list[pathy + 1, pathx+1] = False
    return puzzle_list