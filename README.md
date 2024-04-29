# Latin-Vocab-Quizzer
A command-line app to quiz yourself on latin vocabulary. Written in Python.

# Getting Started
```
git clone https://github.com/Red91K/Latin-Vocab-Quizzer.git
cd Latin-Vocab-Quizzer
python3 latin_quizzer.py
```

## Creating Vocabulary Lists
- Latin-Vocab-Quizzer works by quizzing you on lists of latin vocabulary
- To create a new vocabulary list, create a .txt file in the `vocab_lists` directory and fill it with vocab words
  - separate each part of the word (principle parts for verbs, nominative sg & genitive sg for nouns, etc) with commas.
  - do the same for the definitions of the word
  - Use a dash (-) to separate the parts of the word from the definition.
  - The formatted word should look something like this: `ago, agere, egi, actus, 1 - to do, lead, drive, act`
  - `ago, agere, egi, actus, 1` are the parts of the word
  - `to do, lead, drive, act` are the definitions of the word
 
