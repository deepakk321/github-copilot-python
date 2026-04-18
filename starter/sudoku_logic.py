import copy
import random

SIZE = 9
EMPTY = 0

# Difficulty levels: (difficulty_name, number_of_clues)
DIFFICULTY_LEVELS = {
    'easy': 45,
    'medium': 35,
    'hard': 25
}


def deep_copy(board):
    """Create a deep copy of a board."""
    return copy.deepcopy(board)


def create_empty_board():
    """Create an empty 9x9 Sudoku board."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    """Check if placing num at (row, col) is valid."""
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_valid_move(board, row, col, num):
    """Validate a single move on the board."""
    if not (0 <= row < SIZE and 0 <= col < SIZE):
        return False
    if num < 1 or num > 9:
        return False
    
    # Temporarily place the number
    original = board[row][col]
    board[row][col] = num
    
    # Check row
    for x in range(SIZE):
        if x != col and board[row][x] == num:
            board[row][col] = original
            return False
    
    # Check column
    for x in range(SIZE):
        if x != row and board[x][col] == num:
            board[row][col] = original
            return False
    
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            r, c = start_row + i, start_col + j
            if (r != row or c != col) and board[r][c] == num:
                board[row][col] = original
                return False
    
    board[row][col] = original
    return True


def fill_board(board):
    """Recursively fill the board with valid numbers."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(board, limit=2):
    """Count the number of solutions (stop at limit for efficiency)."""
    count = [0]
    
    def backtrack():
        if count[0] > limit:
            return
        
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    for num in range(1, SIZE + 1):
                        if is_safe(board, row, col, num):
                            board[row][col] = num
                            backtrack()
                            board[row][col] = EMPTY
                    return
        
        count[0] += 1
    
    backtrack()
    return count[0]


def has_unique_solution(puzzle):
    """Verify that the puzzle has exactly one solution."""
    board = deep_copy(puzzle)
    return count_solutions(board, limit=2) == 1


def remove_cells(board, clues):
    """Remove cells to create puzzle from solution."""
    attempts = SIZE * SIZE - clues
    removed_positions = []
    
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        
        if board[row][col] != EMPTY and (row, col) not in removed_positions:
            removed_positions.append((row, col))
            board[row][col] = EMPTY
            attempts -= 1


def generate_puzzle(difficulty='medium'):
    """Generate a new Sudoku puzzle with specified difficulty."""
    if isinstance(difficulty, int):  # Legacy support
        clues = difficulty
    else:
        clues = DIFFICULTY_LEVELS.get(difficulty.lower(), 35)
    
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    
    return puzzle, solution


def get_difficulty_from_clues(clues):
    """Determine difficulty level from number of clues."""
    for difficulty, count in sorted(DIFFICULTY_LEVELS.items(), key=lambda x: -x[1]):
        if clues >= count:
            return difficulty
    return 'hard'
