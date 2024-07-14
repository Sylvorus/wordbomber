import os
import sys
import win32gui
import win32con
import win32console
import msvcrt

# requirements: pywin32, windows
# feel free to edit but keep credits please

art = r"""                           __   __                    __             
  _      ______  _________/ /  / /_  ____  ____ ___  / /_  ___  _____
 | | /| / / __ \/ ___/ __  /  / __ \/ __ \/ __ `__ \/ __ \/ _ \/ ___/
 | |/ |/ / /_/ / /  / /_/ /  / /_/ / /_/ / / / / / / /_/ /  __/ /    
 |__/|__/\____/_/   \__,_/  /_.___/\____/_/ /_/ /_/_.___/\___/_/     by sylvorus
"""

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
    os.system('cls')

def set_window_topmost():
    # Set the console window as always on top.
    console_window = win32gui.GetForegroundWindow()
    win32gui.SetWindowPos(console_window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)\

def set_console_size(cols, lines):
    try:
        # Windows specific code to set console size
        h = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        rect = win32console.PySMALL_RECTType(0, 0, cols - 1, lines - 1)
        h.SetConsoleWindowInfo(True, rect)
        size = win32console.PyCOORDType(cols, lines)
        h.SetConsoleScreenBufferSize(size)
    except Exception as e:
        print(f"Error setting console size on Windows: {e}")

def get_input():
    # Get input from the user without moving to a new line
    buffer = []
    while True:
        char = msvcrt.getch()
        if char == b'\r':  # Enter key
            break
        elif char == b'\x08':  # Backspace key
            if buffer:
                buffer.pop()
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            buffer.append(char.decode('utf-8'))
            sys.stdout.write(char.decode('utf-8'))
            sys.stdout.flush()
    return ''.join(buffer)

def main():
    # Load words from the file
    words = load_words("words.txt")
    used_words = set()

    print(art)
    print(" Type '.' to reset the used words list.")
    print(" Type 'exit' to quit the program.")
    print("\n Enter prompt to start.")

    set_window_topmost()

    while True:
        # Input letters from the user and convert to uppercase
        print("\n Enter the letters: ", end='', flush=True)
        input_letters = get_input().strip().upper()
        
        clear_console()
        
        print(art)
        print(" Type '.' to reset the used words list.")
        print(" Type 'exit' to quit the program.")

        if input_letters == 'EXIT':
            break
        elif not input_letters:
            print("\n Please enter at least 1 letter.")
            continue
        elif input_letters == '.':
            used_words.clear()
            print("\n Used words list has been cleared.")
            continue

        # Find and print the first matching word
        matching_word = find_matching_word(input_letters, words, used_words)

        if matching_word:
            print(f"\n Matching word: {matching_word}")
            used_words.add(matching_word)
        else:
            print("\n No matching words found or all matching words have been used.")

    input("\n Press Enter to exit...")

set_console_size(81, 12)
if __name__ == "__main__":
    main()
