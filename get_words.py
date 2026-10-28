"""
AUTHOR: Ebenezer Jiang
Version 1.3.34

DESCRIPTION: 
    Stores all words in the chosen dictionary to "all_words" list. 

HOW IT WORKS:
    First, "all_words" is a list. If NLTK is used, then we just import the corpus.words.words() list. However,
    important words are missing from NLTK, so a local dictionary is also offered. The local dictionary is 
    a text file with one word per line. The words are taken from ENABLE (https://www.wordgamedictionary.com/enable/download/enable.txt). 
    We read each line and store it as an element in "all_words".

    A Trie of all possible words is created using maps of maps (logic is explained in depth in that section).

    And finally, a function (check_word) is offered (used in Boggle.py) that checks whether a substring could 
    still potentially become a word one day AND whether it is a valid Boggle word.
"""
"""
# Using NLTK built-in dictionary
import nltk

# Download the words corpus from NLTK if it hasn't been downloaded already.
nltk.download('words')
# Load the words corpus into a list for quick lookup.
all_words = nltk.corpus.words.words() # list

"""
# Using Local dictionary all_words_dictionary.txt
ALL_WORDS = []
with open('./all_words_dictionary.txt', 'r') as file:
    for line in file.readlines():
        ALL_WORDS.append(line.strip())

### TRIE ###
def convert_to_map_trie(all_words: list[str]) -> None:
    root = {}
    for word in all_words: # all_words must be a List
        # "copy" the main map so we can nest and travel
        node = root 
        for char in word.lower():
            # For each character in word, see if that character already exists as a key in the current level. 
            # If it doesn't create a new value of {} at that key. Either way, move into this new key to keep nesting maps: "node = ..."
            node = node.setdefault(char, {})
        node["*"] = True # this is a word
    return root


print("[TRIE MAP SET UP] Converting all words to TRIE map")
# This is where all the characters for the word maps will be stored
all_words_prefix_map = convert_to_map_trie(ALL_WORDS) # this is a map of maps, where each level is a character in the word. The "*" key indicates that this is a word.
print(f"[TRIE MAP SET UP] Successfully coverted {len(ALL_WORDS)} words.")

## AN OVERLY-DETAILED EXPLANATION OF WORD-CHECKING LOGIC:
# Check if a substring exists (aka this could potentially be a word)
# NOTE: This is the logic used in BoogleBoard.store_combinations to determine whether or not to
#       continue with checking a path or not. If this function returns false, that means given the
#       current prefix/substring, no matter what future characters you add, there is no possible word 
#       in the dictionary. Example: "zxxq", if this is the substring/prefix, abort this path...no
#       English word start with "zxxq"......make sense?
# Words will be stored in levels...
# When referring to "levels", this is what the programmer means:
# LEVEL 1: {      c        }   
#                / \
# LEVEL 2: {    a,  o      }
#              / \   \
# LEVEL 3: {  r,  n,  d    }
#                      \
# LEVEL 4: {            e  } 
# To check whether "car" exists, you scan the first level for "c" (does this exist in key?). If this passes, you continue.
def check_word(prefix: str, root = all_words_prefix_map) -> dict[str, bool]:
    current_level = root #
    for index, char in enumerate(prefix.lower()): # lower as a precaution, since the trie map is all lowercase
        if not char in current_level.keys(): # is this char in this level?
            return {
                "substring_potential" : False
            }

        # Passed...so far...next level!
        current_level = current_level[char]

        # last term
        if index == len(prefix) - 1: # if this is the last character in the prefix, check if this is a word
            if "*" in current_level.keys(): # if this is a word, return True
                return {
                    "substring_potential" : True,
                    "is_word" : True
                }
            else: 
                return {
                    "substring_potential" : True,
                    "is_word" : False
                }
    # Complete! You exist!

def boggle_verified(word: str) -> bool:
    if len(word) >= 3:
        return True
    return False

"""a = convert_to_map_trie(["car", "cab"])
print(a)
print(check_word("car",a))"""