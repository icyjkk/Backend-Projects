import game

def main():
    game.welcome_message()
    while True:
        secret_number = game.select_random_number()
        attempts = game.get_difficulty_level()

        game.play_guessing_game(secret_number, attempts)

        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break
        
if __name__ == "__main__":
    main()
