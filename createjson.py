"""
    Helps creating json files
"""
#!/usr/bin/python3

import os
import json

# Folder range (inclusive)
start_folder = 1
end_folder = 114

# Content for the JSON file
content = {"sections": [[0, 0], [0, 0]]}

for folder_number in range(start_folder, end_folder + 1):
    # Format folder name with leading zeros (e.g., 001)
    folder_name = f"{folder_number:03d}"
    file_name = f"hafs_husr_{folder_name}.json"

    # Create the folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    # Create the JSON file
    with open(os.path.join(folder_name, file_name), "w", encoding="utf-8") as json_file:
        json.dump(content, json_file, indent=2)  # Indent for readability

    print(f"Created JSON file: {os.path.join(folder_name, file_name)}")
