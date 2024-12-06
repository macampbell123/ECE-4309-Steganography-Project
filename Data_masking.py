import random
import sys
import tty
import termios

# Predefined list of random words for shuffling
RANDOM_WORDS = ["pineapple", "banana", "grapefruit", "watermelon", "kiwi",
                "blueberry", "apple", "mango", "peach", "plum"]

def get_masked_input(prompt):
    """
    Get user input while displaying 'X' in place of the actual input as the user types.
    """
    print(prompt, end='', flush=True)
    masked_input = ''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            if char in ('\n', '\r'):  # Enter key pressed
                break
            if char == '\x7f':  # Backspace handling
                if len(masked_input) > 0:
                    masked_input = masked_input[:-1]
                    sys.stdout.write('\b \b')  # Erase the last 'X' displayed
            else:
                masked_input += char
                sys.stdout.write('X')  # Display 'X' for every character typed
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print()  # Move to the next line after input
    return masked_input

def shuffle_message(word_count):
    """
    Generate a fake message by selecting random words.
    """
    return ' '.join(random.choices(RANDOM_WORDS, k=word_count))

if __name__ == "__main__":
    while True:
        # Masked input
        plaintext = get_masked_input("Enter the text: ")
        print("\nYour input was securely masked.")
        
        # Simulate password check
        user_key = get_masked_input("\nEnter the key: ")
        
        # If the key is wrong, provide a shuffled fake message
        if user_key != "CorrectKey":
            word_count = len(plaintext.split())
            fake_message = shuffle_message(word_count)
            print("\nDecrypted text (shuffled):", fake_message)
        else:
            print("\nDecrypted text (original):", plaintext)

        # Ask to continue or exit
        continue_prompt = input("\nWould you like to type another text? (yes/no): ").strip().lower()
        if continue_prompt != 'yes':
            print("Exiting the program.")
            break

