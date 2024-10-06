import os
import random
import shutil
from math import floor


def round_allocation(count, ratio):
    """
    Allocate the number of items by rounding according to the allocation ratio.

    Parameters:
    count (int): The total number of items.
    ratio (float): The ratio for allocation.

    Returns:
    int: The number of items allocated by rounding.
    """
    return round(count * ratio)


def copy_data_rounded(src_folder_A, src_folder_B, common_dst_folder, split_ratio=0.8, split_name='train'):
    """
    Copy files from source folders to a specified train or test folder by proportion,
    ensuring the correspondence of files between A and B folders using a rounding method.

    Parameters:
    src_folder_A (str): The source folder A path.
    src_folder_B (str): The source folder B path.
    common_dst_folder (str): The common destination folder path.
    split_ratio (float): The ratio of files to copy to the train folder.
    split_name (str): The name for the train or test split.
    """
    files_A = set(os.listdir(src_folder_A))
    files_B = set(os.listdir(src_folder_B))

    # Ensure matching filenames in folders A and B
    assert files_A == files_B, f"Mismatched filenames: The files in {src_folder_A} and {src_folder_B} do not match."

    total_files = list(files_A)  # Use either set, as they are equal
    total_count = len(total_files)
    target_count = round_allocation(total_count, split_ratio)

    # Ensure the destination directory exists
    os.makedirs(common_dst_folder, exist_ok=True)

    # Build the destination folder paths
    dst_folder_A = os.path.join(common_dst_folder, f'{split_name}A_{os.path.basename(src_folder_A)}')
    dst_folder_B = os.path.join(common_dst_folder, f'{split_name}B_{os.path.basename(src_folder_B)}')
    os.makedirs(dst_folder_A, exist_ok=True)
    os.makedirs(dst_folder_B, exist_ok=True)

    selected_files = random.sample(total_files, target_count)

    # Copy A and B files to the corresponding train or test folders
    for file in selected_files:
        src_path_A = os.path.join(src_folder_A, file)
        src_path_B = os.path.join(src_folder_B, file)
        dst_path_A = os.path.join(dst_folder_A, file)
        dst_path_B = os.path.join(dst_folder_B, file)
        shutil.copy(src_path_A, dst_path_A)  # Copy file from A
        shutil.copy(src_path_B, dst_path_B)  # Copy file from B, ensuring matching filenames


# Define the split ratio
split_ratio = 0.8

# Specify the parent folder path
common_dst_folder = '/path/to/destination/folder'

# Iterate over each completion interval folder
interval_edges = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
folders = [os.path.join(common_dst_folder, f'completion_{i}-{j}') for i, j in
           zip(interval_edges[:-1], interval_edges[1:])]

for folder in folders:
    # Copy files from A and B to train and test folders
    src_folder_A = os.path.join(folder, 'from_A')
    src_folder_B = os.path.join(folder, 'from_B')

    # Copy to trainA and trainB
    copy_data_rounded(src_folder_A, src_folder_B, common_dst_folder, split_ratio, 'train')

    # Adjust the split_ratio for the remaining 30% as the test set (if split_ratio=0.7)
    test_split_ratio = 1 - split_ratio
    copy_data_rounded(src_folder_A, src_folder_B, common_dst_folder, test_split_ratio, 'test')

print("Data has been copied using a rounded allocation, ensuring matching filenames in trainA/trainB and testA/testB.")