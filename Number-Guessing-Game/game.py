import random
import time

def welcome_message():
    print("\nWelcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have 3, 5 or 10 chances to guess the correct number. \n")

def select_random_number():
    return random.randint(1, 100)

def get_difficulty_level():
    while True:
        print("Select a difficulty level:")
        print("1. Easy (10 chances)")
        print("2. Medium (5 chances)")
        print("3. Hard (3 chances)")
        choice = input("Enter 1, 2, or 3: ")
        
        if choice == "1":
            return 10
        elif choice == "2":
            return 5
        elif choice == "3":
            return 3
        else:
            print("Invalid choice, please try again.")

def play_guessing_game(secret_number, attempts):
    start_time = time.time()
    
    for attempt in range(1, attempts + 1):
        guess = int(input(f"Attempt {attempt} of {attempts}. Enter your guess: "))

        if guess == secret_number:
            end_time = time.time()  # Registrar el tiempo al adivinar correctamente
            duration = end_time - start_time
            print(f"Congratulations! You've guessed the correct number in {duration:.2f} seconds!")
            break
        elif guess < secret_number:
            print("Too low! Try again.\n")
        else:
            print("Too high! Try again.\n")
    else:
        end_time = time.time()  # Registrar el tiempo al finalizar todos los intentos
        duration = end_time - start_time
        print(f"Sorry, you've used all your chances. The correct number was {secret_number}. It took you {duration:.2f} seconds.")
