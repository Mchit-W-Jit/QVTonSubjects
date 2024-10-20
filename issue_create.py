#!/usr/bin/python3

"""
    Helps massively creating issues
"""

import argparse

def create_issue(sura_name, section_number, riwaya, receiter, label, milestone):
    """
    Creates an issue on GitHub using the 'gh' command-line tool.

    Args:
    sura_name (str): Name of the Surah.
    section_number (int): Section number within the Surah.
    """

    # Format section number with leading zeros for 3 digits
    section_number_str = f"{section_number:03d}"
    # url to working directory for a specific task
    url = "https://github.com/Mchit-W-Jit/QVTonSubjects/tree/dev/"
    if riwaya == 'Hafs':
        url += f"01%20-%20Hafs%20A'n%20Assem%20-%20حفص%20عن%20عاصم/{label}/{section_number_str}"
    elif riwaya == 'Qalon':
        url += f"02%20-%20Qalon%20A'n%20Nafi'%20-%20%D9%82%D8%A7%D9%84%D9%88%D9%86%20%D8%B9%D9%86%20%D9%86%D8%A7%D9%81%D8%B9/{label}/{section_number_str}"
    else:
        pass
        
    title = f"[Impl.] {sura_name}_{section_number_str}_Audio"
    body = f"Please create the audio for [Surah {sura_name}, Section {section_number}]({url})"
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me -m \"{milestone}\""]
    #subprocess.run(command, check=True)
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},{receiter},audacity,audio\" -a @me -m \"{milestone}\" ; sleep 25")

    title = f"[Impl.] {sura_name}_{section_number_str}_Screenshot"
    body = f"Please create the Thumbnail for [Surah {sura_name}, Section {section_number}]({url})"
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me -m \"{milestone}\""]
    #subprocess.run(command, check=True)
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},{receiter},thumbnail,screenshot\" -a @me -m \"{milestone}\" ; sleep 25")

    if ("Hafs" == riwaya):
        title = f"[Impl.] {sura_name}_{section_number_str}_Text"
        body = f"Please create the Text for [Surah {sura_name}, Section {section_number}]({url})"
        #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me -m \"{milestone}\""]
        #subprocess.run(command, check=True)
        print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},{receiter},text\" -a @me -m \"{milestone}\" ; sleep 25")
    else:
        pass

    ##Reviews
    title = f"[Review] {sura_name}_{section_number_str}_Audio"
    body = f"Please review the audio for [Surah {sura_name}, Section {section_number}]({url})"
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me -m \"{milestone}\""]
    #subprocess.run(command, check=True)
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},{receiter},audacity,audio\" -a @me -m \"{milestone}\" ; sleep 25")

    title = f"[Review] {sura_name}_{section_number_str}_Screenshot"
    body = f"Please review the Thumbnail for [Surah {sura_name}, Section {section_number}]({url}) [{sura_name}_{section_number_str}_Screenshot]({url}/{section_number_str}.jpg?raw=true)"
    #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me -m \"{milestone}\""]
    #subprocess.run(command, check=True)
    print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},{receiter},thumbnail,screenshot\" -a @me -m \"{milestone}\" ; sleep 25")

    if ("Hafs" == riwaya):
        title = f"[Review] {sura_name}_{section_number_str}_Text"
        body = f"Please review the Text for [Surah {sura_name}, Section {section_number}]({url})"
        #command = ["gh", "issue", "create", "-t", title, "-b", body, "-l", label, "-a @me -m \"{milestone}\""]
        #subprocess.run(command, check=True)
        print(f"gh issue create -t \"{title}\" -b \"{body}\" -l \"{label},{riwaya},{receiter},text\" -a @me -m \"{milestone}\" ; sleep 25")
    else:
        pass

    #print(f"Successfully created issue for Surah {sura_name}, Section {section_number}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create GitHub issues for Quran review")
    parser.add_argument("sura_name", help="Name of the Surah")
    parser.add_argument("num_sections", type=int, help="Total number of sections in the Surah")
    parser.add_argument("riwaya", help="Riwaya to assign to the issues")
    parser.add_argument("receiter", help="receiter to assign to the issues")
    parser.add_argument("label", help="label to assign to the issues")
    parser.add_argument("milestone", help="milestone to assign to the issues")
    args = parser.parse_args()

    for sec_num in range(1, args.num_sections + 1):
        create_issue(args.sura_name, sec_num, args.riwaya, args.receiter ,args.label,args.milestone)
