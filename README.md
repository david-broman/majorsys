# Mnemonic major system

This repo contains a simple script that extracts phonetic words in Swedish from the database available from [Folkets lexikon](https://folkets-lexikon.csc.kth.se/folkets/). It is also possible to extend the output with additional words.

You must have `Python` version 3 and the package `xmltodict` installed.

To run the script, use e.g., the command:

```
  python3 generate.py major.html 3 false noun "Test"
```

The first argument is the output file. The second argument states the number of digits that should be used. If the third argument is true, the generated file will also include words that have more digits. The fourth argument states the word type (three options: `noun`, `verb`, and `adjective`). The last argument is the title of the generated HTML file.

Note that you need to download the file `folkets_sv_en_public.xml` from [this location](href="https://folkets-lexikon.csc.kth.se/folkets/folkets_en_sv_public.xml).

You can also extend the generated words by adding items in the file `patch.csv`. Each line contains one-word entry in the format `"word, phonetic, class, number"`. A word must always be given, but the phonetic number is optional. The class should be `nn` for a noun, `vb` for a verb, and `jj` for an adjective. If the class is `remove`, then the word will not be used, even if it existed in the database. Finally, if the number is given, then this word will be used in the output with the specific number.

You can find already generated lists [on this page](https://people.kth.se/~dbro/majorsys.html). If you use this script, please add a link to the page below or just credits.
