// Global navigation functionality
function showGame(gameId) {
    // Hide all game containers
    const containers = document.querySelectorAll('.game-container');
    containers.forEach(container => container.classList.remove('active'));
    
    // Show selected game
    document.getElementById(gameId).classList.add('active');
    
    // Update navigation buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

// Tic Tac Toe Game
let tttBoard = ['', '', '', '', '', '', '', '', ''];
let tttCurrentPlayer = 'X';
let tttGameActive = true;

const tttWinConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function makeMove(cellIndex) {
    if (tttBoard[cellIndex] !== '' || !tttGameActive) return;
    
    tttBoard[cellIndex] = tttCurrentPlayer;
    document.querySelectorAll('.cell')[cellIndex].textContent = tttCurrentPlayer;
    document.querySelectorAll('.cell')[cellIndex].classList.add('taken');
    
    if (checkTTTWin()) {
        document.getElementById('ttt-status').textContent = `Player ${tttCurrentPlayer} wins! 🎉`;
        tttGameActive = false;
        return;
    }
    
    if (tttBoard.every(cell => cell !== '')) {
        document.getElementById('ttt-status').textContent = "It's a tie! 🤝";
        tttGameActive = false;
        return;
    }
    
    tttCurrentPlayer = tttCurrentPlayer === 'X' ? 'O' : 'X';
    document.getElementById('ttt-status').textContent = `Player ${tttCurrentPlayer}'s turn`;
}

function checkTTTWin() {
    return tttWinConditions.some(condition => {
        return condition.every(index => tttBoard[index] === tttCurrentPlayer);
    });
}

function resetTicTacToe() {
    tttBoard = ['', '', '', '', '', '', '', '', ''];
    tttCurrentPlayer = 'X';
    tttGameActive = true;
    
    document.querySelectorAll('.cell').forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('taken');
    });
    
    document.getElementById('ttt-status').textContent = "Player X's turn";
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
    window.showGame = function(gameId) {
        originalShowGame.call(this, gameId);
        if (gameId === 'number-guess') {
            setTimeout(() => {
                document.getElementById('ng-input').focus();
            }, 100);
        }
    };
});