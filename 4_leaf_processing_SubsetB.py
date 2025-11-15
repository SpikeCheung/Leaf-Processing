import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def read_file(dir_path):
    """
    Reads and returns a list of filenames from the given directory path.

    Parameters:
    dir_path (str): The path to the directory containing the images.

    Returns:
    list: A list of filenames in the directory.
    """
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            print(file_name)
    return file_list

# Set the directory paths
dir_Path = "/path/to/trainB/"
our_dir_path = "/path/to/new_trainB/"
file_List = read_file(dir_Path)

# Process each file in the list
for file_Name in file_List:
    img_path = os.path.join(dir_Path, file_Name)
    img = cv2.imread(img_path)

    ########################################################################################################
    """
    use EXG-Otsu to segment detached leaves
    """
    # Convert the image to float for calculation
    fsrc = np.array(img, dtype=np.float32) / 255.0
    (b, g, r) = cv2.split(fsrc)
    gray = 2 * g - b - r

    # Calculate the minimum and maximum values in the image
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    # Compute the histogram of the grayscale image
    hist = cv2.calcHist([gray], [0], None, [256], [minVal, maxVal])

    # Convert the grayscale image to 8-bit and apply Otsu's thresholding
    gray_u8 = np.array((gray - minVal) / (maxVal - minVal) * 255, dtype=np.uint8)
    (thresh, bin_img) = cv2.threshold(gray_u8, -1.0, 255, cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ########################################################################################################

    ########################################################################################################
    """
    use hsv if needed
    """
    # # Convert the image to HSV color space
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #
    # # Define the HSV range for green color
    # lower_green = np.array([5, 0, 0])
    # upper_green = np.array([150, 255, 255])
    #
    # # Create a mask for the green color
    # mask = cv2.inRange(hsv, lower_green, upper_green)
    #
    # # Morphological operations to remove noise
    # kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    #
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #########################################################################################################

    #########################################################################################################
    """
    use binarization if needed
    """
    # # Convert the image to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # # binarization
    # _, binary = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    #
    # contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #########################################################################################################

    cnt = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(cnt)

    im = np.zeros(img.shape[:2], dtype="uint8")
    cv2.polylines(im, [cnt], 1, 255)
    # Connect all points to form a closed area
    cv2.fillPoly(im, [cnt], 255)
    mask = im
    masked = cv2.bitwise_and(img, img, mask=mask)

    masked = masked[y:y + h, x:x + w]

    # Create a black background
    black_background = np.zeros((1024, 1024, 3), np.uint8)

    # Calculate the position where the image should be placed
    height, width, _ = masked.shape
    x = (1024 - width) // 2
    y = (1024 - height) // 2

    # Paste the image onto the black background
    try:
        black_background[y:y + height, x:x + width] = masked
    except ValueError:
        print(f'Error processing file: {file_Name}')

    # Save the new image
    cv2.imwrite(os.path.join(our_dir_path, file_Name), black_background)
