// Flask Web App Enhanced JavaScript
// API-powered games with Python backend and authentication

// Global state
let currentUser = null;
let isAuthenticated = false;

// Authentication Functions
async function showAuthTab(tabName) {
    const tabs = document.querySelectorAll('.auth-tab');
    const forms = document.querySelectorAll('.auth-form');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    forms.forEach(form => form.classList.remove('active'));
    
    document.querySelector(`.auth-tab:nth-child(${tabName === 'login' ? '1' : '2'})`).classList.add('active');
    document.getElementById(`${tabName}-form`).classList.add('active');
}

async function loginUser() {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    const messageEl = document.getElementById('login-message');
    
    if (!username || !password) {
        showMessage(messageEl, 'Please fill in all fields', 'error');
        return;
    }
    
    const result = await apiCall('/api/auth/login', { username, password });
    
    if (result.success) {
        showMessage(messageEl, result.message, 'success');
        currentUser = result.user;
        isAuthenticated = true;
        showGameArea();
    } else {
        showMessage(messageEl, result.error, 'error');
    }
}

async function signupUser() {
    const username = document.getElementById('signup-username').value.trim();
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm').value;
    const messageEl = document.getElementById('signup-message');
    
    if (!username || !password || !confirmPassword) {
        showMessage(messageEl, 'Please fill in all fields', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showMessage(messageEl, 'Passwords do not match', 'error');
        return;
    }
    
    const result = await apiCall('/api/auth/signup', { username, password });
    
    if (result.success) {
        showMessage(messageEl, result.message + ' You can now login!', 'success');
        // Clear form and switch to login
        document.getElementById('signup-username').value = '';
        document.getElementById('signup-password').value = '';
        document.getElementById('signup-confirm').value = '';
        setTimeout(() => showAuthTab('login'), 2000);
    } else {
        showMessage(messageEl, result.error, 'error');
    }
}

async function logoutUser() {
    await apiCall('/api/auth/logout', {});
    currentUser = null;
    isAuthenticated = false;
    showAuthPanel();
}

function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `auth-message ${type}`;
    element.style.display = 'block';
    
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

function showAuthPanel() {
    document.getElementById('auth-panel').style.display = 'flex';
    document.getElementById('game-area').style.display = 'none';
    
    // Clear forms
    document.getElementById('login-username').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('signup-username').value = '';
    document.getElementById('signup-password').value = '';
    document.getElementById('signup-confirm').value = '';
}

function showGameArea() {
    document.getElementById('auth-panel').style.display = 'none';
    document.getElementById('game-area').style.display = 'block';
    
    // Update user info
    document.getElementById('current-username').textContent = currentUser.username;
    
    // Load user stats
    loadUserStats();
}

async function checkAuthStatus() {
    const result = await apiCall('/api/auth/status');
    
    if (result.authenticated) {
        currentUser = result.user;
        isAuthenticated = true;
        showGameArea();
    } else {
        showAuthPanel();
    }
}

async function loadUserStats() {
    const stats = await apiCall('/api/user/stats');
    if (stats) {
        document.getElementById('user-total-games').textContent = stats.total_games;
        document.getElementById('user-total-wins').textContent = stats.total_wins;
        const winRate = stats.total_games > 0 ? ((stats.total_wins / stats.total_games) * 100).toFixed(1) : 0;
        document.getElementById('user-win-rate').textContent = winRate + '%';
    }
}

// Global navigation functionality
function showGame(gameId) {
    if (!isAuthenticated) {
        showAuthPanel();
        return;
    }
    
    // Hide all game containers
    const containers = document.querySelectorAll('.game-container');
    containers.forEach(container => container.classList.remove('active'));
    
    // Show selected game
    document.getElementById(gameId).classList.add('active');
    
    // Update navigation buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Initialize game when shown
    if (gameId === 'tic-tac-toe') {
        initializeTicTacToe();
    } else if (gameId === 'number-guess') {
        initializeNumberGuess();
    } else if (gameId === 'memory-cards') {
        initializeMemoryCards();
    } else if (gameId === 'scoreboard') {
        showScoreboard('overall');
    }
}

// API Helper function
async function apiCall(endpoint, data = null) {
    const options = {
        method: data ? 'POST' : 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        return { error: 'Network error' };
    }
}

// Tic Tac Toe Game - Flask API Version
async function initializeTicTacToe() {
    const result = await apiCall('/api/tic-tac-toe/start', {});
    
    if (result.board) {
        updateTicTacToeDisplay(result);
    }
}

async function makeMove(cellIndex) {
    const result = await apiCall('/api/tic-tac-toe/move', { position: cellIndex });
    
    if (result.error) {
        console.error(result.error);
        return;
    }
    
    updateTicTacToeDisplay(result);
}

function updateTicTacToeDisplay(gameState) {
    // Update board
    const cells = document.querySelectorAll('.cell');
    gameState.board.forEach((mark, index) => {
        cells[index].textContent = mark;
        cells[index].classList.toggle('taken', mark !== '');
    });
    
    // Update status
    document.getElementById('ttt-status').textContent = gameState.message;
}

function resetTicTacToe() {
    initializeTicTacToe();
}

// Number Guessing Game
let ngSecretNumber = Math.floor(Math.random() * 100) + 1;
let ngAttempts = 0;
let ngGuesses = [];

function makeGuess() {
    const input = document.getElementById('ng-input');
    const guess = parseInt(input.value);
    
    if (isNaN(guess) || guess < 1 || guess > 100) {
        alert('Please enter a valid number between 1 and 100!');
        return;
    }
    
    ngAttempts++;
    ngGuesses.push(guess);
    
    let message = '';
    let historyColor = '';
    
    if (guess === ngSecretNumber) {
        message = `🎉 Congratulations! You guessed it in ${ngAttempts} attempts!`;
        document.getElementById('ng-status').textContent = message;
        input.disabled = true;
        historyColor = 'color: green; font-weight: bold;';
    } else if (guess < ngSecretNumber) {
        message = 'Too low! Try higher 📈';
        historyColor = 'color: blue;';
    } else {
        message = 'Too high! Try lower 📉';
        historyColor = 'color: red;';
    }
    
    document.getElementById('ng-status').textContent = message;
    document.getElementById('ng-attempts').textContent = `Attempts: ${ngAttempts}`;
    
    // Update guess history
    const history = document.getElementById('ng-history');
    history.innerHTML += `<div style="${historyColor}">Guess ${ngAttempts}: ${guess}</div>`;
    
    input.value = '';
    input.focus();
}

function resetNumberGuess() {
    ngSecretNumber = Math.floor(Math.random() * 100) + 1;
    ngAttempts = 0;
    ngGuesses = [];
    
    document.getElementById('ng-input').disabled = false;
    document.getElementById('ng-input').value = '';
    document.getElementById('ng-status').textContent = 'Guess a number between 1 and 100!';
    document.getElementById('ng-attempts').textContent = 'Attempts: 0';
    document.getElementById('ng-history').innerHTML = '';
    document.getElementById('ng-input').focus();
}

// Memory Cards Game
let mcCards = ['🎮', '🎯', '🎲', '🎪', '🎨', '🎭', '🎸', '🎺'];
let mcGameCards = [];
let mcFlippedCards = [];
let mcMatchedPairs = 0;
let mcMoves = 0;
let mcCanFlip = true;

function initializeMemoryCards() {
    // Duplicate cards and shuffle
    mcGameCards = [...mcCards, ...mcCards].sort(() => Math.random() - 0.5);
    
    const board = document.getElementById('mc-board');
    board.innerHTML = '';
    
    mcGameCards.forEach((emoji, index) => {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.dataset.index = index;
        card.dataset.emoji = emoji;
        card.textContent = '?';
        card.addEventListener('click', flipCard);
        board.appendChild(card);
    });
}

function flipCard(event) {
    if (!mcCanFlip) return;
    
    const card = event.target;
    const index = parseInt(card.dataset.index);
    
    if (card.classList.contains('flipped') || card.classList.contains('matched')) return;
    
    card.classList.add('flipped');
    card.textContent = card.dataset.emoji;
    mcFlippedCards.push(card);
    
    if (mcFlippedCards.length === 2) {
        mcCanFlip = false;
        mcMoves++;
        document.getElementById('mc-score').textContent = `Moves: ${mcMoves}`;
        
        setTimeout(() => {
            if (mcFlippedCards[0].dataset.emoji === mcFlippedCards[1].dataset.emoji) {
                // Match found
                mcFlippedCards.forEach(card => {
                    card.classList.add('matched');
                    card.classList.remove('flipped');
                });
                mcMatchedPairs++;
                
                if (mcMatchedPairs === mcCards.length) {
                    document.getElementById('mc-status').textContent = `🎉 You won in ${mcMoves} moves!`;
                }
            } else {
                // No match
                mcFlippedCards.forEach(card => {
                    card.classList.remove('flipped');
                    card.textContent = '?';
                });
            }
            
            mcFlippedCards = [];
            mcCanFlip = true;
        }, 1000);
    }
}

function resetMemoryCards() {
    mcFlippedCards = [];
    mcMatchedPairs = 0;
    mcMoves = 0;
    mcCanFlip = true;
    
    document.getElementById('mc-status').textContent = 'Find all matching pairs!';
    document.getElementById('mc-score').textContent = 'Moves: 0';
    
    initializeMemoryCards();
}

// Event listeners for Enter key
document.addEventListener('DOMContentLoaded', function() {
    // Initialize memory cards game
    initializeMemoryCards();
    
    // Add enter key support for number guessing
    document.getElementById('ng-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            makeGuess();
        }
    });
    
    // Focus on number input when game is shown
    const originalShowGame = showGame;
    // Check authentication on page load
    checkAuthStatus();
    
    // Add Enter key handlers for auth forms
    document.getElementById('login-password').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            loginUser();
        }
    });
    
    document.getElementById('signup-confirm').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            signupUser();
        }
    });
    
    // Show notification that this is Flask-powered
    console.log('🐍 Flask-powered Simple Games Hub with Authentication loaded!');
});

// Scoreboard functionality
async function showScoreboard(gameType) {
    // Update tab selection
    const tabs = document.querySelectorAll('.score-tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Find and activate the correct tab
    const targetTab = Array.from(tabs).find(tab => {
        const tabText = tab.textContent.toLowerCase();
        return (gameType === 'overall' && tabText.includes('overall')) ||
               (gameType === 'tic-tac-toe' && tabText.includes('tic')) ||
               (gameType === 'number-guess' && tabText.includes('number')) ||
               (gameType === 'memory-cards' && tabText.includes('memory'));
    });
    
    if (targetTab) {
        targetTab.classList.add('active');
    }
    
    // Load leaderboard
    try {
        const result = await apiCall(`/api/scoreboard/${gameType}`);
        
        if (result.leaderboard) {
            displayLeaderboard(result.leaderboard, gameType);
        }
        
        // Update user stats
        await loadUserStats();
    } catch (error) {
        console.error('Failed to load scoreboard:', error);
        document.getElementById('leaderboard-content').innerHTML = '<p>Failed to load leaderboard.</p>';
    }
}

function displayLeaderboard(leaderboard, gameType) {
    const leaderboardContent = document.getElementById('leaderboard-content');
    const leaderboardTitle = document.getElementById('leaderboard-title');
    
    // Update title
    const titles = {
        'overall': '🥇 Top Players - Overall',
        'tic-tac-toe': '🎯 Tic Tac Toe Champions',
        'number-guess': '🔢 Number Guessing Masters',
        'memory-cards': '🧠 Memory Cards Experts'
    };
    leaderboardTitle.textContent = titles[gameType] || '🏆 Leaderboard';
    
    if (leaderboard.length === 0) {
        leaderboardContent.innerHTML = '<p>No scores yet. Be the first to play!</p>';
        return;
    }
    
    let html = '';
    leaderboard.forEach((player, index) => {
        const rank = index + 1;
        const emoji = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : '🏅';
        
        let scoreText = '';
        if (gameType === 'overall') {
            scoreText = `${player.total_wins} wins (${player.win_rate.toFixed(1)}%)`;
        } else if (gameType === 'tic-tac-toe') {
            scoreText = `${player.wins}W-${player.draws}D-${player.losses}L`;
        } else if (gameType === 'number-guess') {
            scoreText = `Best: ${player.best_attempts || 'N/A'} attempts`;
        } else if (gameType === 'memory-cards') {
            scoreText = `Best: ${player.best_moves || 'N/A'} moves`;
        }
        
        html += `
            <div class="leaderboard-item">
                <div class="leaderboard-rank">${emoji} ${rank}</div>
                <div class="leaderboard-username">${player.username}</div>
                <div class="leaderboard-score">${scoreText}</div>
            </div>
        `;
    });
    
    leaderboardContent.innerHTML = html;
}