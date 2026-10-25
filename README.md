#### **AUTHOR:** 
_Ebenezer Jiang_ 

## **OVERVIEW:** 
Creates a class for Boggle boards, offering methods to generate, store, and solve the Boggle boards.

## **HOW IT WORKS:**
- The BoggleBoard class represents a Boggle board and provides methods to generate the board, print it, and store combinations of letters along paths. 
The `combinations` dictionary keeps track of all possible paths and their corresponding words. Whenever a valid word is found, it is appended to the `words_found` list. 

- The `iteration_count` counter tracks the number of iterations performed during the search.

- The program uses recursion to explore all possible paths on the Boggle board, storing the combinations and checking for valid words. Valid words are stored in the `words_found` list. 

- A grammatical approach is implemented to optimize memory. Each route is monitered based on whether words in `all_words` start with the current substring. If there is no word that begins with that substring, that means the current path can be terminated and forgotten.

## **NOTE:**
- In this program, the term `combination` is used to refer to the substring formed by various steps. For example, in this boggle board:
  ```
  a  b  c     00 01 02 
  d  e  f --> 10 11 12 
  g  h  i     20 21 22 
  ```
  The path `"00,01,11,22"` would have a combination of `"abei"`
  The path `"11,20,21"` would have a combination of `"egh"`

## DISCLAIMER:
* The maximum Boggle Board size is 9, otherwise the logic fails, since indexes and paths are stored on a 
2-digit base-10 system (e.g. the position `"01"` represents the `0th` row and the `1st` column), thus the max
position is `"99"`. This is fixable if one updated the code to expend paths to a four-digit position string
(`10th` row + `24th` column = pos `"1024"`)


Created on 10/25/2026 @ 16:34 PM 
