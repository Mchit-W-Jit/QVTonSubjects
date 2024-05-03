#!/usr/bin/python3

import argparse
import subprocess

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
  command = ["ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", "-b:a", 
             str(bitrate) + "k", output_file]
  subprocess.run(command, check=True)

def main():
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
  print(f"Successfully converted {args.input_file} to {args.output_file} 
        with bitrate {args.bitrate} kbps")
  if args.reciter:
      print(f"Quran Reciter: {args.reciter}")
  if args.surah_number:
      print(f"Surah Number: {args.surah_number}")

if __name__ == "__main__":
  main()
