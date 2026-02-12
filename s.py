import matplotlib.pyplot as plt
import random
import copy

def create_base_grid():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

def solve_check(board, limit=2):
    """
    Returns number of solutions found, up to 'limit'.
    """
    find = find_empty(board)
    if not find:
        return 1
    row, col = find

    count = 0
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            count += solve_check(board, limit)
            board[row][col] = 0
            if count >= limit: 
                return count
    return count

def is_valid(board, num, pos):
    # Check row
    if num in board[pos[0]]: return False
    # Check column
    if num in [board[i][pos[1]] for i in range(9)]: return False
    # Check box
    box_x, box_y = pos[1] // 3, pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def mask_grid_symmetric(board):
    puzzle = copy.deepcopy(board)
    
    # List of coordinates to attempt removing
    coords = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(coords)
    
    for r, c in coords:
        if puzzle[r][c] == 0:
            continue # Already removed
            
        # Identify symmetric partner
        sym_r, sym_c = 8 - r, 8 - c
        
        # Store original values
        val_1 = puzzle[r][c]
        val_2 = puzzle[sym_r][sym_c]
        
        # Remove both
        puzzle[r][c] = 0
        puzzle[sym_r][sym_c] = 0
        
        if solve_check(copy.deepcopy(puzzle)) != 1:
            puzzle[r][c] = val_1
            puzzle[sym_r][sym_c] = val_2
            
    return puzzle

def save_grid_image(grid, filename, title="Sudoku", color='black'):
    fig, ax = plt.subplots(figsize=(7, 7))

    # Draw grid lines
    for i in range(10):
        # Thicker lines for the 3x3 boxes
        linewidth = 3.0 if i % 3 == 0 else 1.0
        ax.plot([0, 9], [i, i], color='black', linewidth=linewidth)
        ax.plot([i, i], [0, 9], color='black', linewidth=linewidth)

    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            if val != 0:
                ax.text(c + 0.5, 8.5 - r, str(val),
                        va='center', ha='center', fontsize=22,
                        weight='bold', family='sans-serif', color=color)

    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.close()


# 1. Create full solution
full_solution = create_base_grid()

# 2. Create symmetric puzzle
puzzle_grid = mask_grid_symmetric(full_solution)

# 3. Save Puzzle Image (Blue numbers)
save_grid_image(puzzle_grid, "sudoku_puzzle_symmetric.png", "Sudoku Puzzle", color='navy')
print("Saved sudoku_puzzle_symmetric.png")

# 4. Save Solution Image (Green numbers)
save_grid_image(full_solution, "sudoku_solution_key.png", "Solution Key", color='darkgreen')
print("Saved sudoku_solution_key.png")

# 5. Print Stats
clues = sum(1 for r in puzzle_grid for c in r if c != 0)
print(f"Clues remaining: {clues}")
