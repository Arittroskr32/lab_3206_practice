# Simple Games Hub - Python Web App

A collection of games available in both web and console versions. Features a Flask-powered web application with Python backend API and original HTML/CSS/JavaScript frontend. This project includes three classic games: Tic Tac Toe, Number Guessing, and Memory Cards.

## 🎮 Games Included

### 1. 🎯 Tic Tac Toe
- Classic 3x3 grid game
- Two-player gameplay (X vs O)
- Win by getting three in a row (horizontally, vertically, or diagonally)
- Input positions using numbers 1-9

### 2. 🔢 Number Guessing
- Guess the secret number within a range
- Multiple difficulty levels (Easy: 1-50, Medium: 1-100, Hard: 1-200, Expert: 1-500)
- Intelligent feedback system with "warm/cold" hints
- Track your guesses and attempts
- Score based on number of attempts

### 3. 🧠 Memory Cards
- Match pairs of emoji cards
- 4x4 grid with 8 different card types
- Remember card positions to find matching pairs
- Score based on number of moves
- Input positions using row,col format (e.g., "2,3")

## 🚀 How to Run

### Prerequisites
- Python 3.6 or higher
- Flask (install with `pip install -r requirements.txt`)

### Running the Web Application

1. **Navigate to the project directory:**
   ```bash
   cd path/to/your/project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask web app:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

### Running Console Version

1. **Run the console game hub:**
   ```bash
   python main.py
   ```

2. **Or run individual games directly:**
   ```bash
   # Tic Tac Toe
   python games/tic_tac_toe.py
   
   # Number Guessing
   python games/number_guess.py
   
   # Memory Cards
   python games/memory_cards.py
   ```

## 🎯 Game Controls

### Tic Tac Toe
- Enter numbers 1-9 to place your mark
- Numbers correspond to board positions:
  ```
  1 | 2 | 3
  4 | 5 | 6  
  7 | 8 | 9
  ```
- Type 'q' to quit

### Number Guessing
- Enter numbers within the chosen difficulty range
- Follow the feedback hints (too high/low, warm/cold)
- Type 'q' to quit

### Memory Cards
- Enter positions as "row,col" (e.g., "2,3") or "rowcol" (e.g., "23")
- Positions are numbered 1-4 for both rows and columns
- Type 'q' to quit

## 📂 Project Structure

```
.
├── app.py               # Flask web application entry point
├── main.py              # Console game hub entry point
├── games/               # Console games package directory
│   ├── __init__.py     # Package initialization
│   ├── tic_tac_toe.py  # Tic Tac Toe console game
│   ├── number_guess.py # Number guessing console game
│   └── memory_cards.py # Memory cards console game
├── templates/           # Flask HTML templates
│   └── index.html      # Main web interface
├── static/              # Static web assets
│   ├── script.js       # Enhanced JavaScript with Flask API calls
│   └── style.css       # Game styling
├── requirements.txt     # Python dependencies (including Flask)
└── README.md           # This file
```

## 🆕 Features

### 🌐 Web Application (Flask)
- **API-Powered Games**: Backend Python logic with frontend JavaScript
- **Session Management**: Game state preserved across moves
- **Real-time Updates**: Seamless game experience in the browser
- **Responsive Design**: Works on desktop and mobile devices

### 🖥️ Console Version
- **Enhanced Number Guessing**: Multiple difficulty levels, proximity hints
- **Improved Memory Cards**: Clear interface, better position input
- **Better UX**: Consistent navigation, graceful exits, cross-platform support

### 🎯 Game Features
- **Tic Tac Toe**: Smart move validation, win detection
- **Number Guessing**: Intelligent feedback system, score tracking
- **Memory Cards**: Card matching with move optimization

## 🔧 Development

### Adding Web API Endpoints
1. Add new route in `app.py` with `@app.route()` decorator
2. Update JavaScript in `static/script.js` to call new endpoint
3. Test API with browser developer tools

### Adding Console Games
1. Create new game file in `games/` directory
2. Follow existing structure with `play()` method
3. Import and add to `main.py`

### Code Style
- Follow PEP 8 Python style guidelines
- Use clear, descriptive variable names
- Include docstrings for all classes and methods
- Handle user input gracefully

## � Web vs Console

### Web Version Benefits
- Beautiful visual interface
- Mouse/touch interaction
- No installation required (just open browser)
- Modern web technologies

### Console Version Benefits
- Works anywhere Python runs
- No web browser required
- Lightweight and fast
- Great for terminal enthusiasts

## 🤝 Contributing

Feel free to contribute by:
- Adding new games
- Improving existing game features
- Enhancing the user interface
- Fixing bugs or improving error handling

## 📄 License

This project is open source and available under the MIT License.

## 🎮 Have Fun!

Enjoy playing these classic games in your terminal! Each game is designed to be engaging while maintaining simplicity and ease of use.