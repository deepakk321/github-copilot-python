TEST RESULTS - SUDOKU GAME PROJECT
===================================

Date: April 19, 2026
Total Tests: 49
Status: ALL PASSED ✅

Test Command:
    py -m pytest tests/ -v --tb=short

============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\project\github-copilot-python\starter
plugins: anyio-4.13.0, cov-7.1.0
collecting ... collected 49 items

FLASK ROUTE TESTS (23 tests)
================================
tests/test_app.py::TestIndexRoute
  ✓ test_index_returns_status_200 PASSED
  ✓ test_index_returns_html PASSED

tests/test_app.py::TestNewGameRoute
  ✓ test_new_game_returns_puzzle PASSED
  ✓ test_new_game_medium_difficulty PASSED
  ✓ test_new_game_easy_difficulty PASSED
  ✓ test_new_game_hard_difficulty PASSED
  ✓ test_new_game_invalid_difficulty_defaults_to_medium PASSED
  ✓ test_new_game_returns_solution PASSED
  ✓ test_new_game_puzzle_subset_of_solution PASSED

tests/test_app.py::TestValidateRoute
  ✓ test_validate_valid_move PASSED
  ✓ test_validate_returns_boolean PASSED
  ✓ test_validate_missing_game PASSED

tests/test_app.py::TestCheckRoute
  ✓ test_check_solution_incomplete PASSED
  ✓ test_check_solution_no_game PASSED
  ✓ test_check_solution_returns_json PASSED

tests/test_app.py::TestScoreboardRoute
  ✓ test_get_scoreboard PASSED
  ✓ test_post_score PASSED
  ✓ test_post_score_invalid_time PASSED
  ✓ test_post_score_with_name PASSED
  ✓ test_post_score_truncates_long_name PASSED

tests/test_app.py::TestDifficultiesRoute
  ✓ test_get_difficulties PASSED

tests/test_app.py::TestRouteIntegration
  ✓ test_new_game_then_check PASSED
  ✓ test_new_game_then_save_score PASSED


SUDOKU LOGIC TESTS (26 tests)
================================
tests/test_sudoku_logic.py::TestBoardCreation
  ✓ test_create_empty_board PASSED
  ✓ test_create_empty_board_structure PASSED

tests/test_sudoku_logic.py::TestValidation
  ✓ test_is_safe_true PASSED
  ✓ test_is_safe_duplicate_row PASSED
  ✓ test_is_safe_duplicate_column PASSED
  ✓ test_is_safe_duplicate_box PASSED
  ✓ test_is_valid_move_out_of_bounds PASSED
  ✓ test_is_valid_move_invalid_number PASSED
  ✓ test_is_valid_move_valid PASSED
  ✓ test_is_valid_move_duplicate_conflict PASSED

tests/test_sudoku_logic.py::TestBoardFilling
  ✓ test_fill_board PASSED
  ✓ test_filled_board_complete PASSED
  ✓ test_filled_board_valid PASSED

tests/test_sudoku_logic.py::TestCellRemoval
  ✓ test_remove_cells PASSED
  ✓ test_remove_cells_preserves_some_clues PASSED

tests/test_sudoku_logic.py::TestPuzzleGeneration
  ✓ test_generate_puzzle_easy PASSED
  ✓ test_generate_puzzle_medium PASSED
  ✓ test_generate_puzzle_hard PASSED
  ✓ test_generate_puzzle_numeric_clues PASSED
  ✓ test_puzzle_and_solution_different PASSED
  ✓ test_solution_is_complete PASSED
  ✓ test_puzzle_is_subset_of_solution PASSED

tests/test_sudoku_logic.py::TestUtilityFunctions
  ✓ test_deep_copy PASSED
  ✓ test_get_difficulty_from_clues PASSED

tests/test_sudoku_logic.py::TestCountSolutions
  ✓ test_count_solutions_empty_board PASSED
  ✓ test_count_solutions_complete_board PASSED


TEST SUMMARY
================================
Total: 49 passed in 5.02s ✅

RESULTS BY CATEGORY
================================
Backend Logic Tests:    26/26 PASSED ✅
Flask Route Tests:      23/23 PASSED ✅
Integration Tests:      2/2  PASSED ✅

WHAT'S TESTED
================================

1. SUDOKU LOGIC (test_sudoku_logic.py)
   - Empty board creation and structure
   - Move validation (rows, columns, 3x3 boxes)
   - Boundary checking (out of bounds)
   - Board filling algorithm
   - Cell removal for puzzle creation
   - Puzzle generation for all difficulty levels
   - Utility functions and solution counting

2. FLASK ROUTES (test_app.py)
   - Index page returns HTML
   - New game generation with all difficulty levels
   - Solution validation
   - Move validation endpoint
   - Check solution functionality
   - Scoreboard get/post operations
   - Difficulty levels endpoint
   - Route integration (new game → check → save)

QUICK START
================================

Run all tests:
    cd starter
    python -m pytest tests/ -v

Run tests with coverage:
    cd starter
    python -m pytest tests/ -v --cov=. --cov-report=html

Run specific test:
    cd starter
    python -m pytest tests/test_sudoku_logic.py::TestValidation -v

More details available in README.md "Running Tests" section.
