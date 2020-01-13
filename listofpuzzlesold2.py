import pixelpath as pp
import cv2
import numpy as np

def list_of_puzzles(list, image0):
    """
    list should be a 2D numpy array of type bool
    consisting of trues wherever there are edges or background.
    image0 should be the filename of an image with the same dimensions.
    Returns a list of lists of pixels corresponding to the edges
    of all suspected puzzles pieces
    """
    puzzle_list = []
    pathx = []
    pathy = []
    img = cv2.imread(image0,0)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1,0,ksize = 5)
    sobely = cv2.Sobel(img,cv2.CV_64F, 0,1, ksize = 5)
    sobel = (sobelx * sobelx + sobely * sobely) ** 0.5
    sobelcopy = np.copy(sobel)
    height = sobel.shape[0]
    width = sobel.shape[1]
    counter = 0
    for i in range (height):
        for j in range (width):
            if(list[i,j]):
                counter += 1
                if(counter%100==0):
                    print("Counter is ", counter, " and (i, j) = (", i, ", ", j, ")")
                path = pp.pixel_path_recurse(i,j,i,j,2000,0,False,0,sobely,sobelx,sobel,sobelcopy, height, width)
                puzzle_list.append(path)
                length = len(path)
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