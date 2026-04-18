// Client-side rendering and interaction for the Flask-backed Sudoku Game
const SIZE = 9;
const MINI_BOX = 3;

let puzzle = [];
let currentBoard = [];
let currentSolution = [];
let timerInterval = null;
let startTime = null;
let isGameActive = false;
let currentDifficulty = 'medium';

// ============ Initialization ============

window.addEventListener('load', () => {
  setupEventListeners();
  loadScoreboard();
  applyThemePreference();
  newGame();
});

// ============ Event Listeners ============

function setupEventListeners() {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-button').addEventListener('click', giveHint);
  document.getElementById('clear-board').addEventListener('click', clearBoard);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('save-score').addEventListener('click', saveScore);
  document.getElementById('close-modal').addEventListener('click', () => {
    closeCompletionModal();
    newGame();
  });
  document.getElementById('difficulty-select').addEventListener('change', (e) => {
    currentDifficulty = e.target.value;
  });
}

// ============ Theme Management ============

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  const newTheme = isDark ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeIcon(newTheme);
}

function applyThemePreference() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('.theme-icon');
  icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// ============ Board Creation & Rendering ============

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    
    // Add box highlight class for every 3rd row
    if (i % MINI_BOX === 0 && i !== 0) {
      rowDiv.classList.add('box-border-top');
    }
    
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'numeric';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      
      // Add box highlight class for every 3rd column
      if (j % MINI_BOX === 0 && j !== 0) {
        input.classList.add('box-border-left');
      }
      
      input.addEventListener('input', handleCellInput);
      input.addEventListener('keydown', handleCellKeydown);
      input.addEventListener('blur', () => input.classList.remove('active'));
      input.addEventListener('focus', () => input.classList.add('active'));
      
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  currentBoard = puzzle.map(row => [...row]);
  createBoardElement();
  
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      
      // Store the solution value as a data attribute for hints
      if (currentSolution && currentSolution[i]) {
        inp.dataset.solution = currentSolution[i][j];
      }
      
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.classList.remove('incorrect');
      }
    }
  }
}

// ============ Game Logic ============

async function newGame() {
  try {
    stopTimer();
    clearMessage();
    closeCompletionModal();
    
    const res = await fetch(`/new?difficulty=${currentDifficulty}`);
    const data = await res.json();
    
    currentSolution = data.solution || [];
    renderPuzzle(data.puzzle);
    isGameActive = true;
    startTimer();
    
    // Clear any message
    clearMessage();
  } catch (error) {
    showMessage('Error loading new game', 'error');
    console.error('Error:', error);
  }
}

function handleCellInput(e) {
  // Only allow digits 1-9
  const val = e.target.value.replace(/[^1-9]/g, '');
  e.target.value = val;
  
  if (val) {
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    
    // Update current board
    currentBoard[row][col] = parseInt(val);
    
    // Live validation
    validateCell(e.target);
  } else {
    e.target.classList.remove('incorrect', 'valid');
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    currentBoard[row][col] = 0;
  }
}

function handleCellKeydown(e) {
  if (e.key === 'Backspace' || e.key === 'Delete') {
    e.target.value = '';
    e.target.classList.remove('incorrect', 'valid');
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    currentBoard[row][col] = 0;
  } else if (e.key === 'Enter') {
    // Move to next cell
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    const nextCol = (col + 1) % SIZE;
    const nextRow = row + (col + 1 >= SIZE ? 1 : 0);
    
    if (nextRow < SIZE) {
      const nextCell = document.querySelector(
        `input[data-row="${nextRow}"][data-col="${nextCol}"]`
      );
      if (nextCell) nextCell.focus();
    }
  } else if (e.key === 'ArrowUp' || e.key === 'ArrowDown' || 
             e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
    e.preventDefault();
    handleArrowNavigation(e);
  }
}

function handleArrowNavigation(e) {
  const row = parseInt(e.target.dataset.row);
  const col = parseInt(e.target.dataset.col);
  let newRow = row;
  let newCol = col;
  
  if (e.key === 'ArrowUp') newRow = Math.max(0, row - 1);
  if (e.key === 'ArrowDown') newRow = Math.min(SIZE - 1, row + 1);
  if (e.key === 'ArrowLeft') newCol = Math.max(0, col - 1);
  if (e.key === 'ArrowRight') newCol = Math.min(SIZE - 1, col + 1);
  
  const nextCell = document.querySelector(
    `input[data-row="${newRow}"][data-col="${newCol}"]`
  );
  if (nextCell) nextCell.focus();
}

async function validateCell(input) {
  const row = parseInt(input.dataset.row);
  const col = parseInt(input.dataset.col);
  const num = parseInt(input.value);
  
  if (!num) {
    input.classList.remove('incorrect', 'valid');
    return;
  }
  
  try {
    const res = await fetch('/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        row,
        col,
        num,
        board: currentBoard
      })
    });
    
    const data = await res.json();
    input.classList.remove('incorrect', 'valid');
    if (data.valid) {
      input.classList.add('valid');
    } else {
      input.classList.add('incorrect');
    }
  } catch (error) {
    console.error('Validation error:', error);
  }
}

async function checkSolution() {
  if (!isGameActive) {
    showMessage('Start a new game first', 'error');
    return;
  }
  
  // Get current board state
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val) : 0;
    }
  }
  
  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board })
    });
    
    const data = await res.json();
    
    if (data.error) {
      showMessage(data.error, 'error');
      return;
    }
    
    const incorrect = new Set(data.incorrect.map(x => x[0] * SIZE + x[1]));
    
    // Clear previous highlights
    for (let idx = 0; idx < inputs.length; idx++) {
      const inp = inputs[idx];
      if (!inp.disabled) {
        inp.classList.remove('incorrect', 'valid');
        if (incorrect.has(idx)) {
          inp.classList.add('incorrect');
        }
      }
    }
    
    if (data.completed) {
      isGameActive = false;
      stopTimer();
      const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
      showCompletionModal(elapsedTime);
    } else {
      showMessage(`${incorrect.size} cell(s) incorrect. Keep trying!`, 'error');
    }
  } catch (error) {
    showMessage('Error checking solution', 'error');
    console.error('Error:', error);
  }
}

function clearBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const inp = inputs[idx];
      
      if (!inp.disabled) {
        inp.value = '';
        inp.classList.remove('incorrect', 'valid');
        currentBoard[i][j] = 0;
      }
    }
  }
  
  clearMessage();
}

function giveHint() {
  if (!isGameActive) {
    showMessage('Start a new game first', 'error');
    return;
  }
  
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  
  // Find all empty cells that are not hints
  const emptyCells = [];
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const inp = inputs[idx];
      if (!inp.disabled && inp.value === '' && !inp.classList.contains('hint')) {
        emptyCells.push({ row: i, col: j, idx });
      }
    }
  }
  
  if (emptyCells.length === 0) {
    showMessage('No empty cells remaining!', 'info');
    return;
  }
  
  // Pick a random empty cell
  const hint = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  const hintInput = inputs[hint.idx];
  
  // Get the correct value from the solution
  const correctValue = currentSolution[hint.row][hint.col];
  
  // Fill the cell with the correct answer
  hintInput.value = correctValue;
  hintInput.disabled = true;
  hintInput.classList.add('hint');
  currentBoard[hint.row][hint.col] = correctValue;
  
  showMessage('💡 Hint given! One cell has been filled and locked.', 'success');
}

function getSolutionValue(row, col) {
  // We need to fetch this from the server or store solution locally
  // For now, we'll need to store the solution when we create the puzzle
  return 0;
}

// ============ Timer Management ============

function startTimer() {
  startTime = Date.now();
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  if (timerInterval) clearInterval(timerInterval);
}

function updateTimer() {
  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  const minutes = Math.floor(elapsed / 60);
  const seconds = elapsed % 60;
  document.getElementById('timer').textContent = 
    `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// ============ Message Display ============

function showMessage(text, type = 'info') {
  const msgDiv = document.getElementById('message');
  msgDiv.className = `message ${type}`;
  msgDiv.textContent = text;
  msgDiv.style.display = 'block';
}

function clearMessage() {
  const msgDiv = document.getElementById('message');
  msgDiv.className = 'message';
  msgDiv.style.display = 'none';
}

// ============ Completion Modal ============

function showCompletionModal(elapsedTime) {
  const minutes = Math.floor(elapsedTime / 60);
  const seconds = elapsedTime % 60;
  const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  
  document.getElementById('completion-message').textContent = 
    `You completed the ${currentDifficulty} puzzle in ${timeString}!`;
  document.getElementById('player-name').value = '';
  document.getElementById('completion-modal').classList.remove('hidden');
  document.getElementById('player-name').focus();
}

function closeCompletionModal() {
  document.getElementById('completion-modal').classList.add('hidden');
}

async function saveScore() {
  const playerName = document.getElementById('player-name').value.trim() || 'Anonymous';
  const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
  
  // Create score object
  const newScore = {
    name: playerName,
    time: elapsedTime,
    difficulty: currentDifficulty,
    timestamp: new Date().toISOString()
  };
  
  // Get existing scores from localStorage
  let scores = loadScoresFromStorage();
  
  // Add new score
  scores.push(newScore);
  
  // Sort by time and keep top 10
  scores.sort((a, b) => a.time - b.time);
  scores = scores.slice(0, 10);
  
  // Save to localStorage
  saveScoresToStorage(scores);
  
  // Reload scoreboard display
  loadScoreboard();
  closeCompletionModal();
  showMessage('Score saved! 🎉', 'success');
}

// ============ Scoreboard Management ============

function loadScoresFromStorage() {
  try {
    const stored = localStorage.getItem('sudoku_scores');
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Error loading scores from localStorage:', error);
    return [];
  }
}

function saveScoresToStorage(scores) {
  try {
    localStorage.setItem('sudoku_scores', JSON.stringify(scores));
  } catch (error) {
    console.error('Error saving scores to localStorage:', error);
    showMessage('Could not save score (localStorage full)', 'error');
  }
}

async function loadScoreboard() {
  const scores = loadScoresFromStorage();
  renderScoreboard(scores);
}

function renderScoreboard(scores) {
  const scoreboardDiv = document.getElementById('scoreboard');
  
  if (!scores || scores.length === 0) {
    scoreboardDiv.innerHTML = '<p class="empty-message">No scores yet. Be the first!</p>';
    return;
  }
  
  let html = '<table class="scoreboard-table"><thead><tr><th>Rank</th><th>Name</th><th>Time</th><th>Difficulty</th></tr></thead><tbody>';
  
  scores.forEach((score, index) => {
    const minutes = Math.floor(score.time / 60);
    const seconds = score.time % 60;
    const timeString = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    html += `<tr>
      <td class="rank">${index + 1}</td>
      <td class="name">${escapeHtml(score.name)}</td>
      <td class="time">${timeString}</td>
      <td class="difficulty difficulty-${score.difficulty}">${score.difficulty}</td>
    </tr>`;
  });
  
  html += '</tbody></table>';
  scoreboardDiv.innerHTML = html;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}