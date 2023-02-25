

import json
import xmltodict

with open("folkets_sv_en_public.xml") as xml_file:

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

    # Save words with phonetics in a text file
    print("Save word file with phonetics...")
    with open("words.txt", "w") as txt_file:
        for w in words:
            if "@class" in w and "phonetic" in w and w["@class"] == "nn":
                word = w["@value"]
                phonetic = w["phonetic"]["@value"]
                txt_file.write(f'\"{word}\", \"{phonetic}\"\n')
