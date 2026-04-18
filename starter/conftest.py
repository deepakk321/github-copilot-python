"""Pytest configuration and shared fixtures."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import app and sudoku_logic
sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture
def app():
    """Create Flask app for testing."""
    import app as app_module
    app_module.app.config['TESTING'] = True
    return app_module.app


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """Create Flask app context."""
    with app.app_context():
        yield app
