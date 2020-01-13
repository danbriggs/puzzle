import numpy as np
import cv2
import pylab as pl


def compute_pointness(I, n=5):
    # Compute gradients
    # GX = cv2.Sobel(I, cv2.CV_32F, 1, 0, ksize=5, scale=1)
    # GY = cv2.Sobel(I, cv2.CV_32F, 0, 1, ksize=5, scale=1)
    GX = cv2.Scharr(I, cv2.CV_32F, 1, 0, scale=1)
    GY = cv2.Scharr(I, cv2.CV_32F, 0, 1, scale=1)
    GX = GX + 0.0001  # Avoid div by zero

    # Threshold and invert image for finding contours
    _, I = cv2.threshold(I, 100, 255, cv2.THRESH_BINARY_INV)
    # Pass in copy of image because findContours apparently modifies input.
    C, H = cv2.findContours(I.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    heatmap = np.zeros_like(I, dtype=np.float)
    pointed_points = []
    for contour in C:
        contour = contour.squeeze()
        measure = []
        N = len(contour)
        for i in range(N):
            x1, y1 = contour[i]
            x2, y2 = contour[(i + n) % N]

            # Angle between gradient vectors (gx1, gy1) and (gx2, gy2)
            gx1 = GX[y1, x1]
            gy1 = GY[y1, x1]
            gx2 = GX[y2, x2]
            gy2 = GY[y2, x2]
            cos_angle = gx1 * gx2 + gy1 * gy2
            cos_angle /= (np.linalg.norm((gx1, gy1)) * np.linalg.norm((gx2, gy2)))
            angle = np.arccos(cos_angle)
            if cos_angle < 0:
                angle = np.pi - angle

            x1, y1 = contour[((2*i + n) // 2) % N]  # Get the middle point between i and (i + n)
            heatmap[y1, x1] = angle  # Use angle between gradient vectors as score
            measure.append((angle, x1, y1, gx1, gy1))

        _, x1, y1, gx1, gy1 = max(measure)  # Most pointed point for each contour

        # Possible to filter for those blobs with measure > val in heatmap instead.
        pointed_points.append((x1, y1, gx1, gy1))

    heatmap = cv2.GaussianBlur(heatmap, (3, 3), heatmap.max())
    return heatmap, pointed_points


def plot_points(image, pointed_points, radius=5, color=(255, 0, 0)):
    for (x1, y1, _, _) in pointed_points:
        cv2.circle(image, (x1, y1), radius, color, -1)

def main():
    I = cv2.imread("glLqt.jpg", 0)
    heatmap, pointed_points = compute_pointness(I, n=5)
    pl.figure()
    pl.imshow(heatmap, cmap=pl.cm.jet)
    pl.colorbar()
    I_color = cv2.cvtColor(I, cv2.COLOR_GRAY2RGB)
    plot_points(I_color, pointed_points)
    pl.figure()
    pl.imshow(I_color)
    pl.show()


if __name__ == '__main__':
    main()