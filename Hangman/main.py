import random
from words import word_list

selected_word = random.choice(word_list)
word_length = len(selected_word)

game_over = False
lives = 6

from art import logo
print(logo)

display = []

for _ in range(word_length):
    display += "_"

print(f"{' '.join(display)}")

while not game_over:
    guess = input("Guess a letter: ").lower()
    
    if guess in display:
        print(f"You've already guessed {guess}")
    for position in range(word_length):
        letter = selected_word[position]
        if letter == guess:
            display[position] = letter
    if guess not in selected_word:
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            game_over = True
            print("You lose.")
    print(f"{' '.join(display)}")
    if "_" not in display:
        game_over = True
        print("You win.")
    from art import stages
    print(stages[lives])