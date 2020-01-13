import numpy as np
from matplotlib import pyplot as plt


def intersection(array1, array2, whether_to_display):
    """array1 and array2 should be 2D numpy arrays of type Bool.
    Returns an array consisting of True just where both are True."""
    if (array1.shape != array2.shape):
        print("Error in intersection, arrays of different shapes:")
        print(array1.shape)
        print(array2.shape)
        return []
    array3 = array1 * array2
    if (whether_to_display):
        plt.subplot(2, 2, 1), plt.imshow(array1[:, :], cmap='gray')
        plt.title('Array 1'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 2), plt.imshow(array2[:, :, ], cmap='gray')
        plt.title('Array 2'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 3), plt.imshow(array3[:, :, ], cmap='gray')
        plt.title('Intersection'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 4), plt.imshow(array3[:, :, ], cmap='gray')
        plt.title('Intersection'), plt.xticks([]), plt.yticks([])

        plt.show()
    return array3


#ar1 = np.zeros((100, 100), dtype=bool)
#ar2 = np.zeros((100, 100), dtype=bool)

#for i in range(100):
#    for j in range(100):
#        if (i % 2 == 1):
#            ar1[i, j] = True
#       if (j % 2 == 1):
#            ar2[i, j] = True
#
#intersection(ar1, ar2, True)
