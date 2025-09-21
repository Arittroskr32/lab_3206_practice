"""
Flask Web Application for Simple Games Hub
A web-based version of the games using Python Flask backend with authentication.
"""

from flask import Flask, render_template, request, jsonify, session
import random
import os
from auth import UserManager, login_required

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-please-change-this'

# Initialize user manager
user_manager = UserManager()

class GameState:
    """Manage game states in session"""
    
    @staticmethod
    def init_tic_tac_toe():
        session['ttt_board'] = ['' for _ in range(9)]
        session['ttt_current_player'] = 'X'
        session['ttt_game_active'] = True
        return session['ttt_board']
    
    @staticmethod
    def init_number_guess():
        session['ng_secret_number'] = random.randint(1, 100)
        session['ng_attempts'] = 0
        session['ng_guesses'] = []
        return {'message': 'New game started! Guess a number between 1 and 100.'}
    
    @staticmethod
    def init_memory_cards():
        cards = ['🎮', '🎯', '🎲', '🎪', '🎨', '🎭', '🎸', '🎺']
        game_cards = (cards + cards)
        random.shuffle(game_cards)
        session['mc_cards'] = game_cards
        session['mc_revealed'] = []
        session['mc_matched'] = []
        session['mc_moves'] = 0
        return game_cards

# Authentication Routes
@app.route('/')
def index():
    """Main page with game selection"""
    return render_template('index.html')

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    success, message = user_manager.authenticate_user(username, password)
    
    if success:
        session['username'] = username
        user_stats = user_manager.get_user_stats(username)
        return jsonify({
            'success': True,
            'message': message,
            'user': user_stats
        })
    else:
        return jsonify({'error': message}), 401

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    success, message = user_manager.register_user(username, password)
    
    if success:
        return jsonify({
            'success': True,
            'message': message
        })
    else:
        return jsonify({'error': message}), 400

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    session.pop('username', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    if 'username' in session:
        user_stats = user_manager.get_user_stats(session['username'])
        return jsonify({
            'authenticated': True,
            'user': user_stats
        })
    else:
        return jsonify({'authenticated': False})

# Scoreboard Routes
@app.route('/api/scoreboard/<game_name>')
@login_required
def get_leaderboard(game_name):
    """Get leaderboard for specific game or overall"""
    if game_name == 'overall':
        leaderboard = user_manager.get_leaderboard()
    else:
        leaderboard = user_manager.get_leaderboard(game_name)
    
    return jsonify({'leaderboard': leaderboard})

@app.route('/api/user/stats')
@login_required
def get_user_stats():
    """Get current user statistics"""
    username = session['username']
    stats = user_manager.get_user_stats(username)
    return jsonify(stats)

@app.route('/api/tic-tac-toe/start', methods=['POST'])
@login_required
def start_tic_tac_toe():
    """Initialize a new Tic Tac Toe game"""
    board = GameState.init_tic_tac_toe()
    return jsonify({
        'board': board,
        'current_player': session['ttt_current_player'],
        'game_active': session['ttt_game_active'],
        'message': "Player X's turn"
    })

@app.route('/api/tic-tac-toe/move', methods=['POST'])
@login_required
def make_tic_tac_toe_move():
    """Make a move in Tic Tac Toe"""
    data = request.get_json()
    position = data.get('position')
    
    if not session.get('ttt_game_active', False):
        return jsonify({'error': 'Game not active'})
    
    if session['ttt_board'][position] != '':
        return jsonify({'error': 'Position already taken'})
    
    # Make move
    session['ttt_board'][position] = session['ttt_current_player']
    
    # Check win conditions
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    # Check for win
    for condition in win_conditions:
        if all(session['ttt_board'][pos] == session['ttt_current_player'] for pos in condition):
            session['ttt_game_active'] = False
            
            # Record score - user wins if they're X, loses if they're O (assuming X is user)
            username = session['username']
            result = 'win' if session['ttt_current_player'] == 'X' else 'loss'
            user_manager.update_game_score(username, 'tic_tac_toe', {'result': result})
            
            return jsonify({
                'board': session['ttt_board'],
                'current_player': session['ttt_current_player'],
                'game_active': False,
                'message': f"Player {session['ttt_current_player']} wins! 🎉",
                'winner': session['ttt_current_player']
            })
    
    # Check for tie
    if '' not in session['ttt_board']:
        session['ttt_game_active'] = False
        
        # Record tie
        username = session['username']
        user_manager.update_game_score(username, 'tic_tac_toe', {'result': 'draw'})
        
        return jsonify({
            'board': session['ttt_board'],
            'current_player': session['ttt_current_player'],
            'game_active': False,
            'message': "It's a tie! 🤝",
            'tie': True
        })
    
    # Switch players
    session['ttt_current_player'] = 'O' if session['ttt_current_player'] == 'X' else 'X'
    
    return jsonify({
        'board': session['ttt_board'],
        'current_player': session['ttt_current_player'],
        'game_active': session['ttt_game_active'],
        'message': f"Player {session['ttt_current_player']}'s turn"
    })

@app.route('/api/number-guess/start', methods=['POST'])
@login_required
def start_number_guess():
    """Initialize a new Number Guessing game"""
    result = GameState.init_number_guess()
    return jsonify(result)

@app.route('/api/number-guess/guess', methods=['POST'])
@login_required
def make_number_guess():
    """Make a guess in the Number Guessing game"""
    data = request.get_json()
    guess = data.get('guess')
    
    if not isinstance(guess, int) or guess < 1 or guess > 100:
        return jsonify({'error': 'Invalid guess. Please enter a number between 1 and 100.'})
    
    session['ng_attempts'] += 1
    session['ng_guesses'].append(guess)
    
    secret = session['ng_secret_number']
    
    if guess == secret:
        # Record win score
        username = session['username']
        user_manager.update_game_score(username, 'number_guess', {
            'attempts': session['ng_attempts'],
            'won': True
        })
        
        return jsonify({
            'message': f'🎉 Congratulations! You guessed it in {session["ng_attempts"]} attempts!',
            'correct': True,
            'attempts': session['ng_attempts'],
            'guesses': session['ng_guesses']
        })
    elif guess < secret:
        return jsonify({
            'message': 'Too low! Try higher 📈',
            'correct': False,
            'attempts': session['ng_attempts'],
            'guesses': session['ng_guesses']
        })
    else:
        return jsonify({
            'message': 'Too high! Try lower 📉',
            'correct': False,
            'attempts': session['ng_attempts'],
            'guesses': session['ng_guesses']
        })

@app.route('/api/memory-cards/start', methods=['POST'])
@login_required
def start_memory_cards():
    """Initialize a new Memory Cards game"""
    cards = GameState.init_memory_cards()
    return jsonify({
        'cards': cards,
        'moves': session['mc_moves'],
        'message': 'Find all matching pairs!'
    })

@app.route('/api/memory-cards/complete', methods=['POST'])
@login_required
def complete_memory_cards():
    """Record memory cards game completion"""
    data = request.get_json()
    moves = data.get('moves', 0)
    
    # Record completion score
    username = session['username']
    user_manager.update_game_score(username, 'memory_cards', {
        'moves': moves
    })
    
    return jsonify({
        'success': True,
        'message': f'Game completed in {moves} moves!'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)