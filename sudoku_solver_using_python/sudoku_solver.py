## Written by Ummay Sumaya Khan (#UFID: 1334-7246) ##

import csv
import sys

# Read the file from terminal
filename = open(sys.argv[1], 'r')
csv_reader = csv.reader(filename)

sudoku = []

# Make 2-D matrix sudoku from the csv file
for row in csv_reader:
    row_integers = [int(value) for value in row]   #make every element in wach row integer
    sudoku.append(row_integers)


# Function to check whether the provided sudoku has repeated numbers in row/ columns/ 3x3 sub-block
def has_repeated_numbers(sudoku):

    # Helper function to check for duplicates in a list
    def has_duplicates(nums):
        seen = set()
        for num in nums:
            if num != 0 and num in seen:
                return True
            seen.add(num)
        return False
    
    for i in range(9):
        # Check rows
        if has_duplicates(sudoku[i]):
            return True
        
        # Check columns
        column = [sudoku[j][i] for j in range(9)]
        if has_duplicates(column):
            return True
        
        # Check 3x3 sub-blocks
        start_row, start_col = 3 * (i // 3), 3 * (i % 3)
        sub_block = [sudoku[start_row + j][start_col + k] for j in range(3) for k in range(3)]
        if has_duplicates(sub_block):
            return True
    
    return False


# FUnction for find the empty cells
def find_empty_cell(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                return row, col
    return None, None


# Function to check if the given sudoku is valid
def is_valid(sudoku, row, col, num):
    # Check whether the number already exists in the same row and column
    for i in range(9):
        if sudoku[row][i] == num or sudoku[i][col] == num:
            return False

    # Check whether the number already exists in the corresponding 3x3 sub-block
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if sudoku[start_row + i][start_col + j] == num:
                return False

    return True


# Function to solve the sudoku
def solve_sudoku(sudoku):

    # Find the empy cells
    row, col = find_empty_cell(sudoku)

    if row is None:
        return True  # All cells are filled

    for num in range(1, 10):
        # Assign a number in the empty cell if valid
        if is_valid(sudoku, row, col, num):
            sudoku[row][col] = num

            # Recursively solve for each empty cell
            if solve_sudoku(sudoku):
                return True

            sudoku[row][col] = 0  # Backtrack if solution not found

    return False


if has_repeated_numbers(sudoku):
    print("The provided sudoku has repeated numbers. No solution exists.")

else:
    if solve_sudoku(sudoku):
        for row in sudoku:
            print(row)
    else:
        print("No solution exists.")
    
