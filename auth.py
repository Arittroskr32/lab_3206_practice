"""
User Authentication and Score Management System
Handles user registration, login, and score tracking with local file storage.
"""

import json
import hashlib
import os
from datetime import datetime
from functools import wraps
from flask import session, request, jsonify

class UserManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.scores_file = os.path.join(data_dir, 'scores.json')
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory and files if they don't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump({}, f)
    
    def hash_password(self, password):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def load_users(self):
        """Load users from JSON file."""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_users(self, users):
        """Save users to JSON file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_scores(self):
        """Load scores from JSON file."""
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_scores(self, scores):
        """Save scores to JSON file."""
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=2)
    
    def register_user(self, username, password):
        """Register a new user."""
        users = self.load_users()
        
        if username in users:
            return False, "Username already exists"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        users[username] = {
            'password_hash': self.hash_password(password),
            'created_at': datetime.now().isoformat(),
            'total_games': 0,
            'total_wins': 0
        }
        
        self.save_users(users)
        
        # Initialize user scores
        scores = self.load_scores()
        scores[username] = {
            'tic_tac_toe': {'games': 0, 'wins': 0, 'draws': 0, 'losses': 0},
            'number_guess': {'games': 0, 'best_attempts': None, 'total_attempts': 0},
            'memory_cards': {'games': 0, 'best_moves': None, 'total_moves': 0}
        }
        self.save_scores(scores)
        
        return True, "User registered successfully"
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials."""
        users = self.load_users()
        
        if username not in users:
            return False, "Invalid username or password"
        
        if users[username]['password_hash'] != self.hash_password(password):
            return False, "Invalid username or password"
        
        return True, "Authentication successful"
    
    def get_user_stats(self, username):
        """Get user statistics."""
        users = self.load_users()
        scores = self.load_scores()
        
        if username not in users:
            return None
        
        user_data = users[username]
        user_scores = scores.get(username, {})
        
        return {
            'username': username,
            'member_since': user_data['created_at'],
            'total_games': user_data['total_games'],
            'total_wins': user_data['total_wins'],
            'scores': user_scores
        }
    
    def update_game_score(self, username, game_name, score_data):
        """Update user's game score."""
        users = self.load_users()
        scores = self.load_scores()
        
        if username not in users or username not in scores:
            return False
        
        # Update game-specific scores
        if game_name == 'tic_tac_toe':
            scores[username]['tic_tac_toe']['games'] += 1
            if score_data['result'] == 'win':
                scores[username]['tic_tac_toe']['wins'] += 1
                users[username]['total_wins'] += 1
            elif score_data['result'] == 'draw':
                scores[username]['tic_tac_toe']['draws'] += 1
            else:
                scores[username]['tic_tac_toe']['losses'] += 1
        
        elif game_name == 'number_guess':
            scores[username]['number_guess']['games'] += 1
            attempts = score_data['attempts']
            scores[username]['number_guess']['total_attempts'] += attempts
            
            if score_data['won']:
                users[username]['total_wins'] += 1
                current_best = scores[username]['number_guess']['best_attempts']
                if current_best is None or attempts < current_best:
                    scores[username]['number_guess']['best_attempts'] = attempts
        
        elif game_name == 'memory_cards':
            scores[username]['memory_cards']['games'] += 1
            moves = score_data['moves']
            scores[username]['memory_cards']['total_moves'] += moves
            users[username]['total_wins'] += 1  # Completing the game is a win
            
            current_best = scores[username]['memory_cards']['best_moves']
            if current_best is None or moves < current_best:
                scores[username]['memory_cards']['best_moves'] = moves
        
        # Update total games
        users[username]['total_games'] += 1
        
        self.save_users(users)
        self.save_scores(scores)
        return True
    
    def get_leaderboard(self, game_name=None):
        """Get leaderboard for all games or specific game."""
        scores = self.load_scores()
        users = self.load_users()
        
        if game_name:
            # Game-specific leaderboard
            leaderboard = []
            for username, user_scores in scores.items():
                if game_name in user_scores and user_scores[game_name]['games'] > 0:
                    game_data = user_scores[game_name].copy()
                    game_data['username'] = username
                    leaderboard.append(game_data)
            
            # Sort based on game type
            if game_name == 'tic_tac_toe':
                leaderboard.sort(key=lambda x: (x['wins'], -x['losses']), reverse=True)
            elif game_name == 'number_guess':
                leaderboard.sort(key=lambda x: (x['games'], -(x['best_attempts'] or 999)))
            elif game_name == 'memory_cards':
                leaderboard.sort(key=lambda x: (x['games'], -(x['best_moves'] or 999)))
            
            return leaderboard[:10]  # Top 10
        
        else:
            # Overall leaderboard
            leaderboard = []
            for username, user_data in users.items():
                leaderboard.append({
                    'username': username,
                    'total_games': user_data['total_games'],
                    'total_wins': user_data['total_wins'],
                    'win_rate': (user_data['total_wins'] / user_data['total_games'] * 100) if user_data['total_games'] > 0 else 0
                })
            
            leaderboard.sort(key=lambda x: (x['total_wins'], x['win_rate']), reverse=True)
            return leaderboard[:10]  # Top 10

def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function