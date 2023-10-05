from math import sqrt

# Initialization of the vars for each cell
def z3_vars(sudoku):

    # The naming convention for each var is v<ROW>x<Column>_<Value>
    vars = dict()
    size = len(sudoku)

    for i in range(size):
        for j in range(size):
            # Assign False for all the values of each cell 
            for n in range(1, size + 1):
                v_name = f"v{i+1}x{j+1}_{n}"
                vars[v_name] = False
            # The value will be set to True if there is a value in the cell
            if sudoku[i][j] != 0:
                v_name = f"v{i+1}x{j+1}_{sudoku[i][j]}"
                vars[v_name] = True
    return vars

# Generate script for Z3 simulation
def write_z3_code(sudoku):
    vars = z3_vars(sudoku)
    size = len(sudoku)

    command = "; Declare the vars:\n"
    command += "; The variable's naming convention: v<Row>x<Column>_Value\n"
    command += "\n"

    # Declaring all vars as Bool
    for key in vars:
        command += f"(declare-const {key} Bool)\n"
    command += "\n"

    command += "; Assert True to the vars containing values in provided sudoku\n"
    command += "\n"

    # Asserting True to the vars having a value in provided Sudoku
    for key, value in vars.items():
        if value:
            command += f"(assert (= {key} true))\n"
    command += "\n"

    # Propositional logic for each cell
    command += "; Propositional logic: A cell can only hold one value.\n"
    command += "\n"

    for i in range(1, size + 1):

        for j in range(1, size + 1):

            cell_vals = []

            for value in range(1, size + 1):

                cell_vals.append(f"v{i}x{j}_{value}")

            command += f"; Values for cell {i} x {j} cell_vals. Only one value is true and others will be false\n"
            command += f"; Asserting XOR for confirming that one cell holds only one value\n"
            command += "\n"

            for k in range(len(cell_vals)):
                other_vars = cell_vals[:k] + cell_vals[(k+1):]
                command += f" (assert (=> (= {cell_vals[k]} true)\n"
                command += "    (and\n"
                for var in other_vars:
                    command += f"      (= {var} false)\n"
                command += "    )\n"
                command += "  )\n"
                command += ")\n"

            command += " (assert (xor\n"
            command += f"    {' '.join(cell_vals)}\n"
            command += "  )\n"
            command += ")\n"
            command += "\n"
    command += "\n"

    # Propositional logic for Rows and Columns holding one value only in one cell
    command += "; Propositional logic: A cell in each row and column can hold a unique value.\n"
    command += "\n"

    command += "; Each row and each column must have only one instance of each value.\n"
    command += "\n"
    for value in range(1, size + 1):

        for i in range(1, size + 1):

            row_vals = []
            col_vals = []

            for j in range(1, size + 1):

                row_vals.append(f"v{i}x{j}_{value}")
                col_vals.append(f"v{j}x{i}_{value}")

            command += f"; Rows, columns only have one instance of value {value}\n"
            command += f"; Only one instance of one value is true and others will be false\n"
            command += "\n"
            # One value in each row and column will be true once and other cells will be set to false
            for k in range(0, size):
                other_rows = row_vals[:k] + row_vals[(k+1):]
                other_cols = col_vals[:k] + col_vals[(k+1):]
                command += f"; Rows for {row_vals[k]}\n"
                command += "(assert\n"
                command += f"  (=> (= {row_vals[k]} true)\n"
                command += "    (and\n"
                for row in other_rows:
                    command += f"      (= {row} false)\n"
                command += "    )\n"
                command += "  )\n"
                command += ")\n"
                command += f"; Columns for {col_vals[k]}\n"
                command += "(assert\n"
                command += f"  (=> (= {col_vals[k]} true)\n"
                command += "    (and\n"
                for col in other_cols:
                    command += f"      (= {col} false)\n"
                command += "    )\n"
                command += "  )\n"
                command += ")\n"
                command += "\n"
    command += "\n"

    # Propositional logic for checking 3x3 sub squares
    command += "; Propositional Logic: For a sudoku of size n^2 x n^2,\n"
    command += "; the sub squares of n x n should hold only unique value.\n"
    command += "\n"
    square_size = int(sqrt(size))
    # Generating sub squares
    for i in range(1, size, square_size):
        col_bounds = i + square_size - 1
        for j in range(1, size, square_size):
            row_bounds = j + square_size - 1
            command += f"; sub square positions are from {i} x {j} to {col_bounds} x {row_bounds}\n"
            # Generate the positions of each sub square
            sqr_pos = []
            for col in range(i, col_bounds + 1):
                for row in range(j, row_bounds + 1):
                    sqr_pos.append((col, row))

            # One value in each sub_square will be true once and other cells will be set to false
            for pos_index in range(0, len(sqr_pos)):
                other_sqr_pos = sqr_pos[:pos_index] + sqr_pos[(pos_index + 1):]
                command += f"; Cell Position in sub_square: {sqr_pos[pos_index][0]} x {sqr_pos[pos_index][1]}\n"
                for value in range(1, size + 1):
                    command += f"; For value: {value}\n"
                    command += f"  (assert (=> (= v{sqr_pos[pos_index][0]}x{sqr_pos[pos_index][1]}_{value} true)\n"
                    command += "    (and\n"
                    for pos in other_sqr_pos:
                        command += f" (= v{pos[0]}x{pos[1]}_{value} false)\n"
                    command += "    )\n"
                    command += "  )\n"
                    command += ")\n"
            command += "\n"

    command += "; Check if the sudoku has a solution, and get the model\n"
    command += "(check-sat)\n"
    command += "(get-model)\n"

    return command
