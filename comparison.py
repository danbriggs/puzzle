from PIL import Image, ImageChops

def compared(image1, image2):
    """
    this part doesn't work :(
    """
    diff = ImageChops.difference(image1, image2)
    return diff
def comparison(compare, image, filename):
    """
    Takes in the most matches rotation of the puzzle piece and
    paste it in the bigger picture.
    """
    img1 = Image.open(filename)
    img1 = img1.rotate(compare)
    img2 = Image.open(image)
    width = img1.width
    height = img1.height
    width1 = img2.width
    height1 = img2.height
    height0 = 0
    width0 = 0
    comparing = (0, 0, 100, 100)
    print(compared("tmp1rdo_s7u.jpg", image))
    for i in range(width1 - width):
        for j in range(height1 - height):
            img2.paste(img1, (i, j))
            img2.save("tmp1rdo_s7u.jpg")
            if comparing > compared("tmp1rdo_s7u.jpg", image):
                comparing = compared("tmp1rdo_s7u.jpg", image)
                height0 = j
                width0 = i
    img2.past(img1, (height0, width0))
    img2.save("tmp1rdo_s7u.jpg")
    img2.show()