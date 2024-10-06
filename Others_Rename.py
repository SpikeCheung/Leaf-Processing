import os
import glob

def rename_files(directory, mode):
    """
    Renames files in the specified directory based on the selected mode.

    Parameters:
    directory (str): The path to the directory containing the files.
    mode (int): The mode of renaming (1-6).
    """
    if mode not in [1, 2, 3, 4, 5, 6]:
        print("Invalid mode. Please choose a mode between 1 and 6.")
        return

    if mode not in [4, 6]:
        files = glob.glob(directory + '/*.png')
        for file in files:
            filename = os.path.basename(file)
            if mode == 1:
                new_filename = filename.replace('_real_B', '')  # Replace
            elif mode == 2:
                new_filename = filename.replace('GT', '')  # Keep the name before "_"
            elif mode == 3:
                new_filename = filename.split('_')[0]  # Replace
            elif mode == 5:
                new_filename = filename.replace('SL', '')  # Replace

            if mode == 3:
                os.rename(file, os.path.join(directory, f'{new_filename}.bmp'))
            else:
                os.rename(file, os.path.join(directory, new_filename))

    elif mode == 4:
        # Renaming for trainB
        file_list = os.listdir(directory)
        file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        src = 'S1'
        count = 0
        for file_name in file_list:
            new_filename = file_name.split('_')[0]
            if new_filename == src:
                count += 1
                os.rename(os.path.join(directory, file_name), os.path.join(directory, f'{new_filename}_{count}.bmp'))
                src = new_filename
            else:
                count = 1
                os.rename(os.path.join(directory, file_name), os.path.join(directory, f'{new_filename}_{count}.bmp'))
                src = new_filename

    elif mode == 6:
        # Leaf matching renaming
        file_list = os.listdir(directory)
        file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        order = [5, 13, 7, 4, 9, 1, 11, 2, 8, 16, 14, 18, 12, 3, 15, 17, 6, 10, 0, 0]
        for file_name in file_list:
            count = 0
            file_name_first = file_name.split('_')[0]
            file_order = int(file_name.split('_')[1].split('.')[0])
            for i in range(len(order)):
                if file_order == order[i]:
                    count = i + 1
                    break
            if count != 0:
                os.rename(os.path.join(directory, file_name),
                          os.path.join(directory, f'{file_name_first}_{count}A.bmp'))

# Please replace /path/to/your/directory with the actual path on your system and specify a Mode before running.

# Usage example
rename_files('/path/to/your/directory', 1)  # Mode 1
# rename_files('/path/to/your/directory', 2)  # Mode 2