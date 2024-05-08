#!/usr/bin/python3

import requests

# Replace with your details
github_username = "Mchit-W-Jit"
github_repo = "QVTonSubjects"
label_name = "new-label"
label_color = "f29513"  # Red in hex code
access_token = "Change_me"

url = f"https://api.github.com/repos/{github_username}/{github_repo}/labels"

data = {
    "name": label_name,
    "color": label_color,
    # Optional: description="A descriptive text for the label"
}

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {access_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

response = requests.post(url, headers=headers, json=data, timeout=5)

if response.status_code == 201:
    print(f"Label '{label_name}' created successfully!")
else:
    print(f"Error creating label: {response.text}, status code {response.status_code}")
