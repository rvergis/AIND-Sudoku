# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twins have 2 properties in a unit 

  1. the value they hold are the same and of length 2
  2. there are 2 of them

   
Each of the naked twins would be constrained to hold one of the values.This implies that other boxes in the unit would not hold either of the values
  
To solve this in code
  
1. identify the naked twins boxes and the naked twin value in each unit
	* build a dict of k, v pairs where k is the string value and v is the list of boxes   		   
	* k is of length 2 chars
2. search through the other boxes and remove all of the naked twin entries


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The dialogal sudoku problem adds the boxes along the 2 diagonals to the set of constraints.
  	
  This creates 2 additional units
  	
  1. for the diagonal from top left to bottom right
  2. for the diagonal from the bottom left to the top right
   
  To solve this in code
  
  Create diagonal units and add it to the unitlist
 
        `diagonal_units = [["".join(z) for z in zip(rows, cols)], ["".join(z) for z in zip(reversed(rows), cols)]]`
        `unitlist = row_units + column_units + square_units + diagonal_units`
        
  No additional code changes are necessary. The above code will ensure that the diagonals will be included in appling constraint propagation to the units.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.