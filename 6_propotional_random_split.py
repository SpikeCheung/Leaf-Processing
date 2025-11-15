import os
import random
import shutil

def safe_mkdir(path):
    """Create folder if it does not exist."""
    os.makedirs(path, exist_ok=True)


def split_dataset_no_leakage(src_folder_A, src_folder_B, split_ratio=0.8):
    """
    One-time sampling → ensures no sample leakage between train / test.

    Parameters:
    src_folder_A: path to A images (incomplete)
    src_folder_B: path to B images (complete)
    split_ratio: ratio for train

    Returns:
    train_files, test_files sets
    """
    files_A = set(os.listdir(src_folder_A))
    files_B = set(os.listdir(src_folder_B))

    # Ensure perfect filename matching
    assert files_A == files_B, f"Mismatched files in:\n{src_folder_A}\n{src_folder_B}"

    all_files = sorted(list(files_A))
    total_count = len(all_files)

    train_count = round(total_count * split_ratio)

    # One-time sampling → avoids train/test duplication
    train_files = set(random.sample(all_files, train_count))
    test_files = set(all_files) - train_files

    return train_files, test_files


def copy_files(file_list, src_A, src_B, dst_A, dst_B):
    """Copy matched A/B files into destination folders."""
    safe_mkdir(dst_A)
    safe_mkdir(dst_B)

    for f in file_list:
        shutil.copy(os.path.join(src_A, f), os.path.join(dst_A, f))
        shutil.copy(os.path.join(src_B, f), os.path.join(dst_B, f))


def main():
    # ========== MODIFY THIS ==========
    common_dst_folder = '/path/to/destination/folder'
    split_ratio = 0.8
    # =================================

    safe_mkdir(common_dst_folder)

    # Define 10 completeness intervals (0–0.1, 0.1–0.2, ..., 0.9–1.0)
    interval_edges = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    folders = [
        os.path.join(common_dst_folder, f'completion_{i}-{j}')
        for i, j in zip(interval_edges[:-1], interval_edges[1:])
    ]

    # Global train/test output folders
    dst_train_A = os.path.join(common_dst_folder, 'trainA')
    dst_train_B = os.path.join(common_dst_folder, 'trainB')
    dst_test_A  = os.path.join(common_dst_folder, 'testA')
    dst_test_B  = os.path.join(common_dst_folder, 'testB')

    safe_mkdir(dst_train_A)
    safe_mkdir(dst_train_B)
    safe_mkdir(dst_test_A)
    safe_mkdir(dst_test_B)

    # Process each completeness interval folder independently
    for folder in folders:
        srcA = os.path.join(folder, 'from_A')
        srcB = os.path.join(folder, 'from_B')

        if not os.path.exists(srcA) or not os.path.exists(srcB):
            print(f"Skipping missing folder: {folder}")
            continue

        print(f"Processing: {folder}")

        # One-time fair split → no leakage
        train_files, test_files = split_dataset_no_leakage(srcA, srcB, split_ratio)

        copy_files(train_files, srcA, srcB, dst_train_A, dst_train_B)
        copy_files(test_files, srcA, srcB, dst_test_A, dst_test_B)


if __name__ == "__main__":
    main()
