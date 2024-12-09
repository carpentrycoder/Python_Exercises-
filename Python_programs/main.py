import random

def get_choice():
    player_choice = input("Enter a choice (rock, paper, scissors): ").lower()
    options = ["rock", "paper", "scissors"]
    
    # Validate player input
    while player_choice not in options:
        print("Invalid choice. Please try again.")
        player_choice = input("Enter a choice (rock, paper, scissors): ").lower()
    
    computer_choice = random.choice(options)
    choices = {"player": player_choice, "computer": computer_choice}
    return choices

def check_win(player, computer):
    print(f"You chose {player}, Computer chose {computer}.")
    
    if player == computer:
        return "It's a tie!"
    
    if (player == "rock" and computer == "scissors") or \
       (player == "paper" and computer == "rock") or \
       (player == "scissors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

# Main Program
choices = get_choice()  # Returns a dictionary
result = check_win(choices['player'], choices['computer'])  # Access keys correctly
print(result)
