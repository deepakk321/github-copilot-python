"""Test suite for sudoku_logic module."""
import pytest
import sudoku_logic as sl


class TestBoardCreation:
    """Test board creation and initialization."""

    def test_create_empty_board(self):
        """Test that empty board is created with correct dimensions."""
        board = sl.create_empty_board()
        assert len(board) == 9
        assert all(len(row) == 9 for row in board)
        assert all(cell == 0 for row in board for cell in row)

    def test_create_empty_board_structure(self):
        """Test that empty board is properly structured."""
        board = sl.create_empty_board()
        for i in range(sl.SIZE):
            for j in range(sl.SIZE):
                assert board[i][j] == sl.EMPTY


class TestValidation:
    """Test move validation and safety checks."""

    def test_is_safe_true(self):
        """Test that a valid placement is recognized as safe."""
        board = sl.create_empty_board()
        assert sl.is_safe(board, 0, 0, 5) is True

    def test_is_safe_duplicate_row(self):
        """Test that duplicate in row is not safe."""
        board = sl.create_empty_board()
        board[0][0] = 5
        assert sl.is_safe(board, 0, 1, 5) is False

    def test_is_safe_duplicate_column(self):
        """Test that duplicate in column is not safe."""
        board = sl.create_empty_board()
        board[0][0] = 5
        assert sl.is_safe(board, 1, 0, 5) is False

    def test_is_safe_duplicate_box(self):
        """Test that duplicate in 3x3 box is not safe."""
        board = sl.create_empty_board()
        board[0][0] = 5
        # Same 3x3 box
        assert sl.is_safe(board, 1, 1, 5) is False
        # Different 3x3 box
        assert sl.is_safe(board, 3, 3, 5) is True

    def test_is_valid_move_out_of_bounds(self):
        """Test that out of bounds moves are invalid."""
        board = sl.create_empty_board()
        assert sl.is_valid_move(board, -1, 0, 5) is False
        assert sl.is_valid_move(board, 10, 0, 5) is False
        assert sl.is_valid_move(board, 0, -1, 5) is False
        assert sl.is_valid_move(board, 0, 10, 5) is False

    def test_is_valid_move_invalid_number(self):
        """Test that invalid numbers are rejected."""
        board = sl.create_empty_board()
        assert sl.is_valid_move(board, 0, 0, 0) is False
        assert sl.is_valid_move(board, 0, 0, 10) is False
        assert sl.is_valid_move(board, 0, 0, -1) is False

    def test_is_valid_move_valid(self):
        """Test that valid moves are accepted."""
        board = sl.create_empty_board()
        assert sl.is_valid_move(board, 0, 0, 5) is True

    def test_is_valid_move_duplicate_conflict(self):
        """Test that moves creating conflicts are invalid."""
        board = sl.create_empty_board()
        board[0][0] = 5
        assert sl.is_valid_move(board, 0, 1, 5) is False


class TestBoardFilling:
    """Test board filling algorithm."""

    def test_fill_board(self):
        """Test that board filling completes successfully."""
        board = sl.create_empty_board()
        result = sl.fill_board(board)
        assert result is True

    def test_filled_board_complete(self):
        """Test that filled board has no empty cells."""
        board = sl.create_empty_board()
        sl.fill_board(board)
        assert all(cell != sl.EMPTY for row in board for cell in row)

    def test_filled_board_valid(self):
        """Test that filled board is a valid Sudoku."""
        board = sl.create_empty_board()
        sl.fill_board(board)
        # Check no duplicates in rows
        for row in board:
            assert len(row) == len(set(row))
        # Check no duplicates in columns
        for col in range(sl.SIZE):
            column = [board[row][col] for row in range(sl.SIZE)]
            assert len(column) == len(set(column))


class TestCellRemoval:
    """Test cell removal for puzzle creation."""

    def test_remove_cells(self):
        """Test that cells are removed correctly."""
        board = sl.create_empty_board()
        sl.fill_board(board)
        original_clues = sum(1 for row in board for cell in row if cell != sl.EMPTY)
        
        sl.remove_cells(board, 35)
        remaining_clues = sum(1 for row in board for cell in row if cell != sl.EMPTY)
        
        assert remaining_clues == 35

    def test_remove_cells_preserves_some_clues(self):
        """Test that at least some clues remain."""
        board = sl.create_empty_board()
        sl.fill_board(board)
        
        sl.remove_cells(board, 30)
        clues = sum(1 for row in board for cell in row if cell != sl.EMPTY)
        
        assert clues == 30
        assert clues > 0


class TestPuzzleGeneration:
    """Test puzzle generation."""

    def test_generate_puzzle_easy(self):
        """Test puzzle generation with easy difficulty."""
        puzzle, solution = sl.generate_puzzle('easy')
        puzzle_clues = sum(1 for row in puzzle for cell in row if cell != sl.EMPTY)
        
        assert len(puzzle) == 9
        assert len(solution) == 9
        assert puzzle_clues == sl.DIFFICULTY_LEVELS['easy']

    def test_generate_puzzle_medium(self):
        """Test puzzle generation with medium difficulty."""
        puzzle, solution = sl.generate_puzzle('medium')
        puzzle_clues = sum(1 for row in puzzle for cell in row if cell != sl.EMPTY)
        
        assert len(puzzle) == 9
        assert len(solution) == 9
        assert puzzle_clues == sl.DIFFICULTY_LEVELS['medium']

    def test_generate_puzzle_hard(self):
        """Test puzzle generation with hard difficulty."""
        puzzle, solution = sl.generate_puzzle('hard')
        puzzle_clues = sum(1 for row in puzzle for cell in row if cell != sl.EMPTY)
        
        assert len(puzzle) == 9
        assert len(solution) == 9
        assert puzzle_clues == sl.DIFFICULTY_LEVELS['hard']

    def test_generate_puzzle_numeric_clues(self):
        """Test puzzle generation with numeric clue count."""
        puzzle, solution = sl.generate_puzzle(40)
        puzzle_clues = sum(1 for row in puzzle for cell in row if cell != sl.EMPTY)
        
        assert puzzle_clues == 40

    def test_puzzle_and_solution_different(self):
        """Test that puzzle and solution are different."""
        puzzle, solution = sl.generate_puzzle('medium')
        assert not all(
            puzzle[i][j] == solution[i][j]
            for i in range(sl.SIZE)
            for j in range(sl.SIZE)
        )

    def test_solution_is_complete(self):
        """Test that solution has all cells filled."""
        puzzle, solution = sl.generate_puzzle('medium')
        assert all(cell != sl.EMPTY for row in solution for cell in row)

    def test_puzzle_is_subset_of_solution(self):
        """Test that puzzle clues match solution values."""
        puzzle, solution = sl.generate_puzzle('medium')
        for i in range(sl.SIZE):
            for j in range(sl.SIZE):
                if puzzle[i][j] != sl.EMPTY:
                    assert puzzle[i][j] == solution[i][j]


class TestUtilityFunctions:
    """Test utility functions."""

    def test_deep_copy(self):
        """Test that deep copy creates independent copy."""
        board1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        board2 = sl.deep_copy(board1)
        board2[0][0] = 99
        assert board1[0][0] == 1

    def test_get_difficulty_from_clues(self):
        """Test difficulty detection from clue count."""
        assert sl.get_difficulty_from_clues(45) == 'easy'
        assert sl.get_difficulty_from_clues(35) == 'medium'
        assert sl.get_difficulty_from_clues(25) == 'hard'
        assert sl.get_difficulty_from_clues(50) == 'easy'


class TestCountSolutions:
    """Test solution counting."""

    def test_count_solutions_empty_board(self):
        """Test that empty board has many solutions."""
        board = sl.create_empty_board()
        count = sl.count_solutions(board, limit=3)
        # Should have multiple solutions (we stop at limit)
        assert count >= 2

    def test_count_solutions_complete_board(self):
        """Test that complete valid board has exactly 1 solution."""
        board = sl.create_empty_board()
        sl.fill_board(board)
        count = sl.count_solutions(sl.deep_copy(board), limit=2)
        assert count == 1
