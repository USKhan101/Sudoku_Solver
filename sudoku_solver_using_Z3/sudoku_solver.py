## Written by Ummay Sumaya Khan (#UFID: 1334-7246) ##

from src import check_board, z3_generator, z3model_converter
import csv
import sys
import os

# Define the path for Z3
z3_path  = "/home/sumaya/Downloads/z3-4.8.10-x64-ubuntu-18.04/bin/z3"
    
# Create the Z3_files and output directory
if(not os.path.exists('./Z3_files')):
    os.makedirs('./Z3_files')

if(not os.path.exists('./output')):
    os.makedirs('./output')

# Define the output files
z3_file  = './Z3_files/sudoku.z3'
z3_out = './Z3_files/sudoku_z3_out.out'
sudoku_out = './output/sudoku_output.txt'

# Read the csv file from terminal
filename = open(sys.argv[1], 'r')
csv_reader = csv.reader(filename)

# Make 2-D matrix sudoku from the csv file
sudoku = []

for row in csv_reader:
    row_integers = [int(value) for value in row]   #make every element in wach row integer
    sudoku.append(row_integers)

# Check if the provided sudoku is valid
check_board.is_valid(sudoku)

# Generate Z3 script
z3_code = z3_generator.write_z3_code(sudoku)

# Write the Z3 script into a file
with open(z3_file, 'w') as f:
    f.write(z3_code)

# Solve with z3
os.system(f"{z3_path} {z3_file} > {z3_out}")

# Convert and write output to file
solved_sudoku = z3model_converter.read_z3_model(z3_out)

# Display the solved sudoku and write into a file
with open(sudoku_out, "w", newline="") as f:

    file = csv.writer(f)

    if (solved_sudoku == []):
        f.write("Sorry, there is no solution!! The sudoku is not solvable!!")
        print ("Sorry, there is no solution!! The sudoku is not solvable!!")
    else:
        for row in solved_sudoku:
            file.writerow(row)
            print(row)
