"""
AUTHOR: Ebenezer Jiang

DESCRIPTION: 
    Creates a class for Boggle boards, offering methods to generate, store, and solve the Boggle boards.

HOW IT WORKS:
    The BoggleBoard class represents a Boggle board and provides methods to generate the board, print it, 
    and store combinations of letters along paths. 
    The "combinations" dictionary keeps track of all possible paths and their corresponding words. Whenever a
    valid word is found, it is appended to the "words_found" list. 
    
    The "iteration_count" counter tracks the number of iterations performed during the search.

    The program uses recursion to explore all possible paths on the Boggle board, storing the combinations 
    and checking for valid words. Valid words are stored in the "words_found" list. 
    
    A grammatical approach is implemented to optimize memory. Each route is monitered based on whether words in 
    "all_words" start with the current substring. If there is no word that begins with that substring, that means 
    the current path can be terminated and forgotten.

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

import nltk

all_letters = list(string.ascii_lowercase)
all_vowels = ["a", "e", "i", "o", "u"] # lowercase

# Download the words corpus from NLTK if it hasn't been downloaded already.
nltk.download('words')
# Load the words corpus into a list for quick lookup.
all_words = nltk.corpus.words.words()


# Default size
BOARD_SIZE = 5 # Maximum Boggle Board Size is 9, otherwise logic fails

# Class representing a Boggle board.
# @Attributes:
#     (int) size : The dimension of the board (size x size).
#     (dict) board : A dictionary representing the board, with keys as "row-col" and values as letter characters (e.g., "00", "01").
#     (dict) combinations : A dictionary storing all possible paths and their corresponding words.
#     (list) words_found : A list of all valid words found on the board.
#     (int) iteration_count : The number of iterations performed during search.
# @Methods:
#     pick_letters(weight_vowels: bool = True) -> str: Returns a random letter, optionally weighted towards vowels.
#     generate() -> dict: Generates a random Boggle board with a size of "self.size" x "self.size"
#     print_board() -> None: Prints the current Boggle board.
#     store_combinations(path: str) -> None: Stores the combination of letters along the given path.

class BoggleBoard:
    def __init__(self, size = BOARD_SIZE, inputed_board = None):
        self.size = size # boards will have dimensions of "size" x "size"
        self.board = inputed_board if inputed_board else self.generate() # must be a {}

        # Combinations will store paths:
        #      PATHS           TEXT
        # { "00,01,02,12" : text: "abcd" } # path (list) to a string
        self.combinations = {}
        # This will store all the possible routes from 1 square, so future testing is unnecessary 
        # { "00": ["00,01", "00,10"...] }
        #self.paths_from_start = {}

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

    # Given a starting path, this method will store the substrings in the "self.combinations" dictionary (if it doesn't yet exist).
    # Then, the program will test possible other paths (by moving to diagonal/adjacent squares), handing off the path to the 
    # "self.test_new_path" method.
    #
    # @param path (str): A comma-separated string representing the path of indices on the board (e.g "00,01,02,12")
    # @return None
    def store_combinations(self, path:str) -> None:
        self.iteration_count += 1
        if path == None:
            print("Invalid path. Abort... NONE TYPE ")
            return
        
        path_as_list = path.split(",") # Path is a string, this is List form

        last_index = path_as_list[-1] # STRING! last added index
            
        # Does this path not yet exist in combinations?
        if path not in self.combinations.keys():
            # Only one index in the path:
            if len(path_as_list) == 1:
                # Add to combinations map as the single letter
                self.combinations[path] = self.board[path]
            # More than one index in the path:
            else:
                path_of_all_but_last = path[:-3] # literally just: ",".join(path_as_list[:-1])

                previous_combo = self.combinations[path_of_all_but_last] # Substring of path before adding new letter/step
                last_term = self.board[path_as_list[-1]] # This is the new letter/step

                # Store new combination in "self.combinations"
                self.combinations[path] = previous_combo + last_term 
        # If this path already exists in combinations, just forget about it...
        else:
            return

        # DEBUG
        #print("Path: " + path.ljust(50) + " || Word?: " + self.combinations[path].ljust(16) + " || ITERATIONS: " + str(self.iteration_count))

        ### PREFIX CHECKER ###
        # If there is no word in the English dictionary that start with this combination, why keep going?
        if len([word for word in all_words if word.lower().startswith(self.combinations[path])]) == 0:
            # DEBUG
            #print("No English word starts with: " + self.combinations[path])
            return

        #CHECK WORD!
        potential_word = self.combinations[path]
        # Check if this word appears in "all_words", which theoretically includes...all words...
        if potential_word.lower() in all_words:
            # If it is true, then add this to the "words_found" list
            self.words_found.append(potential_word) 
            print("Word found! " + potential_word.ljust(15) + " | PATH: " + path.ljust(20) + " | ITERATION: #" + str(self.iteration_count))#| PATHS_SEARCHED: " + str(self.combinations.keys()))
       
        # After storing everything, now it's time to check the surroundings...
        # Not really "storing combinations" but hey, go the extra mile...(Matt. 5:41)

        # (-1, -1) (0, -1) (+1,-1)
        # (-1,  0) CURRENT (+1, 0)
        # (-1, +1) (0, +1) (+1 +1)

        self.test_new_path(path_as_list, -1, -1)
        self.test_new_path(path_as_list, 0, -1)
        self.test_new_path(path_as_list, 1, -1)

        self.test_new_path(path_as_list, -1, 0)
        # DON'T TRY YOURSELF! NO +0, +0
        self.test_new_path(path_as_list, 1, 0)

        self.test_new_path(path_as_list, -1, 1)
        self.test_new_path(path_as_list, 0, 1)
        self.test_new_path(path_as_list, 1, 1)       

    # Generates a new path by adding a neighboring cell to the existing path.
    # @param old_path_list (list): The list-form of the current path (e.g. Path = "01,02,21" -> ["01", "02", "21"])
    # @param horz_inc (int): The horizontal increment to the last cell (-1, 0, +1)
    # @param vert_inc (int): The  vertical  increment to the last cell (-1, 0, +1)
    # @return None
    def test_new_path(self, old_path_list:list, horz_inc:int, vert_inc:int) -> None:
        # old_path_list should be like ["00", "10", "11"]
        last_index = old_path_list[-1] # STRING! last added index

        # Since last_index is stored as a string (e.g. "21"), we must separate into integers to update it:
        new_row_num = str(int(last_index[0]) + horz_inc) #(+1, +0, or -1) to the last row index
        new_col_num = str(int(last_index[1]) + vert_inc) #(+1, +0, or -1) to the last column index
        new_last_index = f"{new_row_num}{new_col_num}"   # This is the new last index

        # Do you like it?
        # Let's find out...

        # If the last index does not exist on the board; it's out of bounds...forget it...
        if new_last_index not in self.board.keys():
            return

        # If this sqaure was already visited, you can't visit again...forget it...
        if new_last_index in old_path_list:
            return

        # # #
        # Create new path [00, 01, 02] + JUST ADDED "03" (new_last_index)
        test_new_path = ",".join(old_path_list) + "," + new_last_index
        # If you already tried this path, you can't visit again...
        if test_new_path in self.combinations.keys():
            return

        # You passed! This is a valid path worth storing a combination for...
        self.store_combinations(test_new_path)
    
    # Solves the Boggle board by exploring all possible paths and storing valid words.
    # After solving, the method prints out the board as well as all the valid Boggle words (length <= 3).
    # @return None
    def solve(self) -> None:
        ### Self-explanatory...
        for path in self.board.keys():
            self.store_combinations(path)

        ### Self-explanatory...
        print("\n\n BOARD: ")
        self.print_board()

        ### Self-explanatory...
        print("\n ALL  VALID  BOGGLE  WORDS (length >= 3): ")
        print(", ".join([i for i in set(self.words_found) if len(i) >= 3])) # Print out all words
        print("\n\n\n")


# # # # #
def __main__():
    # Initialize new BoggleBoard with standard size of 5 x 5
    board = BoggleBoard(5)
    
    print("BOGGLE BOARD:")
    board.print_board()

    input("\n\nPress [ENTER] to compute answers...")
    board.solve()

if __name__ == "__main__":
    __main__()