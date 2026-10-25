"""
AUTHOR: Ebenezer Jiang
DESCRIPTION: Generates and manages Boggle boards, including finding words and storing combinations.
TO-DO:
- Optimize the brute force search for finding words.
- The current version had to be dumbed down to a 3x3 grid to manage computational complexity...
"""

import string
import random
import time

import nltk

all_letters = list(string.ascii_lowercase)
all_vowels = ["a", "e", "i", "o", "u"] # lower

nltk.download('words')
all_words = nltk.corpus.words.words()
def check_word(word) -> bool:
    # check if the word is in the list of all words
    return word.lower() in all_words 

# default size
BOARD_SIZE = 3

# class representing a Boggle board
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
        self.brute_force_iterations = 0

    # return a random letter (to put in the boggle board)
    def pick_letters(self, weight_vowels = True) -> str:
        if weight_vowels and random.randint(0, 5) == 5: # give a higher chance of a vowel
            return all_vowels[random.randint(0, len(all_vowels) - 1)]
        else:
            return all_letters[random.randint(0, len(all_letters) - 1)]

    # return a randomly board
    def generate(self) -> {}:
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

    # #print this boggle board
    def print_board(self) -> None:
        for i in range(self.size): # row
            for j in range(self.size): # column
                print(self.board[f"{i}{j}"], end=" ")
            print()

    #
    def store_combinations(self, path:str) -> None:
        self.brute_force_iterations += 1
        #time.sleep(0.1)
        if path == None:
            print("Invalid path. Abort... NONE TYPE ")
            return

        path_as_list = path.split(",")

        last_index = path_as_list[-1] # STRING! last added index
            
        # there are multiple indexes in the path:
        # Does this path not yet exist in combinations?
        if path not in self.combinations.keys():
            # Only one index in the path?
            if len(path_as_list) == 1:
                # Add to combinations map as the single letter
                self.combinations[path] = self.board[path]
            else:
                path_of_all_but_last = ",".join(path_as_list[:-1])

                previous_combo = self.combinations[path_of_all_but_last]
                last_term = self.board[path_as_list[-1]]

                self.combinations[path] = previous_combo + last_term
        else:
            return

        #print("Paths from start: " + str(self.paths_from_start))
        print("Path: " + path.ljust(50) + " || Word?: " + self.combinations[path].ljust(16) + " || ITERATIONS: " + str(self.brute_force_iterations))

        #CHECK WORD!
        potential_word = self.combinations[path]
        if check_word(potential_word):
            self.words_found.append(potential_word)
            print("Word found! " + potential_word + " | PATH: " + path)
            print("All words: " + str(self.words_found))
    
       
        # Check all surroundings!
        self.new_path(path_as_list, -1, -1)
        self.new_path(path_as_list, 0, -1)
        self.new_path(path_as_list, 1, -1)

        self.new_path(path_as_list, -1, 0)
        # DON'T TRY YOURSELF! NO +0, +0
        self.new_path(path_as_list, 1, 0)

        self.new_path(path_as_list, -1, 1)
        self.new_path(path_as_list, 0, 1)
        self.new_path(path_as_list, 1, 1)
        
        ##print(path)

    def new_path(self, old_path_list:list, horz_inc:int, vert_inc:int) -> None:
        # old_path_list should be like ["00", "10", "11"]
        last_index = old_path_list[-1] # STRING! last added index

        # Since last_index is stored as a string (e.g. "21"), we must separate into integers and update it:
        new_row_num = str(int(last_index[0]) + horz_inc)
        new_col_num = str(int(last_index[1]) + vert_inc)
        new_last_index = f"{new_row_num}{new_col_num}"

        # if the last (added) index does not exist on the board, forget it...
        if new_last_index not in self.board.keys():
            #print("Out of bounds. Abort... " + new_path)
            return

        # # #
        # Create new path [00, 01, 02] + JUST ADDED "03" (new_last_index)
        new_path = ",".join(old_path_list) + "," + new_last_index

        # If you already visited here, you can't visit again...
        if new_last_index in old_path_list:
            #print("Already visited this index. Abort...", new_last_index, old_path_list)
            return
        # If you already tried this path, you can't visit again...
        elif new_path in self.combinations.keys():
            return

        # You passed!
        self.store_combinations(new_path)

"""set_board = {
    '00': 'a', '01': 'b', '02': 'c', '03': 'd', 
    '10': 'e', '11': 'f', '12': 'g', '13': 'h',
    '20': 'i', '21': 'j', '22': 'k', '23': 'l', 
    '30': 'm', '31': 'n', '32': 'o', '33': 'p'
} # manually defined 4x4 boggle board"""

set_board = {
    '00': 'a', '01': 'l', '02': 'l', 
    '10': 'e', '11': 'e', '12': 'o',
    '20': 's', '21': 'h', '22': 'i'
} # manually defined 3x3 boggle board


def __main__():
    board = BoggleBoard(3)
    board.print_board()
    
    for path in board.board.keys():
        board.store_combinations(path)

    print(board.words_found)

    board.print_board()

if __name__ == "__main__":
    __main__()