"""
Memory Cards Game - Python Version
A console-based memory matching game where players flip cards to find matching pairs.
"""

import os
import random
import time

class MemoryCards:
    def __init__(self):
        self.cards = ['🎮', '🎯', '🎲', '🎪', '🎨', '🎭', '🎸', '🎺']
        self.game_cards = []
        self.revealed_positions = []
        self.matched_pairs = []
        self.moves = 0
        self.current_flipped = []
        self.game_active = True
        self.board_size = 4  # 4x4 grid
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def initialize_game(self):
        """Initialize a new game with shuffled cards."""
        # Create pairs and shuffle
        self.game_cards = (self.cards + self.cards)[:16]  # Ensure we have exactly 16 cards
        random.shuffle(self.game_cards)
        
        # Reset game state
        self.revealed_positions = []
        self.matched_pairs = []
        self.moves = 0
        self.current_flipped = []
        self.game_active = True
    
    def display_header(self):
        """Display the game header."""
        print("\n🧠 MEMORY CARDS GAME")
        print("=" * 40)
        print("🎯 Find all matching pairs!")
        print("=" * 40)
        print()
    
    def display_board(self):
        """Display the current game board."""
        print("   ", end="")
        for col in range(self.board_size):
            print(f"  {col+1} ", end="")
        print()
        
        for row in range(self.board_size):
            print(f" {row+1} ", end="")
            for col in range(self.board_size):
                position = row * self.board_size + col
                
                if position in self.matched_pairs:
                    # Show matched cards
                    print(f" {self.game_cards[position]} ", end="")
                elif position in self.current_flipped:
                    # Show currently flipped cards
                    print(f" {self.game_cards[position]} ", end="")
                else:
                    # Show hidden cards
                    print(" ? ", end="")
            print()
        print()
    
    def display_stats(self):
        """Display current game statistics."""
        matched_count = len(self.matched_pairs) // 2
        total_pairs = len(self.game_cards) // 2
        print(f"📊 Moves: {self.moves}")
        print(f"🎯 Matched pairs: {matched_count}/{total_pairs}")
        print()
    
    def get_position_input(self, prompt):
        """Get a valid position from user input."""
        while True:
            try:
                user_input = input(prompt).strip().lower()
                
                if user_input == 'q':
                    return None
                
                if ',' in user_input:
                    row_str, col_str = user_input.split(',')
                    row = int(row_str.strip()) - 1
                    col = int(col_str.strip()) - 1
                elif len(user_input) == 2:
                    row = int(user_input[0]) - 1
                    col = int(user_input[1]) - 1
                else:
                    print("❌ Invalid format! Use 'row,col' (e.g., '2,3') or 'rowcol' (e.g., '23')")
                    continue
                
                if 0 <= row < self.board_size and 0 <= col < self.board_size:
                    position = row * self.board_size + col
                    return position
                else:
                    print(f"❌ Position out of bounds! Use rows 1-{self.board_size} and columns 1-{self.board_size}.")
                    
            except (ValueError, IndexError):
                print("❌ Invalid input! Use format 'row,col' (e.g., '2,3') or 'q' to quit.")
    
    def is_valid_move(self, position):
        """Check if the move is valid."""
        if position in self.matched_pairs:
            print("❌ That card is already matched!")
            return False
        if position in self.current_flipped:
            print("❌ That card is already flipped!")
            return False
        return True
    
    def check_for_match(self):
        """Check if the two flipped cards match."""
        if len(self.current_flipped) == 2:
            pos1, pos2 = self.current_flipped
            if self.game_cards[pos1] == self.game_cards[pos2]:
                # Match found!
                self.matched_pairs.extend(self.current_flipped)
                print(f"🎉 Match found! {self.game_cards[pos1]} = {self.game_cards[pos2]}")
                return True
            else:
                # No match
                print(f"❌ No match: {self.game_cards[pos1]} ≠ {self.game_cards[pos2]}")
                return False
        return False
    
    def is_game_won(self):
        """Check if all pairs have been matched."""
        return len(self.matched_pairs) == len(self.game_cards)
    
    def calculate_score(self):
        """Calculate and display the final score."""
        total_pairs = len(self.game_cards) // 2
        min_moves = total_pairs  # Theoretical minimum
        
        if self.moves <= min_moves + 2:
            return "⭐⭐⭐ PERFECT! Outstanding memory!"
        elif self.moves <= min_moves + 5:
            return "⭐⭐ EXCELLENT! Great job!"
        elif self.moves <= min_moves + 10:
            return "⭐ GOOD! Well done!"
        else:
            return "💪 Keep practicing to improve your memory!"
    
    def play(self):
        """Main game loop."""
        while True:
            # Initialize new game
            self.initialize_game()
            
            print("🧠 MEMORY CARDS GAME")
            print("=" * 40)
            print("📋 Instructions:")
            print("• Find all matching pairs of cards")
            print("• Enter positions as 'row,col' (e.g., '2,3') or 'rowcol' (e.g., '23')")
            print("• Cards are numbered 1-4 for both rows and columns")
            print("• Type 'q' to quit at any time")
            print()
            input("Press Enter to start...")
            
            # Main game loop
            while self.game_active:
                self.clear_screen()
                self.display_header()
                self.display_board()
                self.display_stats()
                
                if self.is_game_won():
                    print("🏆 CONGRATULATIONS! You found all pairs!")
                    print(f"🎯 Final score: {self.moves} moves")
                    print(self.calculate_score())
                    break
                
                # Get first card
                if len(self.current_flipped) == 0:
                    print("Select the first card:")
                    position1 = self.get_position_input("Enter position (row,col) or 'q' to quit: ")
                    
                    if position1 is None:
                        return
                    
                    if not self.is_valid_move(position1):
                        input("Press Enter to continue...")
                        continue
                    
                    self.current_flipped.append(position1)
                    
                    # Show the first card
                    self.clear_screen()
                    self.display_header()
                    self.display_board()
                    self.display_stats()
                
                # Get second card
                print("Select the second card:")
                position2 = self.get_position_input("Enter position (row,col) or 'q' to quit: ")
                
                if position2 is None:
                    return
                
                if not self.is_valid_move(position2):
                    input("Press Enter to continue...")
                    self.current_flipped = []  # Reset if invalid move
                    continue
                
                self.current_flipped.append(position2)
                self.moves += 1
                
                # Show both cards
                self.clear_screen()
                self.display_header()
                self.display_board()
                self.display_stats()
                
                # Check for match
                if self.check_for_match():
                    input("Press Enter to continue...")
                else:
                    input("Press Enter to flip cards back...")
                
                # Reset current flipped cards
                self.current_flipped = []
            
            # Ask if player wants to play again
            while True:
                play_again = input("\n🔄 Do you want to play again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    return
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    game = MemoryCards()
    game.play()