"""
AUTHOR: Ebenezer Jiang
Version 1.3.0

DESCRIPTION: 
    Stores all words in the chosen dictionary to "all_words" list. 

HOW IT WORKS:
    First, "all_words" is a list. If NLTK is used, then we just import the corpus.words.words() list. However,
    important words are missing from NLTK, so a local dictionary is also offered. The local dictionary is 
    a text file with one word per line. The words are taken from ENABLE (https://www.wordgamedictionary.com/enable/download/enable.txt). 
    We read each line and store it as an element in "all_words".

    Next, a Trie is created from the list using maps of maps (logic is explained in depth in that section).

    And finally, a function is offered (used in Boggle.py) that checks whether a substring could still potentially 
    become a word one day...
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
all_words = []
with open('./all_words_dictionary.txt', 'r') as file:
    for line in file.readlines():
        all_words.append(line.strip())


### TRIE ###
print("[TRIE MAP SET UP] Converting all words to TRIE map")
# This is where all the characters for the word maps will be stored
all_words_prefix_map = {}
for word in all_words: # all_words must be a List
    # "copy" the main map so we can nest and travel
    node = all_words_prefix_map 
    for char in word.lower():
        # For each character in word, see if that character already exists as a key in the current level. 
        # If it doesn't create a new value of {} at that key. Either way, move into this new key to keep nesting maps: "node = ..."
        node = node.setdefault(char, {})
    node["*"] = True # this is a word

print(f"[TRIE MAP SET UP] Successfully coverted {len(all_words)} words.")

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
def prefix_can_still_exist(prefix: str) -> bool:
    current_level = all_words_prefix_map #
    for char in prefix.lower(): # lower as a precaution, since the trie map is all lowercase
        if not char in current_level.keys(): # is this char in this level?
            return False

        # Passed...so far...next level!
        current_level = current_level[char]
    # Complete! You exist!
    return True