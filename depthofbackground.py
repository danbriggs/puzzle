from operator import mul
from PIL import Image
import numpy as np

def depth_of_background(image0):
    im = Image.open(image0)
    pixel_color = im.load()
    height0 = im.size[1]
    width0 = im.size[0]
    color_stats = []
    color_stats1 = []
    depth1 = height0
    depth2 = width0
    depth3 = height0
    depth4 = width0
    for i in range(height0):
        color_stats.append(pixel_color[0, i])
        if(np.all(np.subtract(tuple(map(mul,color_stats[i*2],color_stats[i*2])), tuple(map(mul, color_stats[0],color_stats[0]))) > (100,100,100))):
            depth1 = i
            break
        color_stats.append(pixel_color[width0-1, i])
        if(np.all(np.subtract(tuple(map(mul,color_stats[1+i*2],color_stats[1+i*2])), tuple(map(mul,color_stats[1],color_stats[1]))) > (100,100,100))):
            depth3 = i
            break
    for j in range(width0):
        color_stats1.append(pixel_color[j,0])
        if(np.all(np.subtract(tuple(map(mul,color_stats1[j*2],color_stats1[j*2])), tuple(map(mul,color_stats1[0],color_stats1[0]))) > (100,100,100))):
            depth2 = j
            break
        color_stats1.append(pixel_color[j, height0-1])
        if(np.all(np.subtract(tuple(map(mul,color_stats1[1+j*2],color_stats1[1+j*2])), tuple(map(mul,color_stats1[1],color_stats1[1]))) > (100,100,100))):
            depth4 = j
            break
    return min(depth1, depth2, depth3, depth4)