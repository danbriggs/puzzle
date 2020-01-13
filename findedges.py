import cv2

def find_edges(list, image0,cutoff):
    img = cv2.imread(image0, 0)
    img1 = cv2.imread(image0)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    sobel = (sobelx * sobelx + sobely * sobely) ** 0.5
    height = img.shape[0]
    width = img.shape[1]
    for i in range(height):
        for j in range(width):
            if(sobel[i,j] > cutoff):
                list[i,j] = True

    return list
