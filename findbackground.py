import cv2
import edge_stats as es
def find_background(image0, depth):
    """Return a numpy matrix of boolean corresponding to whether each
    pixel is to be considered a background pixel"""
    ans = es.border_color_statistics(image0, depth)
    return ans
