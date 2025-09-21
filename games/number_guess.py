"""
Number Guessing Game - Python Version
A console-based number guessing game where players try to guess a secret number.
"""

import os
import random

class NumberGuess:
    def __init__(self):
        self.secret_number = None
        self.attempts = 0
        self.guesses = []
        self.min_number = 1
        self.max_number = 100
        self.game_active = True
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def generate_secret_number(self):
        """Generate a new secret number."""
        self.secret_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        self.guesses = []
        self.game_active = True
    
    def display_header(self):
        """Display the game header."""
        print("\n🔢 NUMBER GUESSING GAME")
        print("=" * 40)
        print(f"🎯 Guess the secret number between {self.min_number} and {self.max_number}!")
        print("=" * 40)
        print()
    
    def display_stats(self):
        """Display current game statistics."""
        print(f"📊 Attempts: {self.attempts}")
        if self.guesses:
            print(f"📝 Previous guesses: {', '.join(map(str, self.guesses))}")
        print()
    
    def get_player_guess(self):
        """Get a valid guess from the player."""
        while True:
            try:
                guess_input = input(f"Enter your guess ({self.min_number}-{self.max_number}) or 'q' to quit: ").strip().lower()
                
                if guess_input == 'q':
                    return None
                
                guess = int(guess_input)
                
                if self.min_number <= guess <= self.max_number:
                    return guess
                else:
                    print(f"❌ Invalid range! Please enter a number between {self.min_number} and {self.max_number}.")
            
            except ValueError:
                print(f"❌ Invalid input! Please enter a number between {self.min_number} and {self.max_number} or 'q' to quit.")
    
    def provide_feedback(self, guess):
        """Provide feedback on the player's guess."""
        difference = abs(guess - self.secret_number)
        
        if guess == self.secret_number:
            return "🎉 Congratulations! You guessed it!", "correct"
        elif guess < self.secret_number:
            if difference <= 5:
                return "📈 Too low! But you're very close! 🔥", "close_low"
            elif difference <= 10:
                return "📈 Too low! Getting warmer! 🌡️", "warm_low"
            else:
                return "📈 Too low! Try higher 🆙", "low"
        else:  # guess > self.secret_number
            if difference <= 5:
                return "📉 Too high! But you're very close! 🔥", "close_high"
            elif difference <= 10:
                return "📉 Too high! Getting warmer! 🌡️", "warm_high"
            else:
                return "📉 Too high! Try lower 🔽", "high"
    
    def display_guess_history(self):
        """Display a formatted guess history with feedback."""
        if not self.guesses:
            return
        
        print("\n📈 Guess History:")
        print("-" * 30)
        for i, guess in enumerate(self.guesses, 1):
            feedback, _ = self.provide_feedback(guess)
            status_icon = "✅" if guess == self.secret_number else "❌"
            print(f"{i:2d}. {guess:3d} {status_icon}")
        print("-" * 30)
    
    def get_difficulty_level(self):
        """Let player choose difficulty level."""
        print("Choose difficulty level:")
        print("1. 🟢 Easy (1-50, unlimited attempts)")
        print("2. 🟡 Medium (1-100, unlimited attempts)")
        print("3. 🔴 Hard (1-200, unlimited attempts)")
        print("4. 🔥 Expert (1-500, unlimited attempts)")
        print()
        
        while True:
            try:
                choice = input("Select difficulty (1-4): ").strip()
                if choice == '1':
                    self.min_number, self.max_number = 1, 50
                    return "Easy"
                elif choice == '2':
                    self.min_number, self.max_number = 1, 100
                    return "Medium"
                elif choice == '3':
                    self.min_number, self.max_number = 1, 200
                    return "Hard"
                elif choice == '4':
                    self.min_number, self.max_number = 1, 500
                    return "Expert"
                else:
                    print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("❌ Invalid input! Please enter a number between 1-4.")
    
    def play(self):
        """Main game loop."""
        while True:
            self.clear_screen()
            print("🔢 NUMBER GUESSING GAME")
            print("=" * 40)
            
            # Choose difficulty
            difficulty = self.get_difficulty_level()
            
            # Generate secret number
            self.generate_secret_number()
            
            print(f"\n🎯 Difficulty: {difficulty}")
            print(f"🎲 Secret number generated! Range: {self.min_number}-{self.max_number}")
            print("💡 Hint: The closer you get, the 'warmer' the feedback!")
            input("\nPress Enter to start guessing...")
            
            # Game loop
            while self.game_active:
                self.clear_screen()
                self.display_header()
                self.display_stats()
                
                if self.guesses:
                    self.display_guess_history()
                
                # Get player guess
                guess = self.get_player_guess()
                
                if guess is None:  # Player wants to quit
                    print(f"\n🎲 The secret number was: {self.secret_number}")
                    return
                
                # Process guess
                self.attempts += 1
                self.guesses.append(guess)
                
                # Provide feedback
                feedback, feedback_type = self.provide_feedback(guess)
                
                if feedback_type == "correct":
                    self.clear_screen()
                    self.display_header()
                    self.display_guess_history()
                    print(f"\n{feedback}")
                    print(f"🏆 You won in {self.attempts} attempts!")
                    
                    # Calculate score based on attempts
                    max_attempts = (self.max_number - self.min_number) // 10 + 5
                    if self.attempts <= max_attempts // 3:
                        print("⭐⭐⭐ EXCELLENT! Outstanding guessing!")
                    elif self.attempts <= max_attempts // 2:
                        print("⭐⭐ GREAT! Well done!")
                    elif self.attempts <= max_attempts:
                        print("⭐ GOOD! Nice work!")
                    else:
                        print("💪 Keep practicing to improve!")
                    
                    self.game_active = False
                else:
                    print(f"\n{feedback}")
                    input("Press Enter to continue...")
            
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
    game = NumberGuess()
    game.play()