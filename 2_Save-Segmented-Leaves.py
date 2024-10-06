import os
import cv2
import torch
from PIL import Image
from ultralytics import YOLO
import numpy as np

def img_paste(img_path, save_path, polygon_dict, save_name):
    """
    Paste a polygon mask onto an image and save the result.

    Parameters:
    img_path (str): Path to the input image.
    polygon_dict (dict): Dictionary containing the polygon coordinates.
    save_name (str): Name for the saved image.
    """
    image = cv2.imread(img_path)

    # Create a zero array the same size as the input image
    im = np.zeros(image.shape[:2], dtype="uint8")
    # Draw all the points
    cv2.polylines(im, [polygon_dict], 1, 255)
    # Connect all points to form a closed area
    cv2.fillPoly(im, [polygon_dict], 255)
    mask = im

    # Perform a bitwise AND to mask the area
    masked = cv2.bitwise_and(image, image, mask=mask)

    # Split and merge the channels to convert from BGR to RGB
    b, g, r = cv2.split(masked)
    masked = cv2.merge([r, g, b])

    # Convert masked image to PIL format
    image_1 = Image.fromarray(masked)

    # Save the masked image
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_1.save(os.path.join(save_path, save_name))

# Please replace /path/to/input/images, /path/to/output/images, and /path/to/model/weights/best.pt with the actual
# paths on your system before running the script.


if __name__ == "__main__":
    dir_path = '/path/to/input/images'  # Specify the directory path
    out_dir_path = '/path/to/output/images/'

    file_list = os.listdir(dir_path)
    file_list.sort(key=lambda x: x.split('_')[0])

    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            print(file_name)

    for file_name in file_list:
        img_path = os.path.join(dir_path, file_name)
        save_fn = file_name.split('_')[0]
        save_fn = save_fn[0:-4]

        # Load the segmentation model
        model = YOLO('/path/to/model/weights/best.pt')
        prediction = model(img_path)

        for i, pixel_xy in enumerate(prediction[0].masks.xy):
            points = np.array(pixel_xy, np.int32)

            # Paste the polygon mask and save the image
            img_paste(img_path, out_dir_path, points, f'{save_fn}_{i + 1}.bmp')