import os
import cv2
import numpy as np
from PIL import Image

"""
Reads and returns a list of filenames from the given directory path.
"""


def read_file(dir_path):
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            print(file_name)
    return file_list


"""
Finds the center of the green object in the image using super green segmentation.
Returns the center coordinates (center_x, center_y) after extracting the largest connected area.
"""


def find_center(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to float for calculation
    f_src = np.array(img, dtype=np.float32) / 255.0
    (b, g, r) = cv2.split(f_src)
    gray = 2 * g - b - r

    # Calculate the minimum and maximum values
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    # Calculate the histogram
    hist = cv2.calcHist([gray], [0], None, [256], [minVal, maxVal])

    # Convert to u8 type and perform Otsu binarization
    gray_u8 = np.array((gray - minVal) / (maxVal - minVal) * 255, dtype=np.uint8)
    (thresh, bin_img) = cv2.threshold(gray_u8, -1.0, 255, cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(cnt)
    center_x = x + w / 2
    center_y = y + h / 2
    print(center_x, center_y)
    return center_x, center_y


"""
Rotates the leaf image so that the leaf is facing upwards.
Calculates the rotation angle based on the center of the leaf and rotates the image accordingly.
"""


def rotate_leaf(image_path, new_img_path, save_path, center):
    # Read the image
    o_leaf = cv2.imread(image_path, 0)

    # Calculate the leaf center
    leaf_y, leaf_x = np.where(o_leaf > 0)
    leaf_center_x, leaf_center_y = np.mean(leaf_x), np.mean(leaf_y)
    print(leaf_center_x, leaf_center_y)

    # Calculate the rotation angle
    dx = leaf_center_x - center[0]
    dy = leaf_center_y - center[1]
    angle = np.arctan2(dy, dx) * 180. / np.pi
    rotation_angle = angle + 90
    print(rotation_angle)

    # Rotate the leaf to face upwards
    leaf = cv2.imread(new_img_path)
    rows, cols = leaf.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)
    rotated_img = cv2.warpAffine(leaf, M, (cols, rows))

    cv2.imwrite(save_path, rotated_img)


"""
Moves the leaf to the center of the image and crops it to the required size.
"""


def move_leaf_to_center(image_path, out_path, img_size):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Find the leaf's boundary
    left, upper, right, lower = img.getbbox()

    # Calculate the leaf's center point
    center_x = (right - left) // 2 + left
    center_y = (lower - upper) // 2 + upper

    # Calculate new boundaries
    new_left = (width - img_size[0]) // 2
    new_upper = (height - img_size[1]) // 2
    new_right = new_left + img_size[0]
    new_lower = new_upper + img_size[1]

    # Crop the image
    img = img.crop((new_left, new_upper, new_right, new_lower))

    # Save the new image
    img.save(out_path)

# Define the paths
leaf_path = "/path/to/leaf/images/"
our_dir_path = "/path/to/output/images/"
val_path = '/path/to/validation/images/'
img_list = read_file(leaf_path)

for img_name in img_list:
    img_path = os.path.join(leaf_path, img_name)
    save_Path = os.path.join(our_dir_path, img_name)
    plant_Num = img_name.split('_')[0]
    plant_path = os.path.join(val_path, f"{plant_Num}.bmp")
    print(plant_path)
    cX, cY = find_center(plant_path)
    print(f"Center coordinates: ({cX}, {cY})")
    move_leaf_to_center(img_path, save_Path, [1024, 1024])
    rotate_leaf(img_path, save_Path, save_Path, [cX, cY])