"""
AUTHOR: Ebenezer Jiang
Version 1.3.0

DESCRIPTION: 
    Creates a class for Boggle boards, offering methods to generate, store, and solve the Boggle boards.

HOW IT WORKS:
    The BoggleBoard class represents a Boggle board and provides methods to generate the board, print it, 
    and check combinations of letters along paths. Whenever a valid word is found, it is appended to the "words_found" list. 

    The program uses recursion to explore all possible paths on the Boggle board. Valid words are stored in the "words_found" list. 
    
    A grammatical approach is implemented to optimize memory. Each route is monitered based on whether words in 
    "all_words" start with the current substring. If there is no word that begins with that substring, that means 
    the current path can be terminated and forgotten. This logic is found in get_words.py, which uses a Trie approach
    to eliminate impossible substrings/prefixes.

    NOTE: In this program, the term "combination" is used to refer to the substring formed by various steps. For
          example, in this boggle board:
          a  b  c     00 01 02
          d  e  f --> 10 11 12
          g  h  i     20 21 22
          The path 00,01,11,22 would have a combination of "abei"
          The path 11,20,21 would have a combination of "egh"

DISCLAIMER:
  * The maximum Boggle Board size is 9, otherwise the logic fails, since indexes and paths are stored on a 
    2-digit base-10 system (e.g. the position "01" represents the 0th row and the 1st column), thus the max
    position is "99". This is fixable if one updated the code to expend paths to a four-digit position string
    (10th row + 24th column = pos "1024")
"""

import string
import random
import time

from get_words import all_words, prefix_can_still_exist

all_letters = list(string.ascii_lowercase)
all_vowels = ["a", "e", "i", "o", "u"] # lowercase

# Default size
BOARD_SIZE = 4 # Maximum Boggle Board Size is 9, otherwise logic fails

class BoggleBoard():
    def __init__(self, size = BOARD_SIZE, inputed_board = None):
        self.size = size # boards will have dimensions of "size" x "size"
        self.board = inputed_board if inputed_board else self.generate() # must be a valid board dictionary

        # Store all words found on the board
        self.words_found = []

        # Count the number of iterations
        self.iteration_count = 0

    # This "randomly" picks a letter from the letters list (includes vowels) or returns a vowel (potentially with higher weight)
    # @param weight_vowels (bool): Whether or not to weight the vowels
    # @return str: A randomly selected letter
    def pick_letters(self, weight_vowels = True) -> str:
        if weight_vowels and random.randint(0, 100) <= 15: # give a higher chance of a vowel
            return all_vowels[random.randint(0, len(all_vowels) - 1)]
        else:
            return all_letters[random.randint(0, len(all_letters) - 1)]

    # This generates a random board with a size of "self.size"
    # @return dict: A dictionary representing the generated Boggle board with a size of "self.size" x "self.size"
    def generate(self) -> dict:
        # generate a random boggle board
        board = {}
        for i in range(self.size): # row
            for j in range(self.size): # column
                """
                Map the board based off of row # and column #
                This will be 0-indexed
                # For example: 00 = 0th row, 0th column
                #              23 = 2nd row, 3rd column
                # """
                board[f"{i}{j}"] = self.pick_letters(True)
        return board

    # This prints the boggle board in a legible manner
    # @return None
    def print_board(self) -> None:
        for i in range(self.size): # row
            for j in range(self.size): # column
                print(self.board[f"{i}{j}"], end=" ")
            print()

    # Given a (known to be valid) path, we check if this is a word and attempt to continue paths
    #
    # @param path (str): A comma-separated string representing the path of indices on the board (e.g "00,01,02,12")
    # @param word (str): The word associated with the path
    # @return None
    def check_combinations(self, path:list, word:str, horz_inc:int = 0, vert_inc:int = 0) -> None:
        self.iteration_count += 1#

        last_index = path[-1] 
        next_index = f"{int(last_index[0]) + horz_inc}{int(last_index[1]) + vert_inc}"

        if next_index not in self.board.keys():  
            return

        # Passed Level 1 Check, create new word
        new_path = path + [next_index] # list
        new_word = word + self.board[next_index] # str

        ### PREFIX CHECKER ###
        if next_index in path:
            return

        if prefix_can_still_exist(new_word) == False:
            return

        if new_word in all_words:
            # If it is true, then add this to the "words_found" list
            print("WORD FOUND - " + new_word)
            self.words_found.append(new_word) 

        self.check_surroundings(new_path, new_word)

    def check_surroundings(self, new_path, new_word):
        # (-1, -1) (0, -1) (+1,-1)
        # (-1,  0) CURRENT (+1, 0)
        # (-1, +1) (0, +1) (+1 +1)
        self.check_combinations(new_path, new_word,-1, -1)
        self.check_combinations(new_path, new_word,0, -1)
        self.check_combinations(new_path, new_word,1, -1)

        self.check_combinations(new_path, new_word,-1, 0)
        # DON'T TRY YOURSELF! NO +0, +0
        self.check_combinations(new_path, new_word,1, 0)

        self.check_combinations(new_path, new_word,-1, 1)
        self.check_combinations(new_path, new_word,0, 1)
        self.check_combinations(new_path, new_word,1, 1) 
    
    # Solves the Boggle board by exploring all possible paths and storing valid words.
    # After solving, the method prints out the board as well as all the valid Boggle words (length <= 3).
    # @return None
    def solve(self, give_information = True) -> None:
        # Give runtime 
        if give_information:
            start = time.time()

        ### Self-explanatory...
        for path in self.board.keys():
            self.check_surroundings([path], self.board[path]) 

        ### Self-explanatory...
        print("\n\n BOARD: ")
        self.print_board()

        ### Self-explanatory...
        print("\n ALL  VALID  BOGGLE  WORDS (length >= 3): ")
        # remove duplicates and makes sure word lengths >= 3
        self.words_found = [i for i in set(self.words_found) if len(i) >= 3]
        self.words_found.sort() # Sort alphabetically
        print(", ".join(self.words_found)) # Print out all words
        print("\n")

        # Give runtime
        if give_information:
            end = time.time()
            print(f"Runtime: {round(end - start, 2)} seconds")
            print("Total checks: ", self.iteration_count)

preset = {
    "00":"z", "01":"g", "02":"z", "03":"z",
    "10":"n", "11":"z", "12":"d", "13":"z", 
    "20":"z", "21":"i", "22":"z", "23":"o", 
    "30":"z", "31":"z", "32":"z", "33":"c", 
}

# # # # #
def __main__():
    # Initialize new BoggleBoard
    board = BoggleBoard(4, preset) 
    
    print("BOGGLE BOARD:")
    board.print_board()

    #input("\n\nPress [ENTER] to compute answers...")
    board.solve()

if __name__ == "__main__":
    __main__()