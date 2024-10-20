#!/usr/bin/python3
"""
Module generate mp3 files from audacity.
"""
import subprocess
import os
import json
from datetime import datetime
from argparse import ArgumentParser


def trim_mp3_from_json(json_dir):
    """
    Trims MP3 files based on start time and duration from JSON files within subdirectories.

    Args:
      json_dir (str): Path to the directory containing subdirectories with JSON files.
    """
    # Loop through subdirectories (assuming folder naming convention from 001 to 114)
    for folder_num in range(1, 115):  # 1 to 114 (inclusive)
        folder_name = f"{folder_num:03d}"  # Pad with zeros for 3 digits
        subfolder_path = os.path.join(json_dir, folder_name)

        # Check if subdirectory exists
        if os.path.isdir(subfolder_path):
            # Find the JSON file within the subdirectory
            json_file = os.path.join(subfolder_path, "data.json")

            # Check if JSON file exists
            if os.path.isfile(json_file):
                try:
                    # Call the function to process the specific JSON file
                    trim_mp3_from_json_file(json_file)
                except FileNotFoundError as e:
                    print(f"Error: File not found - {json_file} {e}")
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
    with open(json_file_path, "r", encoding="utf-8") as f:
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
    ffmpeg_command = (
        f"ffmpeg -ss {start_time} -t {duration} -i '{mp3_link}' -c:a copy trimmed.mp3"
    )

    # Download and trim the MP3 file (assuming curl is installed)
    try:
        # Execute ffmpeg command to trim
        subprocess.run(ffmpeg_command.split(), check=True)
        print("Trimmed MP3 saved as 'trimmed.mp3'")

        # Remove temporary file (optional)
        os.remove("temp.mp3")
    except subprocess.CalledProcessError as e:
        print(f"Error trimming MP3: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")


def calculate_duration(start_time_str, end_time_str):
    """
    Calculates the duration as the difference between two times in "hh:mm:ss.ss" format.

    Args:
        start_time_str (str): The start time in "hh:mm:ss.ss" format.
        end_time_str (str): The end time in "hh:mm:ss.ss" format.

    Returns:
        str: The duration in "hh:mm:ss.ss" format.
    """
    try:
        # Parse strings to datetime objects
        start_time = datetime.strptime(start_time_str, "%H:%M:%S.%f")
        end_time = datetime.strptime(end_time_str, "%H:%M:%S.%f")

        # Calculate duration as timedelta
        duration = end_time - start_time

        # Extract hours, minutes, seconds, and microseconds from timedelta
        # print(f"total seconds {duration.total_seconds()}")
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format duration string
        duration_str = f"{hours:.0f}:{minutes:.0f}:{seconds:.2f}"
        # ffmpeg -ss <start_time> -t <duration> -i <input_file> -c:a copy <output_file>

        return duration_str

    except ValueError as e:
        print(f"File not found: {e}")
        raise ValueError("Invalid time format. Please use 'hh:mm:ss.ss' format.")


def generate_mp3s_with_1_section(dict, riwaya, reciter):
    """_summary_

    Args:
        dict (_type_): _description_
        riwaya (_type_): _description_
        reciter (_type_): _description_
    """
    for element in dict:
        if 1 == element[1]:
            dir, url = get_mp3_paths(riwaya, reciter)
            # Define build folder (create it if it doesn't exist)
            build_folder = os.path.join(dir, element[0][:3])
            os.makedirs(build_folder, exist_ok=True)
            # Define download URL and filename
            url += f"{element[0][:3]}.mp3"
            filename = "001.mp3"  # Customize filename format if needed

            # Download the file
            ## Build the wget command with arguments
            wget_cmd = ["wget", "-O", build_folder + "/" + filename, url]
            ## Run wget as a subprocess
            process = subprocess.run(wget_cmd, capture_output=True)
            ## Check for successful download
            if process.returncode == 0:
                print(f"Downloaded and saved: {filename}")
                # Optional: Decode and print wget output if needed
                # output = process.stdout.decode()
                # print(f"wget output:\n{output}")
            else:
                print(f"Error downloading file: {process.returncode}")

            # Add Metadata
            print(get_thumbnail_and_description("Hafs", element[0], "001"))


def generate_mp3s(diction, riwaya, reciter):
    """_summary_

    Args:
        diction (_type_): _description_
        riwaya (_type_): _description_
        reciter (_type_): _description_
    """
    for element in diction:
        build_dir, mp3_link = get_mp3_paths(riwaya, reciter)
        build_folder = os.path.join(build_dir, element[0][:3])
        json_path = get_json_path(riwaya, reciter, element[0])
        os.makedirs(build_folder, exist_ok=True)
        mp3_link += f"{element[0][:3]}.mp3"

        # Download the MP3 file
        download_command = ["wget", "-O", "temp.mp3", mp3_link]
        subprocess.run(download_command, check=True)

        # Read the JSON file
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                # "./01 - Hafs A'n Assem - حفص عن عاصم/001_Al-Fatiha_الفاتحة/hafs_husari_001.json"
                data = json.load(f)
            # Extract audio information
            json_sections = data["sections"]
        except Exception as e:
            print(f"Error reading JSON file: {e}")

        # Check if sections exist
        if not json_sections:
            print(f"No 'sections' data found in JSON file: {json_path}")
            return
        for section, _ in enumerate(json_sections):
            filename = f"{section + 1:03d}.mp3"
            # Extract first edge for trimming
            start_time = json_sections[section][0]
            end_time = json_sections[section][1]
            # duration    = calculate_duration(start_time, end_time)

            # Construct ffmpeg command (replace with your actual command if needed)
            ffmpeg_command = f'ffmpeg -y -ss {start_time} -to {end_time} -i temp.mp3 -c:a copy "{build_folder}/{filename}"'
            print(f"ffmep cmd : {ffmpeg_command}")
            try:
                # Trim the downloaded MP3 file using ffmpeg
                os.system(ffmpeg_command)
                # subprocess.run(ffmpeg_command, check=True)
                print(f"Trimmed MP3 saved as {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error trimming MP3: {e}")
            except FileNotFoundError as e:
                print(f"File not found: {e}")
        # Delete the downloaded file (optional)
        subprocess.run(["rm", "temp.mp3"], check=True)

def get_mp3_paths(riwaya, reciter):
    """_summary_

    Args:
        riwaya (_type_): _description_
        reciter (_type_): _description_

    Returns:
        _type_: _description_
    """
    base_url = ""
    base_dir = "./build/"
    if "Hafs" == riwaya:
        base_dir += "01-Hafs/"
        if "Husari" == reciter:
            base_dir += "Mahmoud Khalil Al-Hussary/"
            base_url = "https://server13.mp3quran.net/husr/"
        else:
            pass
    elif "Qalon" == riwaya:
        base_dir += "02-Qalon/"
        if "Huthifi" == reciter:
            base_dir += "Ali Alhuthaifi/"
            base_url = "https://server9.mp3quran.net/huthifi_qalon/"
        else:
            pass
    else:
        pass
    return base_dir, base_url


def get_json_path(riwaya, reciter, sura):
    """_summary_

    Args:
        riwaya (_type_): _description_
        reciter (_type_): _description_
        sura (_type_): _description_

    Returns:
        _type_: _description_
    """
    json_path = ""
    prefix = f"_{sura[:3]}.json"
    if "Hafs" == riwaya:
        base_dir = "./01 - Hafs A'n Assem - حفص عن عاصم"
        if "Husari" == reciter:
            json_path = f"{base_dir}/{sura}/hafs_husari{prefix}"
        else:
            pass
    elif "Qalon" == riwaya:
        base_dir = "./02 - Qalon A'n Nafi' - قالون عن نافع"
        if "Huthifi" == reciter:
            json_path = f"{base_dir}/{sura}/qalon_huthifi{prefix}"
        else:
            pass
    else:
        pass
    return json_path


def get_thumbnail_and_description(riwaya, sura, section):
    """Returns the path to the thumbnail and description for a given Quran surah.

    Args:
        riwaya (str): The name of the riwaya (e.g., "Hafs").
        sura (str): The sura number.
        section (str): The section of the sura.

    Returns:
        str: Path to the thumbnail and description. 
    """
    thumbnail = ""
    if "Hafs" == riwaya:
        path = "01 - Hafs A'n Assem - حفص عن عاصم/"
        path += f"{sura}/{section}/{section}/."
        thumbnail = path + "jpg"
        text = path + "txt"
        print(f"text {text}")
    else:
        pass

    try:
        with open(text, "r", encoding="utf-8") as file:
            description = file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {text}")
        description = None
    except PermissionError:
        print(f"Error: Insufficient permissions to access file - {text}")
        description = None
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file content - {text}")
        description = None
    except Exception as e:
        print(f"Error reading file: {text} - {e}")
        description = None

    return thumbnail, description


def is_ffmpeg_installed():
    """Checks if ffmpeg is installed by attempting to run the 'ffmpeg -version' command.

    Returns:
        bool: True if ffmpeg is found, False otherwise.
    """
    try:
        # Run ffmpeg -version with capture_output to get command output
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, check=False
        )
        # Check if the return code is successful (0) and output contains 'ffmpeg version'
        return result.returncode == 0 and "ffmpeg version" in result.stdout
    except subprocess.CalledProcessError:
        # Handle potential errors (e.g., ffmpeg not found)
        return False


def is_eyed3_installed():
    """Checks if eyeD3 is installed using pip show command.

    Returns:
        bool: True if eyeD3 is found, False otherwise.
    """
    try:
        # Run pip show eyed3 with capture_output to get command output
        result = subprocess.run(
            ["eyeD3", "-h"], capture_output=True, text=True, check=False
        )
        # Check if the return code is successful (0) and output contains 'ffmpeg version'
        return result.returncode == 0 and "usage: eyeD3" in result.stdout
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    # Parse command-line arguments
    parser = ArgumentParser(
        description="Generate Trimmed MP3 file based on provided JSON data."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to the JSON file containing audio information.",
        required=False,
    )
    parser.add_argument(
        "-r",
        "--riwaya",
        type=str,
        choices=["Hafs", "Qalon", "Warsh", "all"],
        default="all",
        help="Riwaya [Hafs, Qalon ,Warsh]",
    )
    parser.add_argument(
        "-b", "--bitrate", type=int, default=192, help="MP3 bitrate (default: 192 kbps)"
    )
    parser.add_argument("-q", "--reciter", help="Quran, reciter name", required=False)
    args = parser.parse_args()

    Surat_dict = [
        #["001_Al-Fatiha_الفاتحة", 2],
        #["002_Al-Baqarah_البقرة", 114],
        #["003_Al-Imran_آل عمران", 68],
        #["004_An-Nisaa'_النساء", 73],
        #["005_Al-Ma'idah_المائدة", 60],
        #["006_Al-An'am_الأنعام", 64],
        #["007_Al-A'raf_الأعراف", 62],
        #["008_Al-Anfal_الأنفال", 31],
        #["009_At-Tawbah_التوبة", 51],
        ["010_Yunus_يونس", 32],
        #["011_Hud_هود", 27],
        #["012_Yusuf_يوسف", 31],
        #["013_Ar-Ra'd_الرعد", 15],
        #["014_Ibrahim_إبراهيم", 18],
        #["015_Al-Hijr_الحجر", 16],
        #["016_An-Nahl_النحل", 37],
        #["017_Al-Israa'_الإسراء", 34],
        #["018_Al-Kahf_الكهف", 32],
        #["019_Maryam_مريم", 19],
        #["020_Taha_طه", 27],
        #["021_Al-Anbiya'_الأنبياء", 32],
        ["022_Al-Hajj_الحج", 28],
        #["023_Al-Mu'minoon_المؤمنون", 23],
        #["024_An-Nur_النور", 23],
        #["025_Al-Furqan_الفرقان", 16],
        #["026_Ash-Shu'araa'_الشعراء", 22],
        #["027_An-Naml_النمل", 23],
        #["028_Al-Qasas_القصص", 22],
        #["029_Al-Ankabut_العنكبوت", 24],
        #["030_Ar-Rum_الروم", 17],
        #["031_Luqman_لقمان", 10],
        #["032_As-Sajdah_السجدة", 10],
        #["033_Al-Ahzab_الأحزاب", 29],
        #["034_Saba'_سبأ", 18],
        #["035_Fatir_فاطر", 16],
        #["036_Ya Sin_يس", 13],
        #["037_As-Saffat_الصافات", 20],
        #["038_Saad_ص", 16],
        #["039_Az-Zumar_الزمر", 30],
        #["040_Ghafir_غافر", 25],
        #["041_Fussilat_فصلت", 16],
        #["042_Ash-Shuraa'_الشورى", 20],
        #["043_Az-Zukhruf_الزخرف", 19],
        #["044_Ad-Dukhan_الدخان", 10],
        #["045_Al-Jathiyah_الجاثية", 11],
        #["046_Al-Ahqaf_الأحقاف", 11],
        #["047_Muhammad_محمد", 13],
        #["048_Al-Fath_الفتح", 13],
        #["049_Al-Hujurat_الحجرات", 10],
        #["050_Qaf_ق", 10],
        #["051_Ad-Dhariyat_الذاريات", 12],
        #["052_At-Tur_الطور", 8],
        #["053_An-Najm_النجم", 11],
        #["054_Al-Qamar_القمر", 11],
        #["055_Ar-Rahman_الرحمن", 8],
        #["056_Al-Waqi'ah_الواقعة", 11],
        #["057_Al-Hadid_الحديد", 14],
        #["058_Al-Mujadilah_المجادلة", 7],
        #["059_Al-Hashr_الحشر", 9],
        #["060_Al-Mumtahinah_الممتحنة", 6],
        #["061_As-Saff_الصف", 5],
        #["062_Al-Jumu'ah_الجمعة", 3],
        #["063_Al-Munafiqun_المنافقون", 3],
        #["064_At-Taghabun_التغابن", 7],
        #["065_At-Talaq_الطلاق", 4],
        #["066_At-Tahrim_التحريم", 4],
        #["067_Al-Mulk_الملك", 8],
        #["068_Al-Qalam_القلم", 8],
        #["069_Al-Haqqah_الحاقة", 6],
        #["070_Al-Ma'arij_المعارج", 7],
        #["071_Nuh_نوح", 5],
        #["072_Al-Jinn_الجن", 5],
        #["073_Al-Muzzammil_المزمل", 4],
        #["074_Al-Mudaththir_المدثر", 7],
        ##["075_Al-Qiyama_القيامة", 5],
        ##["076_Al-Insan_الإنسان", 8],
        ##["077_Al-Mursalat_المرسلات", 7],
        #["078_An-Nabaa'_النبأ", 6],
        #["079_An-Nazi'at_النازعات", 6],
        #["080_Abasa_عبس", 4],
        #["081_At-Takwir_التكوير", 3],
        #["082_Infitar_الإنفطار", 4],
        #["083_Al-Mutaffifin_المطففين", 4],
        ["084_Al-Inshiqaq_الانشقاق ", 4],
        #["085_Al-Buruj_البروج", 4],
        #["086_At-Tariq_الطارق", 3],
        #["087_Al-A'la_الأعلى", 3],
        #["088_Al-Ghashiyah_الغاشية", 4],
        #["089_Al-Fajr_الفجر", 3],
        #["090_Al-Balad_البلد", 3],
        #["091_Ash-Shams_الشمس", 2],
        #["092_Al-Layl_الليل", 3],
        #["093_Ad-Duha_الضحى", 2],
        #["094_Ash-Sharh_الشرح", 2],
        #["095_At-Tin_التين", 2],
        #["096_Al-Alaq_العلق", 3],
        #["097_Al-Qadr_القدر", 1],
        #["098_Al-Bayyinah_البينة", 3],
        #["099_Az-Zalzalah_الزلزلة", 1],
        #["100_Al-Adiyat_العاديات", 2],
        #["101_Al-Qariah_القارعة", 3],
        #["102_At-Takathur_التكاثر", 2],
        #["103_Al-Asr_العصر", 1],
        #["104_Al-Humazah_الهمزة", 1],
        #["105_Al-Fil_الفيل", 1],
        #["106_Quraysh_قريش", 1],
        #["107_Al-Ma'un_الماعون", 2],
        #["108_Al-Kawthar_الكوثر", 1],
        #["109_Al-Kafirun_الكافرون", 1],
        #["110_An-Nasr_النصر", 1],
        #["111_Al-Masad_المسد", 1],
        #["112_Al-Ikhlas_الاخلاص", 1],
        #["113_Al-Falaq_الفلق", 1],
        #["114_An-Nas_الناس", 1],
    ]

    # Call the trim function with the provided JSON file path
    # generate_mp3s_with_1_section(Surat_dict, "Hafs", "Husari")
    #generate_mp3s_with_1_section(Surat_dict, "Qalon", "Huthifi")
    #generate_mp3s(Surat_dict, "Hafs", "Husari")
    generate_mp3s(Surat_dict, "Qalon", "Huthifi")
