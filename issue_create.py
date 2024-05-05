#!/usr/bin/python3
import argparse

def create_issue(sura_name, section_number, riwaya, label):
    """
    Creates an issue on GitHub using the 'gh' command-line tool.

    Args:
    sura_name (str): Name of the Surah.
    section_number (int): Section number within the Surah.
    """
    # Format section number with leading zeros for 3 digits
    section_number_str = f"{section_number:03d}"
    #Sleeping 6Ss to avoid GraphQL: was submitted too quickly (createIssue) error

    ##Implementaitons
    title = f"[Impl.] {sura_name}_{section_number_str}_Audacity"
    body = f"Please create the audio for Surah {sura_name}, Section {section_number}."
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me"]
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},audacity,audio\" -a @me && sleep 6")
    #subprocess.run(command, check=True)

    title = f"[Impl.] {sura_name}_{section_number_str}_Thumbnail"
    body = f"Please create the Thumbnail for Surah {sura_name}, Section {section_number}."
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me"]
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},thumbnail\" -a @me && sleep 6")
    #subprocess.run(command, check=True)

    title = f"[Impl.] {sura_name}_{section_number_str}_Text"
    body = f"Please create the Text for Surah {sura_name}, Section {section_number}."
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me"]
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},text\" -a @me && sleep 6")
    #subprocess.run(command, check=True)

    ##Reviews
    title = f"[Review] {sura_name}_{section_number_str}_Audacity"
    body = f"Please review the audio for Surah {sura_name}, Section {section_number}."
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me"]
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},audacity,audio\" -a @me && sleep 6")
    #subprocess.run(command, check=True)

    title = f"[Review] {sura_name}_{section_number_str}_Thumbnail"
    body = f"Please review the Thumbnail for Surah {sura_name}, Section {section_number}."
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me"]
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},thumbnail\" -a @me && sleep 6")
    #subprocess.run(command, check=True)

    title = f"[Review] {sura_name}_{section_number_str}_Text"
    body = f"Please review the Text for Surah {sura_name}, Section {section_number}."
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me"]
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},text\" -a @me && sleep 6")
    #subprocess.run(command, check=True)

    #print(f"Successfully created issue for Surah {sura_name}, Section {section_number}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create GitHub issues for Quran review")
    parser.add_argument("sura_name", help="Name of the Surah")
    parser.add_argument("num_sections", type=int, help="Total number of sections in the Surah")
    parser.add_argument("riwaya", help="Riwaya to assign to the issues")
    parser.add_argument("label", help="label to assign to the issues")
    args = parser.parse_args()

    for sec_num in range(1, args.num_sections + 1):
        create_issue(args.sura_name, sec_num, args.riwaya ,args.label)
