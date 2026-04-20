# Project Development Instructions

## Overview
This document provides guidelines for AI developer assistants and developers working on this Python Sudoku project. It ensures code quality, maintainability, and comprehensive testing practices.

---

## 1. AI Developer Assistant Role

As an AI developer assistant (GitHub Copilot), You will:

- **Provide Python-based Solutions**: All code implementations will be written in Python, following Python best practices (PEP 8)
- **Suggest Related Platforms**: Recommend appropriate frameworks, libraries, and tools for the project needs
  - Current Stack: Flask (web framework), Pytest (testing), JSON (data persistence)
  - Additional platforms/tools may be suggested based on feature requirements
- **Ensure Code Quality**: Write clean, efficient, and maintainable code
- **Maintain Consistency**: Follow the established project structure and conventions

---

## 2. Code Standards

### Simplicity and Clarity
- **Keep Code Simple**: Write straightforward, easy-to-understand code
- **Avoid Over-Engineering**: Use the simplest solution that meets requirements
- **Readability First**: Clear code is better than clever code

### Documentation Requirements
- **Docstrings**: Every function and class must have a docstring explaining purpose, parameters, and return values
  ```python
  def solve_sudoku(board):
      """
      Solve a Sudoku puzzle using backtracking algorithm.
      
      Args:
          board (list): 9x9 2D list representing the Sudoku grid
      
      Returns:
          bool: True if puzzle is solved, False otherwise
      """
  ```
- **Inline Comments**: Use comments for complex logic and non-obvious implementations
- **Type Hints**: Include type hints where applicable for better code understanding

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Maximum line length: 88 characters (Black formatter standard)
- Use 4 spaces for indentation

---

## 3. Unit Testing Requirements

### Test Coverage
- **Complete Coverage**: All functions must have unit tests
- **Multiple Scenarios**: Test normal cases, edge cases, and error conditions
- **Test Organization**: Tests are organized in the `tests/` directory

### Testing Framework
- **Tool**: Pytest
- **Location**: `tests/` directory
- **Naming Convention**: `test_*.py` for test files, `test_*()` for test functions

### Test Requirements by Module

#### Sudoku Logic (`sudoku_logic.py`)
- [ ] Test all validation functions
- [ ] Test puzzle solving with valid inputs
- [ ] Test puzzle solving with invalid/incomplete puzzles
- [ ] Test edge cases (empty board, full board, impossible puzzles)

#### Flask App (`app.py`)
- [ ] Test route accessibility (GET/POST requests)
- [ ] Test data validation
- [ ] Test response formats (HTML, JSON)
- [ ] Test error handling

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sudoku_logic.py

# Run with coverage report
pytest --cov=. tests/
```

---

## 4. Change Documentation and Impact Analysis

When implementing changes, document:

### Change Description Format
```
### Change: [Feature/Fix Title]

**What Changed:**
- Brief description of the modification

**Why:**
- Reason for the change
- Problem it solves or feature it adds

**Impact on Project Flow:**
- How this affects existing functionality
- Any breaking changes
- Performance implications
- User-facing changes
```

### Impact Categories

1. **User Interface Impact**
   - Changes to UI behavior, appearance, or user workflows
   - New features or removed functionality visible to users

2. **Backend Logic Impact**
   - Changes to algorithms, business logic, or data processing
   - Performance improvements or regressions
   - Data structure modifications

3. **Testing Impact**
   - New tests required
   - Existing tests that may be affected
   - Coverage improvements

4. **Integration Impact**
   - Changes to APIs or function signatures
   - Dependencies on other modules
   - Compatibility with existing features

### Example Change Documentation
```
### Change: Implement Sudoku Hint System

**What Changed:**
- Added `get_hint()` function to sudoku_logic.py
- Added new endpoint `/api/hint` in app.py
- Frontend button to request hints

**Why:**
- Improve user experience for stuck players
- Common feature in Sudoku applications

**Impact on Project Flow:**
- User Logic Flow: Player can now request hints during game
- Backend: New function uses existing solve logic
- Testing: Added 3 new unit tests for hint generation
- No breaking changes to existing APIs
```


## 5. Workflow Guidelines

### For New Features
1. **Plan**: Clearly define what the feature should do
2. **Code**: Implement in Python with proper documentation
3. **Test**: Write unit tests covering all scenarios
4. **Document**: Add change documentation with impact analysis
5. **Review**: Ensure code meets standards in section 2

### For Bug Fixes
1. **Identify**: Reproduce and understand the bug
2. **Fix**: Implement the minimal fix needed
3. **Test**: Add/update tests to prevent regression
4. **Document**: Explain what was broken and how it was fixed

### For Refactoring
1. **Improve**: Enhance code structure or performance
2. **Preserve**: Maintain all existing functionality
3. **Test**: Run full test suite to ensure nothing breaks
4. **Document**: Explain why refactoring was needed and its benefits

---

## 6. Dependencies and Platforms

### Current Stack
- **Framework**: Flask (web development)
- **Testing**: Pytest (unit testing)
- **Data Storage**: JSON (simple persistence)
- **Frontend**: HTML, CSS, JavaScript (vanilla)

### Installation and Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if using dev environment)
pip install pytest pytest-cov

# Activate virtual environment (if using venv)
# Windows:
.venv\Scripts\Activate.ps1
# Unix/MacOS:
source .venv/bin/activate
```

---

## 7. Common Development Tasks

### Adding a New Function
1. Write function with docstring
2. Add 1-3 unit tests minimum
3. Update this file if it's a major feature
4. Run `pytest` to verify all tests pass

### Modifying Existing Code
1. Run existing tests first
2. Make changes
3. Run tests again
4. Update documentation if behavior changed