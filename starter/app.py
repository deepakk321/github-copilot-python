from flask import Flask, render_template, jsonify, request
import sudoku_logic
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'difficulty': 'medium',
    'start_time': None
}

# Scoreboard file path
SCOREBOARD_FILE = Path(__file__).parent / 'scoreboard.json'


def load_scoreboard():
    """Load the scoreboard from file."""
    if SCOREBOARD_FILE.exists():
        try:
            with open(SCOREBOARD_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_scoreboard(scores):
    """Save the scoreboard to file."""
    try:
        with open(SCOREBOARD_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
    except IOError as e:
        print(f"Error saving scoreboard: {e}")


def add_score(name, time_seconds, difficulty):
    """Add a new score to the scoreboard and return top 10."""
    scores = load_scoreboard()
    new_score = {
        'name': name,
        'time': time_seconds,
        'difficulty': difficulty,
        'timestamp': datetime.now().isoformat()
    }
    scores.append(new_score)
    # Sort by time (ascending) and keep top 10
    scores.sort(key=lambda x: x['time'])
    scores = scores[:10]
    save_scoreboard(scores)
    return scores


def validate_board_move(board, row, col, num):
    """Validate if a move is valid on the current board."""
    if not (0 <= row < sudoku_logic.SIZE and 0 <= col < sudoku_logic.SIZE):
        return False
    if num < 1 or num > 9:
        return False
    return sudoku_logic.is_valid_move(board, row, col, num)


@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/new', methods=['GET'])
def new_game():
    """Start a new game with specified difficulty."""
    difficulty = request.args.get('difficulty', 'medium').lower()
    if difficulty not in sudoku_logic.DIFFICULTY_LEVELS:
        difficulty = 'medium'
    
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['difficulty'] = difficulty
    CURRENT['start_time'] = datetime.now().isoformat()
    
    return jsonify({
        'puzzle': puzzle,
        'solution': solution,
        'difficulty': difficulty
    })


@app.route('/validate', methods=['POST'])
def validate_move():
    """Validate a single move without checking full solution."""
    data = request.json
    row = data.get('row')
    col = data.get('col')
    num = data.get('num')
    
    current_board = data.get('board', CURRENT.get('puzzle', []))
    
    if current_board is None:
        return jsonify({'error': 'No game in progress', 'valid': False}), 400
    
    is_valid = validate_board_move(current_board, row, col, num)
    return jsonify({'valid': is_valid})


@app.route('/check', methods=['POST'])
def check_solution():
    """Check the completed solution."""
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    
    completed = len(incorrect) == 0
    response = {'incorrect': incorrect, 'completed': completed}
    
    return jsonify(response)


@app.route('/scoreboard', methods=['GET'])
def get_scoreboard():
    """Get the top 10 scores."""
    scores = load_scoreboard()
    return jsonify({'scores': scores})


@app.route('/scoreboard', methods=['POST'])
def post_score():
    """Add a new score to the scoreboard."""
    data = request.json
    name = data.get('name', 'Anonymous').strip()[:20]  # Max 20 chars
    time_seconds = data.get('time', 0)
    difficulty = data.get('difficulty', 'medium')
    
    if time_seconds < 0 or time_seconds > 3600:  # Max 1 hour
        return jsonify({'error': 'Invalid time'}), 400
    
    scores = add_score(name, time_seconds, difficulty)
    return jsonify({'scores': scores})


@app.route('/difficulties', methods=['GET'])
def get_difficulties():
    """Get available difficulty levels."""
    return jsonify({
        'difficulties': list(sudoku_logic.DIFFICULTY_LEVELS.keys()),
        'levels': sudoku_logic.DIFFICULTY_LEVELS
    })


if __name__ == '__main__':
    app.run(debug=True)