"""Module generate mp3 files from audacity."""

#!/usr/bin/python3

import argparse
import subprocess
import os
import json
from argparse import ArgumentParser

def trim_mp3_from_json(json_dir):
  """
  Trims MP3 files based on start time and duration from JSON files within subdirectories.

  Args:
      json_dir (str): Path to the directory containing subdirectories with JSON files.
  """
  # Loop through subdirectories (assuming folder naming convention from 001 to 114)
  for folder_num in range(1, 115):  # 1 to 114 (inclusive)
    folder_name = f"folder_{folder_num:03d}"  # Pad with zeros for 3 digits
    subfolder_path = os.path.join(json_dir, folder_name)

    # Check if subdirectory exists
    if os.path.isdir(subfolder_path):
      # Find the JSON file within the subdirectory
      json_file = os.path.join(subfolder_path, "data.json")  # Assuming file name is "data.json"

      # Check if JSON file exists
      if os.path.isfile(json_file):
        try:
          # Call the function to process the specific JSON file
          trim_mp3_from_json_file(json_file)
        except FileNotFoundError as e:
          print(f"Error: File not found - {json_file}")
      else:
        print(f"Skipping: JSON file not found - {json_file}")
    else:
      print(f"Skipping: Subdirectory not found - {subfolder_path}")

def trim_mp3_from_json_file(json_file_path):
    """
    Trims an MP3 file based on start time and duration from a JSON file.

    Args:
      json_file_path (str): Path to the JSON file containing audio information.
    """
    # Read the JSON file
    with open(json_file_path, "r",encoding="utf-8") as f:
        data = json.load(f)

    # Extract audio information
    mp3_link = data["link"]
    edges = data["edges"]

    # Check if edges exist
    if not edges:
        print(f"No 'edges' data found in JSON file: {json_file_path}")
        return

    # Extract first edge for trimming
    start_time, duration = edges[0]

    # Construct ffmpeg command (replace with your actual command if needed)
    ffmpeg_command = f"ffmpeg -ss {start_time} -t {duration} -i '{mp3_link}' -c:a copy trimmed.mp3"

    # Download and trim the MP3 file (assuming curl is installed)
    try:
        # Download the MP3 (optional, modify if download is not needed)
        #subprocess.run(["curl", "-L", mp3_link, "-o", "temp.mp3"])

        # Execute ffmpeg command to trim
        subprocess.run(ffmpeg_command.split(), check=True)
        print(f"Trimmed MP3 saved as 'trimmed.mp3'")

        # Remove temporary file (optional)
        os.remove("temp.mp3")
    except subprocess.CalledProcessError as e:
        print(f"Error trimming MP3: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")

def convert_to_mp3(input_file, output_file, bitrate=192, reciter=None,
                   surah_number=None):
  """
  Converts an audio file to MP3 using ffmpeg (example with Quran reciter and Surah arguments).

  Args:
      input_file (str): Path to the input audio file.
      output_file (str): Path to the output MP3 file.
      bitrate (int, optional): MP3 bitrate (default: 192 kbps).
      reciter (str, optional): Quran reciter name.
      surah_number (int, optional): Surah number in the Quran.
  """
  command = ["ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", "-b:a", str(bitrate) + "k", output_file]
  subprocess.run(command, check=True)

def main():
  """Main function."""
  # Parse user arguments
  parser = argparse.ArgumentParser(description="Convert audio file to MP3 (Quran)")
  parser.add_argument("input_file", help="Path to the input audio file")
  parser.add_argument("output_file", help="Path to the output MP3 file")
  parser.add_argument("-b", "--bitrate", type=int, default=192,
                      help="MP3 bitrate (default: 192 kbps)")
  parser.add_argument("-r", "--reciter", help="Quran reciter name", required=False)
  parser.add_argument("-sn", "--surah_number", type=int, help="Surah number", required=False)
  args = parser.parse_args()
  # Call the conversion function with user-provided arguments
  convert_to_mp3(args.input_file, args.output_file, args.bitrate, args.reciter, args.surah_number)
  print(f"Successfully converted {args.input_file} to {args.output_file} with bitrate {args.bitrate} kbps")
  if args.reciter:
      print(f"Quran Reciter: {args.reciter}")
  if args.surah_number:
      print(f"Surah Number: {args.surah_number}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = ArgumentParser(description="Trim MP3 file based on JSON data.")
    parser.add_argument("json_file", type=str, help="Path to the JSON file containing audio information.")
    args = parser.parse_args()

    # Call the trim function with the provided JSON file path
    trim_mp3_from_json(args.json_file)
