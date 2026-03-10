import random

def load_words(filename):
    """Loads words from a file."""
    try:
        with open(filename, 'r') as f:
            words = [line.strip().upper() for line in f if len(line.strip()) == 5]
        return words
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def get_feedback(guess, secret_word):
    """Generates feedback for a guess."""
    feedback = []
    secret_word_chars = list(secret_word)
    guess_chars = list(guess)
    
    # First pass: Check for correct letters in correct positions (Green)
    for i in range(len(guess)):
        if guess_chars[i] == secret_word_chars[i]:
            feedback.append('🟩')
            secret_word_chars[i] = None # Mark as used
            guess_chars[i] = None # Mark as handled
        else:
            feedback.append(None) # Placeholder

    # Second pass: Check for correct letters in wrong positions (Yellow)
    for i in range(len(guess)):
        if feedback[i] is None: # Only check if not already green
            if guess_chars[i] in secret_word_chars:
                feedback[i] = '🟨'
                secret_word_chars[secret_word_chars.index(guess_chars[i])] = None # Mark as used
            else:
                feedback[i] = '⬛'

    return feedback

def print_keyboard(keyboard_status):
    """Prints the status of the keyboard letters."""
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    print("\nKeyboard:")
    for row in rows:
        line = ""
        for char in row:
            line += f"{char}{keyboard_status.get(char, '⬜')} "
        print(line)
    print()

def main():
    print("Welcome to Wordle!")
    
    # Load mystery words and valid guess words
    mystery_words = load_words("words.txt")
    valid_guesses = load_words("guesses.txt")
    
    # Combine lists for checking valid guesses
    all_valid_words = set(mystery_words + valid_guesses)
    
    if not mystery_words:
        print("No words loaded. Please check 'words.txt'.")
        return

    secret_word = random.choice(mystery_words)
    attempts = 6
    
    # Initialize keyboard status (White square for unused)
    keyboard_status = {chr(i): '⬜' for i in range(65, 91)}

    while attempts > 0:
        guess = input(f"Enter a 5-letter guess ({attempts} attempts left): ").upper()

        if len(guess) != 5:
            print("Invalid guess length. Please enter a 5-letter word.")
            continue
        
        if guess not in all_valid_words:
             print("Not a valid word.")
             continue

        feedback = get_feedback(guess, secret_word)
        
        # Display guess letters aligned with feedback emojis
        print(" ".join(list(guess)))
        print(" ".join(feedback))

        # Update keyboard status
        for char, emoji in zip(guess, feedback):
            current_status = keyboard_status[char]
            # Priority: Green > Yellow > Black > Unused
            if emoji == '🟩':
                keyboard_status[char] = emoji
            elif emoji == '🟨':
                if current_status != '🟩':
                    keyboard_status[char] = emoji
            elif emoji == '⬛':
                if current_status == '⬜':
                    keyboard_status[char] = emoji

        print_keyboard(keyboard_status)

        if guess == secret_word:
            print("Congratulations! You guessed the word!")
            break

        attempts -= 1

    if attempts == 0:
        print(f"Game over! The word was: {secret_word}")

if __name__ == "__main__":
    main()
