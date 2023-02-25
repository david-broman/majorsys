

import json
import xmltodict

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
    "k"  : "7",
    "g"  : "7",
    "f"  : "8",
    "v"  : "8",
    "p"  : "9",
    "b"  : "9"
}

# Classes of words
noun = "nn"
verb = "vb"
adjective = "jj"

# Extract a sequence of numbers from a phonetic string
def extract_from_phonetic(phonetic):
    return ''.join([pmap[x] for x in list(phonetic) if x in pmap])

def read_file(file):
    with open(file) as f:
        return f.read()

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
    words = [(x["@value"].replace("|",""),
              x["phonetic"]["@value"] if "phonetic" in x else "",
              x["@class"] if "@class" in x else "")
             for x in data["dictionary"]["word"]]

    # Print statistics
    print("Printing statistics...")
    print("  Total number of words:", len(words))
    def print_stats(text, abbrv, without_phonetic):
        count = [1 for (w,p,c) in words if (without_phonetic or p != "") and c == abbrv]
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
        for (word,phonetic,class_) in words:
          if phonetic != "" and class_ != "":
              number = extract_from_phonetic(phonetic)
              txt_file.write(f'\"{word}\", \"{phonetic}\", {number}\n')
              word_map[word] = (number, class_)

    # Sort into number order
    num_map = {}
    for (word, (num, class_)) in word_map.items():
        if len(num) >= no_of_digits and class_ == noun:
            num2 = num[0:no_of_digits]
            if num2 in num_map:
                num_map[num2].append(word)
            else:
                num_map[num2] = []
    print(len(num_map))

    # Generate html file
    with open("major.html", "w") as txt_file:
        txt_file.write(read_file(html_header))
        txt_file.write(read_file(html_description))
        txt_file.write("Hello")
        for (num, words) in sorted(num_map.items()):
            word_list = ', '.join(words)
            txt_file.write(f'<p><b>Number {num}</b><br>{word_list}<br>')
        txt_file.write(read_file(html_footer))
