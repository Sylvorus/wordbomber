import os
import sys
import platform

# requirements: pywin32

art = r"""                          __   __                    __             
 _      ______  _________/ /  / /_  ____  ____ ___  / /_  ___  _____
| | /| / / __ \/ ___/ __  /  / __ \/ __ \/ __ `__ \/ __ \/ _ \/ ___/
| |/ |/ / /_/ / /  / /_/ /  / /_/ / /_/ / / / / / / /_/ /  __/ /    
|__/|__/\____/_/   \__,_/  /_.___/\____/_/ /_/ /_/_.___/\___/_/     by sylvorus
"""

# Check if on Windows to use pywin32 for window manipulation
if platform.system() == 'Windows':
    import win32gui
    import win32con

def load_words(filename):
    # Load words from a file and return a list of words.
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words

def find_matching_word(letters, words, used_words):
    # Find a word that contains the letters in the same order and hasn't been used.
    for word in words:
        if letters in word and word not in used_words:
            return word
    return None

def clear_console():
    #Clear the console output. 
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows
    else:
        # ANSI escape codes to clear the terminal screen
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()

def set_window_topmost():
    # Set the console window as always on top.
    if platform.system() == 'Windows':
        console_window = win32gui.GetForegroundWindow()
        win32gui.SetWindowPos(console_window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def main():
    # Load words from the file
    words = load_words("words.txt")
    used_words = set()

    print(art)
    print("Type 'restart' to reset the used words list. (e.g new game)")
    print("Type 'exit' to quit the program.")

    set_window_topmost()

    while True:
        # Input letters from the user and convert to uppercase
        input_letters = input("\nEnter the letters: ").strip().upper()

        clear_console()
        print(art)
        print("Type 'restart' to reset the used words list.")
        print("Type 'exit' to quit the program.")

        if input_letters == 'EXIT':
            break
        elif input_letters == 'RESTART':
            used_words.clear()
            print("Used words list has been cleared.")
            continue

        # Find and print the first matching word
        matching_word = find_matching_word(input_letters, words, used_words)

        if matching_word:
            print(f"\nMatching word: {matching_word}")
            used_words.add(matching_word)
        else:
            print("\nNo matching words found or all matching words have been used.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
