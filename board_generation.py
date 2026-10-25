import string
import random
import nltk
import time

all_letters = list(string.ascii_lowercase)
all_vowels = ["a", "e", "i", "o", "u"] # lower

all_words = nltk.corpus.words.words()
def check_word(word) -> bool:
    # check if the word is in the list of all words
    return word.lower() in all_words 

# default size
BOARD_SIZE = 4

# class representing a Boggle board
class BoggleBoard:
    def __init__(self, size = BOARD_SIZE, inputed_board = None):
        self.size = size # boards will have dimensions of "size" x "size"
        self.board = inputed_board if inputed_board else self.generate() # must be a {}

        # Combinations will store paths:
        # { "00,01,02,12" : text: "abcd" } # path (list) to a string
        self.combinations = {}

        # Store all words found on the board
        self.words_found = []

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

    # print this boggle board
    def print_board(self) -> None:
        for i in range(self.size): # row
            for j in range(self.size): # column
                print(self.board[f"{i}{j}"], end=" ")
            print()

    #
    def store_combinations(self, path:str) -> None:
        time.sleep(0.1)
        if path == None:
            print("Invalid path. Abort... NONE TYPE ")
            return

        path_as_list = path.split(",")
        #print(path_as_list)

        last_index = path_as_list[-1] # STRING! last added index

        # Only one index in the path?
        if len(path_as_list) == 1:
            # Add to combinations map as the single letter
            self.combinations[path] = self.board[path]
        # there are multiple indexes in the path:
        # Does this path not yet exist in combinations?
        elif path not in self.combinations.keys():
            path_of_all_but_last = ",".join(path_as_list[:-1])

            previous_combo = self.combinations[path_of_all_but_last]
            last_term = self.board[path_as_list[-1]]

            self.combinations[path] = previous_combo + last_term
        else:
            print("Abort...")
            return

        print("Current combination: " + str(self.combinations[path]))

        #CHECK WORD!
        potential_word = self.combinations[path]
        if check_word(potential_word):
            self.words_found.append(potential_word)
            print("Word found! " + potential_word)
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
        
        #print(path)

    def new_path(self, old_path_list:list, horz_inc:int, vert_inc:int) -> None:
        # old_path_list should be like ["00", "10", "11"]
        last_index = old_path_list[-1] # STRING! last added index

        #print("LI: " + last_index)

        # Since last_index is stored as a string (e.g. "21"), we must separate into integers to update it:
        # ...to update rows:
        new_row_num = str(int(last_index[0]) + horz_inc)
        # ...to update columns:
        new_col_num = str(int(last_index[1]) + vert_inc)

        #print(f"NR: {new_row_num} || NC: {new_col_num}")

        new_last_index = f"{new_row_num}{new_col_num}"

        # If you already visited here, you can't visit again...
        if new_last_index in old_path_list:
            return
        
        new_path = ",".join(old_path_list) + "," + new_last_index

        # if the last (added) index does not exist on the board, forget it...
        if new_last_index not in self.board.keys():
            print("Out of bounds. Abort... " + new_path)
            return
        # If you already tried this path, you can't visit again...
        elif new_path in self.combinations.keys():
            return 

        # You passed!
        self.store_combinations(new_path)

set_board = {
    '00': 'a', '01': 'b', '02': 'c', '03': 'd', 
    '10': 'e', '11': 'f', '12': 'g', '13': 'h',
    '20': 'a', '21': 'b', '22': 'c', '23': 'd', 
    '30': 'e', '31': 'f', '32': 'g', '33': 'h'
} # manually defined 4x4 boggle board


def __main__():
    board = BoggleBoard(BOARD_SIZE, set_board)

    board.store_combinations("00")

if __name__ == "__main__":
    __main__()