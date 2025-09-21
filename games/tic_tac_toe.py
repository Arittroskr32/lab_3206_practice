"""
Tic Tac Toe Game - Python Version
A console-based implementation of the classic Tic Tac Toe game.
"""

import os

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board represented as 1D list
        self.current_player = 'X'
        self.game_active = True
        self.win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_board(self):
        """Display the current game board."""
        print("\n🎯 TIC TAC TOE")
        print("=" * 30)
        print()
        print("   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   ")
        print()
        
        # Display position guide
        print("Position guide:")
        print("   |   |   ")
        print(" 1 | 2 | 3 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 4 | 5 | 6 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 7 | 8 | 9 ")
        print("   |   |   ")
        print()
    
    def make_move(self, position):
        """Make a move at the given position."""
        if self.board[position] != ' ' or not self.game_active:
            return False
        
        self.board[position] = self.current_player
        return True
    
    def check_win(self):
        """Check if current player has won."""
        for condition in self.win_conditions:
            if all(self.board[pos] == self.current_player for pos in condition):
                return True
        return False
    
    def check_tie(self):
        """Check if the game is a tie."""
        return ' ' not in self.board
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_player_move(self):
        """Get valid move from player."""
        while True:
            try:
                move = input(f"Player {self.current_player}, enter position (1-9) or 'q' to quit: ").strip().lower()
                
                if move == 'q':
                    return None
                
                position = int(move) - 1  # Convert to 0-based index
                
                if 0 <= position <= 8:
                    if self.board[position] == ' ':
                        return position
                    else:
                        print("❌ That position is already taken! Choose another.")
                else:
                    print("❌ Invalid position! Please enter a number between 1-9.")
            
            except ValueError:
                print("❌ Invalid input! Please enter a number between 1-9 or 'q' to quit.")
    
    def reset_game(self):
        """Reset the game for a new round."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_active = True
    
    def play(self):
        """Main game loop."""
        while True:
            self.clear_screen()
            self.display_board()
            
            if not self.game_active:
                break
            
            print(f"Current player: {self.current_player}")
            
            # Get player move
            move = self.get_player_move()
            
            if move is None:  # Player wants to quit
                break
            
            # Make the move
            if self.make_move(move):
                # Check for win
                if self.check_win():
                    self.clear_screen()
                    self.display_board()
                    print(f"🎉 Player {self.current_player} wins! Congratulations!")
                    self.game_active = False
                # Check for tie
                elif self.check_tie():
                    self.clear_screen()
                    self.display_board()
                    print("🤝 It's a tie! Good game!")
                    self.game_active = False
                else:
                    # Switch players
                    self.switch_player()
            else:
                print("❌ Invalid move! Try again.")
                input("Press Enter to continue...")
            
            # Ask if players want to play again
            if not self.game_active:
                while True:
                    play_again = input("\n🔄 Do you want to play again? (y/n): ").strip().lower()
                    if play_again in ['y', 'yes']:
                        self.reset_game()
                        break
                    elif play_again in ['n', 'no']:
                        return
                    else:
                        print("❌ Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    game = TicTacToe()
    game.play()