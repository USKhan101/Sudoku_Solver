import sys

def is_valid(board):

    height = len(board)
    width = len(board[0])

    if height != width:
        print("ERROR! Please give a board with the same width and height. Exiting...")
        sys.exit()
       

    # Checking the rows have repeated numbers
    for r in range(height):
        for c in range(height):
            num = board[r][c]
            for j in range(c+1,height):
                if board[r][j] == num and num!=0:
                    print(f"Row Conflict at ({r+1},{c+1}) and ({r+1},{j+1}). Exiting...")
                    sys.exit()

    # Checking the columns have repeated numbers
    for c in range(height):
        for r in range(height):
            num = board[r][c]
            for j in range(r+1,height):
                if board[j][c] == num and num!=0:
                    print(f"Column Conflict at ({r+1},{c+1}) and ({j+1},{c+1}). Exiting...")
                    sys.exit()

    # Checking sub squares have repeated numbers
    for i in range(3):
        for j in range(3):
            start_r, start_c = 3 * i, 3 * j

            # Create a dictionary to store the positions of unique numbers in the submatrix
            positions = {}
            conflicted_cells = []
            for r in range(3):
                for c in range(3):
                    num = board[start_r+r][start_c+c]
                    # If the number is already in the dictionary, it's a conflict
                    if num in positions and num!=0:
                        pos_r, pos_c = positions[num]
                        print(f"Sub-square Conflict at ({pos_r+1}, {pos_c+1}) and ({start_r+r+1},{start_c+c+1}). Exiting...")
                        sys.exit()
                    else:
                        positions[num] = (start_r+r, start_c+c)

    return
