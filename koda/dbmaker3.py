import os
import shutil
import random


def remove_files_with_number(file_names, number):
    return [name for name in file_names if name[7] != str(number)]


def save_file_names(input_folder):
    return [filename for filename in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, filename))]


def copy_files(file_names, source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for name in file_names:
        source_path = os.path.join(source_folder, name)
        destination_path = os.path.join(destination_folder, name)
        shutil.copy(source_path, destination_path)
        print(name)


def replace_extensions(filenames, ex1, ex2):
    return [filename.replace(ex1, ex2) for filename in filenames]


def rename_files(file_names, before, after):
    new_names = []
    for name in file_names:
        if 'frameC' in name:
            name = name.replace(before, after)
        new_names.append(name)
    return new_names


def split_train_test(file_names):
    random.shuffle(file_names)
    split_index = int(0.8 * len(file_names))
    return file_names[:split_index], file_names[split_index:]


def create_dataset(database_num, source_folder, image_folder, destination_folder, exclude_numbers, letter):
    all_names = save_file_names(source_folder)
    for num in exclude_numbers:
        all_names = remove_files_with_number(all_names, num)
    
    train_list, test_list = split_train_test(all_names)

    copy_files(train_list, source_folder, os.path.join(destination_folder, f"{letter}_jsons_train"))
    copy_files(test_list, source_folder, os.path.join(destination_folder, f"{letter}_jsons_test"))

    train_list = replace_extensions(train_list, ".json", ".jpg")
    test_list = replace_extensions(test_list, ".json", ".jpg")

    train_list = rename_files(train_list, "A", "B")
    test_list = rename_files(test_list, "A", "B")

    copy_files(train_list, image_folder, os.path.join(destination_folder, f"{letter}_images_train"))
    copy_files(test_list, image_folder, os.path.join(destination_folder, f"{letter}_images_test"))


database_num = 7
source_folder = "database_jsons"
image_folder = "database_B_images"
destination_folder = f"database{database_num}"

# A images
exclude_numbers = [2, 3, 4, 5]
create_dataset(database_num, source_folder, image_folder, destination_folder, exclude_numbers, "A")

# B images
exclude_numbers = [1, 3, 4, 6]
create_dataset(database_num, source_folder, image_folder, destination_folder, exclude_numbers, "B")

# C images
exclude_numbers = [1, 2, 4, 6]
create_dataset(database_num, source_folder, image_folder, destination_folder, exclude_numbers, "C")
