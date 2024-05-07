#!/usr/bin/python3

"""
    Helps massively creating folders and files
"""

import os

def create_structure(riwaya, surah_name, num_folders):
    """
    Creates a directory structure with subfolders and text files.

    Args:
        base_dir (str): Path to the base directory.
        num_folders (int): Number of folders to create (001 to num_folders).
    """

    #getting base_dir and base_url based on Riwaya
    if "Hafs" == riwaya:
        base_dir = "01 - Hafs A'n Assem - حفص عن عاصم/"
        base_url= "https://server13.mp3quran.net/husr"
    elif "Qalon" == riwaya:
        base_dir = "02 - Qalon A'n Nafi' - قالون عن ناف/"
        base_url= " https://server13.mp3quran.net/download/husr/Rewayat-Qalon-A-n-Nafi"
    else:
        print(' ')

    readme = f"""
## Working file for Surah {surah_name}.

You can listen to and download the working file for [{surah_name}]({base_url}/{surah_name[:3]}.mp3)

**Copyright mp3Quran**

<audio controls src="{base_url}/{surah_name[:3]}.mp3"></audio>
"""
    #print (readme)
    #Creating README for each Surah
    folder_path = os.path.join(base_dir, surah_name)
    file_path = os.path.join(folder_path, "README.md")
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
    else:
        with open(file_path, "a",encoding="utf-8") as f:
            f.write(readme)

    for i in range(1, num_folders + 1):
        # Format folder name with leading zeros
        folder_name = f"{i:03d}"
        folder_path = os.path.join(base_dir, surah_name,folder_name)

        # Create folder if it doesn't exist (avoids pylint warning for potential OSError)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create text file with the same name as the folder
        file_path = os.path.join(folder_path, f"{folder_name}.txt")
        if os.path.exists(file_path):
            print(f"The file '{file_path}' exists.")
        else:
            with open(file_path, "a",encoding="utf-8") as f:
                f.write("")  # Empty file

        file_path = os.path.join(folder_path, f"{folder_name}.aup")
        if os.path.exists(file_path):
                print(f"The file '{file_path}' exists.")
        else:
            with open(file_path, "a",encoding="utf-8") as f:
                f.write("")  # Empty file

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create folders and text files")
    parser.add_argument("riwaya", help="Riwaya's working directories")
    parser.add_argument("num_folders", type=int, help="Number of folders to create")
    parser.add_argument("surah_name", help="Surah name")

    args = parser.parse_args()
    create_structure(args.riwaya, args.surah_name, args.num_folders)
    print(f"Successfully created {args.num_folders} folders and text files within '{args.surah_name}'.")
