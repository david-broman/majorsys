

import json
import xmltodict

# Files
database = "folkets_sv_en_public.xml"
html_header = "header.html"
html_description = "description.html"
html_footer = "footer.html"

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

# Open the free Swedish database with words
with open(database) as xml_file:

    # Read, parse, and convert the lexicon to a dictionary
    print("Parsing XML file...")
    data = xmltodict.parse(xml_file.read())
    words = data["dictionary"]["word"]

    # Save it as JSON for easier analysis
    print("Saving JSON file with complete dictionary...")
    with open("folkets.json", "w") as json_file:
        json_file.write(json.dumps(data, indent=4))

    # Print statistics
    print("Printing statistics...")
    print("  Total number of words:", len(words))
    def print_stats(text, abbrv, without_phonetic):
        count = [1 for w in words if "@class" in w and
                 (without_phonetic or "phonetic" in w) and w["@class"] == abbrv]
        print(text, len(count))
    print_stats("  Total number of nouns:", "nn", True)
    print_stats("  Number of nouns with phonetic:", "nn", False)
    print_stats("  Total number of verbs:", "vb", True)
    print_stats("  Number of verbs with phonetic:", "vb", False)
    print_stats("  Total number of adjectives:", "jj", True)
    print_stats("  Number of adjectives with phonetic:", "jj", False)

    # Extract numbers, classes, and words. Avoid duplicates
    word_map = {}
    print("Save word file with phonetics...")
    with open("words.txt", "w") as txt_file:
        for w in words:
            if "@class" in w and "phonetic" in w:
                word = w["@value"]
                phonetic = w["phonetic"]["@value"]
                number = extract_from_phonetic(phonetic)
                txt_file.write(f'\"{word}\", \"{phonetic}\", {number}\n')
                word_map[word] = (number, w["@class"])

    # Generate html file
    print(word_map)
