#!/usr/bin/env python3
"""
Simple Games Hub - Python Version
A collection of console-based games including Tic Tac Toe, Number Guessing, and Memory Cards.
"""

import os
import sys
from games.tic_tac_toe import TicTacToe
from games.number_guess import NumberGuess
from games.memory_cards import MemoryCards

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the main header."""
    print("=" * 50)
    print("🎮 SIMPLE GAMES HUB - PYTHON VERSION 🎮")
    print("=" * 50)
    print()

def display_menu():
    """Display the main menu options."""
    print("Choose a game to play:")
    print()
    print("1. 🎯 Tic Tac Toe")
    print("   Classic 3x3 grid game. Get three in a row to win!")
    print()
    print("2. 🔢 Number Guessing")
    print("   Guess the secret number between 1 and 100!")
    print()
    print("3. 🧠 Memory Cards")
    print("   Match pairs of cards to test your memory!")
    print()
    print("4. 🚪 Exit")
    print()
    print("-" * 50)

def get_user_choice():
    """Get and validate user's menu choice."""
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            else:
                print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input! Please enter a number between 1-4.")

def main():
    """Main game loop."""
    while True:
        try:
            clear_screen()
            display_header()
            display_menu()
            
            choice = get_user_choice()
            
            if choice == 1:
                # Play Tic Tac Toe
                game = TicTacToe()
                game.play()
            elif choice == 2:
                # Play Number Guessing
                game = NumberGuess()
                game.play()
            elif choice == 3:
                # Play Memory Cards
                game = MemoryCards()
                game.play()
            elif choice == 4:
                # Exit
                clear_screen()
                print("🎮 Thanks for playing! Goodbye! 👋")
                sys.exit(0)
            
            # Ask if user wants to return to main menu
            input("\n🔄 Press Enter to return to main menu...")
            
        except KeyboardInterrupt:
            print("\n\n🎮 Thanks for playing! Goodbye! 👋")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()