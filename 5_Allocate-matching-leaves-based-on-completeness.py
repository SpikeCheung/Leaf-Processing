import os
import cv2
import shutil
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
    # Find the largest contour, assumed to be the leaf contour
    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    return area

# Please replace /path/to/all_A, /path/to/all_B, and /path/to/train with the actual paths on your system before running the script.

# Set the directory paths
dir_A = '/path/to/all_A'
dir_B = '/path/to/all_B'

# List files in directory A and sort them by numeric value
file_list = os.listdir(dir_A)
file_list.sort(key=lambda x: int(x.replace("_", "").split(".")[0]))

# Define completion intervals and initialize counters if needed
interval_edges = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
base_path = '/path/to/train'
folders_to_create = [os.path.join(base_path, f'completion_{i}-{j}') for i, j in zip(interval_edges[:-1], interval_edges[1:])]
# Create subfolders for A and B
for folder in folders_to_create:
    os.makedirs(os.path.join(folder, 'from_A'), exist_ok=True)
    os.makedirs(os.path.join(folder, 'from_B'), exist_ok=True)

# Initialize completion counters
c_counts = {f'c{i}': {'A': 0, 'B': 0} for i in range(10)}

# Process each file in the list
for file_name in file_list:
    A_path = os.path.join(dir_A, file_name)
    B_path = os.path.join(dir_B, file_name)

    # Count the area for both images
    area_A = count_area(A_path)
    area_B = count_area(B_path)

    # Calculate the completion ratio
    completion = area_A / area_B
    print(f"Image '{file_name}' completion: {completion:.2f}")

    # Determine the target folder based on the completion ratio
    target_folder = next(
        folder for i, folder in enumerate(folders_to_create) if interval_edges[i] <= completion < interval_edges[i + 1])

    # Move files to the corresponding folder
    new_A_path = os.path.join(target_folder, 'from_A', file_name)
    new_B_path = os.path.join(target_folder, 'from_B', file_name)
    shutil.move(A_path, new_A_path)
    shutil.move(B_path, new_B_path)

    # Update counters
    for i, edge in enumerate(interval_edges[:-1]):
        if edge <= completion < interval_edges[i + 1]:
            c_counts[f'c{i}']['A'] += 1
            c_counts[f'c{i}']['B'] += 1
            break

# Print the number of images in each completion interval for A and B
print("\nNumber of images in each completion interval (A/B):")
for key, value in c_counts.items():
    print(f"{key}: A-{value['A']} B-{value['B']}")