# Simple scripts that extracts numbers for Swedish words, according
# to the mnemonic major system
# By David Broman (C) Copyright 2023. MIT License.

import json
import xmltodict
import csv

# Files
database = "folkets_sv_en_public.xml"
html_header = "html/header.html"
html_description = "html/description.html"
html_footer = "html/footer.html"
no_of_digits = 3

# Mapping of phonetic IPA symbols to numbers. Note that focus is on Swedish sounds.
pmap = {
    "s"  : "0",
    "t"  : "1",
    "d"  : "1",
    "n"  : "2",
    "@"  : "2",
    "m"  : "3",
    "r"  : "4",
    "l"  : "5",
    "j"  : "6",
    "$"  : "6",
    "c"  : "6",
    "k"  : "7",
    "g"  : "7",
    "f"  : "8",
    "v"  : "8",
    "p"  : "9",
    "b"  : "9"
}

# Extract a sequence of numbers from a phonetic string
def extract_from_phonetic(phonetic):
    return ''.join([pmap[x] for x in list(phonetic) if x in pmap])

# Word list mapping. Note how the order matters.
wlist = [
    ("06", ["zige"]),
    ("07", ["isky"]),
    ("41", ["rld"]),
    ("22", ["egn"]),
    ("427", ["rng"]),
    ("70", ["x", "acc"]),
    ("27", ["nk"]),
    ("56", ["alg", "älg"]),
    ("46", ["org", "ärg"]),
    ("207", ["nsk"]),
    ("26", ["ngi", "ange"]),
    ("22", ["ägn", "agn", "ign"]),
    ("47", ["rk"]),
    ("7", ["ake", "eke", "ike", "oke", "uke", "yke", "åke", "äke", "öke",
           "aki", "eki", "iki", "oki", "uki", "yki", "åki", "äki", "öki",
           "age", "ege", "ige", "oge", "uge", "yge", "åge", "äge", "öge",
           "agi", "ogi", "ugi", "ågi"]),
    ("6", ["jj", "j", "skj", "sky", "ski", "skö", "sj", "sch",
           "ke", "ki", "ky", "kä", "kö",
           "ge", "gi", "gy", "gä", "gö", "gj",
           "tj", "lju", "ske", "sio", "skä",
           "ch", "tio"]),
    ("7", ["ck", "kk", "k", "K", "gg", "g", "G", "ca", "co", "cu", "cå"]),
    ("0", ["ss", "s", "S", "zz", "z", "s", "c"]),
    ("1", ["tt", "t", "T", "dd", "d", "D"]),
    ("2", ["ng", "nn", "n", "N"]),
    ("3", ["mm", "m", "M"]),
    ("4", ["rr", "r"]),
    ("5", ["ll", "l", "L"]),
    ("8", ["ff", "f", "F", "W", "w", "ww", "vv", "v", "V"]),
    ("9", ["pp", "p", "P", "bb", "b", "B"])
]


# Extract number from word using the wlist
def extract_from_word(word):
    word = " " + word
    num = ""
    i = 0
    while(i < len(word)):
        next = False
        for (k, lst) in wlist:
            if next:
                break
            for l in lst:
                if word[i:i+len(l)] == l:
                    num += k
                    i += len(l)
                    next = True
                    break
        if not next:
            i += 1
    return num

# Classes of words'
noun = "nn"
verb = "vb"
adjective = "jj"

# Helper for reading a file
def read_file(file):
    with open(file) as f:
        return f.read()

# Helper, check if ends with one of the alternatives
def my_endswith(str, lst):
    for x in lst:
        if str.endswith(x):
            return True
    return False


# Open the free Swedish database with words
with open(database) as xml_file:

    # Read, parse, and convert the lexicon to a dictionary
    print("Parsing XML file...")
    data = xmltodict.parse(xml_file.read())

    # Save it as JSON for easier analysis
    print("Saving JSON file with complete dictionary...")
    with open("folkets.json", "w") as json_file:
        json_file.write(json.dumps(data, indent=4))

    # Extracts words
    print("Extracts triple (word, phonetic, class)...")
    words = {x["@value"].replace("|",""):
              (x["phonetic"]["@value"] if "phonetic" in x else "",
               x["@class"] if "@class" in x else "")
             for x in data["dictionary"]["word"]}

    # Patch words
    # Format: word,phonetic,class,number
    # If a number is given, it is taken as the truth
    # If class = 'remove', then the word is removed instead of added.
    with open("patch.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for r in csv_reader:
            if r[2] == "remove":
                del words[r[0]]
            words[r[0]] = (r[1],r[2])

    # Remove strings with space from words
    for w in [w for (w,_) in words.items() if ' ' in w]:
        del words[w]

    # Clean up phonetic strings wit (et.
    for (w,(p,c)) in words.items():
        p = p[0:p.find("el.") if p.find("el.") >= 0 else len(p)]
        p = p.replace(" ", "").replace("(", "")
        words[w] = (p,c)
        
    # Print statistics
    print("Printing statistics...")
    print("  Total number of words:", len(words))
    def print_stats(text, abbrv, without_phonetic):
        count = [1 for (w,(p,c)) in words.items()
                 if (without_phonetic or p != "") and c == abbrv]
        print(text, len(count))
    print_stats("  Total number of nouns:", "nn", True)
    print_stats("  Number of nouns with phonetic:", "nn", False)
    print_stats("  Total number of verbs:", "vb", True)
    print_stats("  Number of verbs with phonetic:", "vb", False)
    print_stats("  Total number of adjectives:", "jj", True)
    print_stats("  Number of adjectives with phonetic:", "jj", False)

    # Extract numbers, classes, and words. Avoid word duplicates
    word_map = {}
    print("Generate numbers according to the major system...")
    with open("words.txt", "w") as txt_file:
        no_ok = 0
        no_error = 0
        for (word,(phonetic,class_)) in words.items():
          if phonetic != "":
              number_p = extract_from_phonetic(phonetic)
              txt_file.write(f'\"{word}\", \"{phonetic}\", {number_p}\n')
              word_map[word] = (number_p, class_)
              number_w = extract_from_word(word)
              # Fix strange ending of phonetic
              if number_p != number_w:
                  if (my_endswith(phonetic, ["er","ar","a:r", "e:r",
                                             "å:r", "o:r", "ir", "i:r"])
                      and number_w == number_p[0:len(number_p)-1]):
                    number_p = number_p[0:len(number_p)-1]

              if number_p == number_w:
                  no_ok += 1
              else:
                  no_error += 1
                  print(f'word: \"{word}\", phonetic: \"{phonetic}\", ')
                  print(f'number_w: {number_w}, number_p: {number_p}\n')

        # Summarize errors when extracting from words
        print(f'  Number of tests for number extraction: {no_ok + no_error}')
        print(f'  Number of errors for number extraction: {no_error}')

    # Sort into number order
    num_map = {}
    for (word, (num, class_)) in word_map.items():
        if len(num) >= no_of_digits and class_ == noun:
            num2 = num[0:no_of_digits]
            if num2 in num_map:
                num_map[num2].append(word)
            else:
                num_map[num2] = []
    print("  Total number of generated numbers:", len(num_map))

    # Generate html file
    with open("major.html", "w") as txt_file:
        txt_file.write(read_file(html_header))
        txt_file.write(read_file(html_description))
        txt_file.write("Hello")
        for (num, words) in sorted(num_map.items()):
            word_list = ', '.join(words)
            txt_file.write(f'<p><b>Number {num}</b><br>{word_list}<br>')
        txt_file.write(read_file(html_footer))
