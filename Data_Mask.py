
from Crypto.Hash import SHA256, HMAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import getpass
import random
import sys
import tty
import termios

# Constants
ALGORITHM_NONCE_SIZE = 12
ALGORITHM_TAG_SIZE = 16
ALGORITHM_KEY_SIZE = 16
PBKDF2_SALT_SIZE = 16
PBKDF2_ITERATIONS = 32767
PBKDF2_LAMBDA = lambda x, y: HMAC.new(x, y, SHA256).digest()

# Fixed password (for testing purposes)
PASSWORD = "Marcus1"

# Predefined list of random words
RANDOM_WORDS = ["pineapple", "banana", "grapefruit", "watermelon", "kiwi",
                "blueberry", "apple", "mango", "peach", "plum"]

def encryptString(plaintext, password):
    salt = get_random_bytes(PBKDF2_SALT_SIZE)
    key = PBKDF2(password, salt, ALGORITHM_KEY_SIZE, PBKDF2_ITERATIONS, PBKDF2_LAMBDA)
    ciphertextAndNonce = encrypt(plaintext.encode('utf-8'), key)
    ciphertextAndNonceAndSalt = salt + ciphertextAndNonce
    return base64.b64encode(ciphertextAndNonceAndSalt).decode('utf-8')

def decryptString(base64CiphertextAndNonceAndSalt, password):
    ciphertextAndNonceAndSalt = base64.b64decode(base64CiphertextAndNonceAndSalt)
    salt = ciphertextAndNonceAndSalt[:PBKDF2_SALT_SIZE]
    ciphertextAndNonce = ciphertextAndNonceAndSalt[PBKDF2_SALT_SIZE:]
    key = PBKDF2(password, salt, ALGORITHM_KEY_SIZE, PBKDF2_ITERATIONS, PBKDF2_LAMBDA)
    try:
        plaintext = decrypt(ciphertextAndNonce, key)
        return plaintext.decode('utf-8')
    except ValueError:
        return None

def encrypt(plaintext, key):
    nonce = get_random_bytes(ALGORITHM_NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + ciphertext + tag

def decrypt(ciphertextAndNonce, key):
    nonce = ciphertextAndNonce[:ALGORITHM_NONCE_SIZE]
    ciphertext = ciphertextAndNonce[ALGORITHM_NONCE_SIZE:-ALGORITHM_TAG_SIZE]
    tag = ciphertextAndNonce[-ALGORITHM_TAG_SIZE:]
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

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
            if char == '\x7f':  # Backspace handling                if len(masked_input) > 0:
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

if __name__ == "__main__":
    while True:
        plaintext = get_masked_input("Enter the text: ")
        encrypted = encryptString(plaintext, PASSWORD)
        print("\nEncrypted:", encrypted)

        input_password = getpass.getpass("\nis this message okay? ")
        decrypted = decryptString(encrypted, input_password)

        if decrypted is None:
            word_count = len(plaintext.split())
            random_phrase = ' '.join(random.choices(RANDOM_WORDS, k=word_count))
            print("\nDecrypted text:", random_phrase)
        else:
            print("\nDecrypted text:", decrypted)

        continue_prompt = input("\nWould you like to type another text? (yes/no): ").strip().lower()
        if continue_prompt != 'yes':
            print("Exiting the program.")
            break