import os
import pandas as pd
import cv2
import numpy as np

dir_path = ''  # Input dir path
out_dir = ''  # Save dir path
file_list = os.listdir(dir_path)

# Automatically determine the sorting order based on the directory name
if 'real' in dir_path[-6:]:
    file_list.sort(key=lambda x: int(x.replace("_", "").replace("realA", "").replace("realB", "").split(".")[0]))
    print('real')
elif 'fake' in dir_path[-6:]:
    file_list.sort(key=lambda x: int(x.replace("_", "").replace("fakeA", "").replace("fakeB", "").split(".")[0]))
    print('fake')
# file_list.sort(key=lambda x: int(x.replace("_", "").split(".")[0]))

data_list = []

# Check if data_list is empty, if so, initialize an empty DataFrame
if not data_list:
    df = pd.DataFrame(columns=['ImageName', 'LeafLength', 'LeafWidth', 'LeafPerimeter', 'LeafArea', 'Width1', 'Width2'])
else:
    # Directly create DataFrame from list, assuming each dictionary has the correct keys
    df = pd.DataFrame(data_list,
                      columns=['ImageName', 'LeafLength', 'LeafWidth', 'LeafPerimeter', 'LeafArea', 'Width1', 'Width2'])

for file_name in file_list:

    in_path = os.path.join(dir_path, file_name)
    out_path = os.path.join(out_dir, file_name)

    ####################################################################################################
    "Extract valid pixels by Binary image processing"
    # Load the image
    img = cv2.imread(in_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarize the image, setting non-black areas to 1
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ####################################################################################################

    ####################################################################################################
    "Extract valid pixels by HSV if needed"
    # # Load the image
    # img = cv2.imread(in_path)
    #
    # # Convert the image to HSV
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #
    # # Set the green threshold range
    # lower_green = np.array([10, 20, 20])
    # upper_green = np.array([200, 255, 255])
    #
    # # Create a mask based on the threshold
    # mask = cv2.inRange(hsv, lower_green, upper_green)
    #
    # # morphological operations to improve the mask
    # kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.dilate(mask, kernel, iterations=1)
    # mask = cv2.erode(mask, kernel, iterations=1)
    #
    # # Finding contours in a binary image
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ####################################################################################################

    # Find the largest contour, which is the leaf contour
    cnt = max(contours, key=cv2.contourArea)

    # Calculate the minimum bounding rectangle of the leaf
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    x, y, w, h = cv2.boundingRect(cnt)  # Bounding rectangle

    masked = img.copy()
    masked = cv2.drawContours(masked, [cnt], -1, (0, 255, 0), thickness=1)

    # Calculate leaf length, width, and area
    w2 = rect[1][1] if rect[1][1] < rect[1][0] else rect[1][0]
    if w - w2 < 12:
        leaf_width = w
        cv2.rectangle(masked, (x, y), (x + w, y + h), (0, 255, 0), thickness=1)
    else:
        leaf_width = w2
        masked = cv2.drawContours(masked, [box], 0, (0, 255, 0), 1)

    leaf_length = h
    leaf_c = cv2.arcLength(cnt, True)
    leaf_area = cv2.contourArea(cnt)

    img_name = file_name.split(".")[0]
    print(
        f'{img_name}: Leaf Length: {leaf_length}, Leaf Width: {leaf_width}, Leaf Perimeter: {leaf_c}, Leaf Area: {leaf_area}, Width: {w} or {w2}')
    leaf_data = {
        'ImageName': img_name,
        'LeafLength': leaf_length,
        'LeafWidth': leaf_width,
        'LeafPerimeter': leaf_c,
        'LeafArea': leaf_area,
        'Width1': w,
        'Width2': w2
    }
    data_list.append(leaf_data)

    # Save the masked image
    cv2.imwrite(out_path, masked)

# Concatenate all data into a single DataFrame
df = pd.concat([pd.DataFrame(data) for data in data_list], ignore_index=True)
# Save the DataFrame as a CSV file
output_csv_path = os.path.join(out_dir, 'leaf_data.csv')
df.to_csv(output_csv_path, index=False)