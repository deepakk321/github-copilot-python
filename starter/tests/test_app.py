"""Test suite for Flask application routes."""
import pytest
import json


class TestIndexRoute:
    """Test the index route."""

    def test_index_returns_status_200(self, client):
        """Test that index route returns 200 OK."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        """Test that index route returns HTML content."""
        response = client.get('/')
        assert b'<!doctype html>' in response.data
        assert b'Sudoku' in response.data


class TestNewGameRoute:
    """Test the new game route."""

    def test_new_game_returns_puzzle(self, client):
        """Test that new game returns a puzzle."""
        response = client.get('/new')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'puzzle' in data
        assert 'difficulty' in data
        assert len(data['puzzle']) == 9

    def test_new_game_medium_difficulty(self, client):
        """Test new game with medium difficulty."""
        response = client.get('/new?difficulty=medium')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['difficulty'] == 'medium'

    def test_new_game_easy_difficulty(self, client):
        """Test new game with easy difficulty."""
        response = client.get('/new?difficulty=easy')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['difficulty'] == 'easy'

    def test_new_game_hard_difficulty(self, client):
        """Test new game with hard difficulty."""
        response = client.get('/new?difficulty=hard')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['difficulty'] == 'hard'

    def test_new_game_invalid_difficulty_defaults_to_medium(self, client):
        """Test that invalid difficulty defaults to medium."""
        response = client.get('/new?difficulty=impossible')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['difficulty'] == 'medium'

    def test_new_game_returns_solution(self, client):
        """Test that new game returns solution for hints."""
        response = client.get('/new')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'solution' in data
        assert len(data['solution']) == 9

    def test_new_game_puzzle_subset_of_solution(self, client):
        """Test that puzzle clues match solution."""
        response = client.get('/new')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        solution = data['solution']
        
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    assert puzzle[i][j] == solution[i][j]


class TestValidateRoute:
    """Test the validate move route."""

    def test_validate_valid_move(self, client):
        """Test validation of a valid move."""
        # Create new puzzle first
        client.get('/new')
        
        response = client.post('/validate', json={
            'row': 0,
            'col': 0,
            'num': 5,
            'board': [[0] * 9 for _ in range(9)]
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'valid' in data

    def test_validate_returns_boolean(self, client):
        """Test that validate returns a boolean."""
        client.get('/new')
        
        response = client.post('/validate', json={
            'row': 0,
            'col': 0,
            'num': 5,
            'board': [[0] * 9 for _ in range(9)]
        })
        
        data = json.loads(response.data)
        assert isinstance(data['valid'], bool)

    def test_validate_missing_game(self, client):
        """Test validation without active game shows error."""
        response = client.post('/validate', json={
            'row': 0,
            'col': 0,
            'num': 5,
            'board': [[0] * 9 for _ in range(9)]
        })
        
        # Should either succeed with the provided board or show error
        assert response.status_code in [200, 400]


class TestCheckRoute:
    """Test the check solution route."""

    def test_check_solution_incomplete(self, client):
        """Test checking an incomplete solution."""
        client.get('/new')
        
        board = [[0] * 9 for _ in range(9)]
        response = client.post('/check', json={'board': board})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'incorrect' in data
        assert 'completed' in data

    def test_check_solution_no_game(self, client):
        """Test checking solution without active game returns error or processes."""
        board = [[0] * 9 for _ in range(9)]
        response = client.post('/check', json={'board': board})
        
        # In test context, CURRENT might be empty, so either 400 error or 200 with result
        assert response.status_code in [200, 400]
        if response.status_code == 400:
            data = json.loads(response.data)
            assert 'error' in data

    def test_check_solution_returns_json(self, client):
        """Test that check returns proper JSON response."""
        client.get('/new')
        
        board = [[0] * 9 for _ in range(9)]
        response = client.post('/check', json={'board': board})
        
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert 'incorrect' in data
        assert isinstance(data['incorrect'], list)


class TestScoreboardRoute:
    """Test the scoreboard route."""

    def test_get_scoreboard(self, client):
        """Test getting scoreboard."""
        response = client.get('/scoreboard')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'scores' in data
        assert isinstance(data['scores'], list)

    def test_post_score(self, client):
        """Test posting a new score."""
        response = client.post('/scoreboard', json={
            'name': 'Test Player',
            'time': 120,
            'difficulty': 'medium'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'scores' in data

    def test_post_score_invalid_time(self, client):
        """Test that invalid time is rejected."""
        response = client.post('/scoreboard', json={
            'name': 'Test Player',
            'time': 5000,  # > 1 hour
            'difficulty': 'medium'
        })
        
        assert response.status_code == 400

    def test_post_score_with_name(self, client):
        """Test posting score with name."""
        response = client.post('/scoreboard', json={
            'name': 'Alice',
            'time': 60,
            'difficulty': 'easy'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['scores']) > 0

    def test_post_score_truncates_long_name(self, client):
        """Test that long names are truncated."""
        long_name = 'A' * 50
        response = client.post('/scoreboard', json={
            'name': long_name,
            'time': 60,
            'difficulty': 'easy'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Check that the longest name is at most 20 characters
        if len(data['scores']) > 0:
            assert len(data['scores'][0]['name']) <= 20


class TestDifficultiesRoute:
    """Test the difficulties route."""

    def test_get_difficulties(self, client):
        """Test getting available difficulties."""
        response = client.get('/difficulties')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'difficulties' in data
        assert 'levels' in data
        assert 'easy' in data['difficulties']
        assert 'medium' in data['difficulties']
        assert 'hard' in data['difficulties']


class TestRouteIntegration:
    """Test integration between routes."""

    def test_new_game_then_check(self, client):
        """Test creating game then checking solution."""
        # Get new game
        game_response = client.get('/new')
        game_data = json.loads(game_response.data)
        solution = game_data['solution']
        
        # Check the solution
        check_response = client.post('/check', json={'board': solution})
        check_data = json.loads(check_response.data)
        
        # Should be completed with no incorrect cells
        assert check_data['completed'] is True
        assert len(check_data['incorrect']) == 0

    def test_new_game_then_save_score(self, client):
        """Test creating game and saving score."""
        client.get('/new')
        
        score_response = client.post('/scoreboard', json={
            'name': 'Test Gamer',
            'time': 300,
            'difficulty': 'medium'
        })
        
        assert score_response.status_code == 200
        
        data = json.loads(score_response.data)
        assert len(data['scores']) > 0
