import io
import re

# Converting Z3 model into a output text file

def read_z3_model(model):

    with io.open(model, 'r', encoding="utf8") as file:

        model_text = file.read()

    sudoku = []
    sudoku_temp = []
    size = 0

    extract  = re.compile(r"define-fun v\d+x\d+_\d+ \(\) Bool\n    true")
    cells = re.findall(extract, model_text)

    for cell in cells:
        # Extract all the row, col and value from the model
        nums = [int(n) for n in re.findall(r"\d+", cell)]

        sudoku_temp.append(nums)

        if nums[1] > size:

            size = nums[1]

    for i in range(size):
        sudoku.append([0] * size)

    # convert the model into a sudoku
    for row, col, val in sudoku_temp:
        sudoku[row - 1][col - 1] = val

    return sudoku
