import os
import cv2
import numpy as np

def count_area(img_path):
    """
    Count the area of the largest contour in the image.

    Parameters:
    img_path (str): The path to the image file.

    Returns:
    float: The area of the largest contour.
    """
    # Load the image
    image = cv2.imread(img_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary thresholding to the grayscale image
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour, which is assumed to be the leaf contour
    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    return area

# Please replace /path/to/real_A/images and /path/to/real_B/images with the actual paths on your system before running the script.
# Define the directory paths
dir_A = '/path/to/real_A/images'
dir_B = '/path/to/real_B/images'

# List files in directory A and sort them
file_list = os.listdir(dir_A)
file_list.sort(key=lambda x: int(x.replace("_", "").replace("realA", "").replace("realB", "").split(".")[0]))

# Iterate over the sorted file list
for file_name in file_list:
    A_path = os.path.join(dir_A, file_name)
    B_path = os.path.join(dir_B, file_name)

    # Count the area for both images
    area_A = count_area(A_path)
    area_B = count_area(B_path)

    # Calculate the completion ratio
    completion = area_A / area_B if area_B != 0 else 0

    # Print the completion ratio for the current file
    print(f'{file_name} Completion: {completion}')