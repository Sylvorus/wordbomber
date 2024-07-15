import os
import sys
import random
import win32gui
import win32con
import win32console
import msvcrt

art = r"""                           __   __                    __             
  _      ______  _________/ /  / /_  ____  ____ ___  / /_  ___  _____
 | | /| / / __ \/ ___/ __  /  / __ \/ __ \/ __ `__ \/ __ \/ _ \/ ___/
 | |/ |/ / /_/ / /  / /_/ /  / /_/ / /_/ / / / / / / /_/ /  __/ /    
 |__/|__/\____/_/   \__,_/  /_.___/\____/_/ /_/ /_/_.___/\___/_/     by sylvorus
"""

def load_words(filename):
    # loads words
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words

def find_matching_word(letters, words, used_words, mode):
    # finds matching unused word
    matching_words = [word for word in words if letters in word and word not in used_words]
    
    if not matching_words:
        return None

    if mode == 'Longest':
        return max(matching_words, key=len)
    elif mode == 'Random':
        return random.choice(matching_words)
    
    return None

def clear_console():
    # clear console 
    os.system('cls')

def set_window_topmost():
    # always ontop
    console_window = win32gui.GetForegroundWindow()
    win32gui.SetWindowPos(console_window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def set_console_size(cols, lines):
    try:
        # setting console size
        h = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        rect = win32console.PySMALL_RECTType(0, 0, cols - 1, lines - 1)
        h.SetConsoleWindowInfo(True, rect)
        size = win32console.PyCOORDType(cols, lines)
        h.SetConsoleScreenBufferSize(size)
    except Exception as e:
        print(f"Error setting console size on Windows: {e}")

def get_input():
    # get input without starting a new line
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

#################################################################################################

def main_normal_mode():
    set_console_size(83, 17)
    # load words from file
    words = load_words("words.txt")
    used_words = set()
    used_words_list = []
    mode = 'Longest'

    print(art)
    print(" Type '.' to reset the used words list.")
    print(" Type ',' to toggle between longest and random word modes.")
    print(" Type '/' to skip the current word.")
    print(" Type 'exit' to quit the program.")
    print(f"\n Current mode: {mode}")
    print("\n Enter prompt to start.")

    while True:
        # read all letters as uppercase
        print("\n Enter the letters: ", end='', flush=True)
        input_letters = get_input().strip().upper()

        clear_console()

        print(art)
        print(" Type '.' to reset the used words list.")
        print(" Type ',' to toggle between longest and random word modes.")
        print(" Type '/' to skip the current word.")
        print(" Type 'exit' to quit the program.")
        
        if input_letters == 'EXIT':
            break
        elif input_letters == '.':
            used_words.clear()
            used_words_list.clear()
            print(f"\n Current mode: {mode}")
            print("\n Used words list has been cleared.")
            continue
        elif input_letters == ',':
            mode = 'Random' if mode == 'Longest' else 'Longest'
            print(f"\n Current mode: {mode}")
            print(f"\n Mode has been changed to {mode}.")
            continue
        elif not input_letters:
            print(f"\n Current mode: {mode}")
            print("\n Please enter at least 1 letter.")
            continue
        elif input_letters == '/':
            if used_words_list:
                last_word = used_words_list.pop()
                used_words.remove(last_word)
                print(f"\n Current mode: {mode}")
                print(f"\n '{last_word}' has been removed from the used words list.")
            else:
                print(f"\n Current mode: {mode}")
                print("\n No words to remove.")
            continue

        # find and print first matching word
        matching_word = find_matching_word(input_letters, words, used_words, mode)

        if matching_word:
            print(f"\n Current mode: {mode}")
            print(f"\n Matching word: {matching_word}")
            used_words.add(matching_word)
            used_words_list.append(matching_word)
        else:
            print(f"\n Current mode: {mode}")
            print("\n No matching words found or all matching words have been used.")

    clear_console()
    set_console_size(61, 8)
    print(r'''     __                  __               ____            __
    / /_  __  _____     / /_  __  _____  / / /  ____    _/_/
   / __ \/ / / / _ \   / __ \/ / / / _ \/ / /  / __ \ _/_/  
  / /_/ / /_/ /  __/  / /_/ / /_/ /  __/_/_/  / /_/ //_/    
 /_.___/\__, /\___/  /_.___/\__, /\___(_|_)   \____/_/      
       /____/              /____/            ''')
    input("\n Press Enter to exit...")

#################################################################################################

def main_compact_mode():
    set_console_size(51, 3)
    # load words from file
    words = load_words("words.txt")
    used_words = set()
    used_words_list = []
    mode = 'Longest'

    print(f"Current mode: {mode}")
    print("Enter prompt to start.")

    while True:
        # read all letters as uppercase
        print("Enter the letters: ", end='', flush=True)
        input_letters = get_input().strip().upper()

        clear_console()

        if input_letters == 'EXIT':
            break
        elif input_letters == '.':
            used_words.clear()
            used_words_list.clear()
            print(f"Current mode: {mode}")
            print("Used words list has been cleared.")
            continue
        elif input_letters == ',':
            mode = 'Random' if mode == 'Longest' else 'Longest'
            print(f"Current mode: {mode}")
            print(f"Mode has been changed to {mode}.")
            continue
        elif not input_letters:
            print(f"Current mode: {mode}")
            print("Please enter at least 1 letter.")
            continue
        elif input_letters == '/':
            if used_words_list:
                last_word = used_words_list.pop()
                used_words.remove(last_word)
                print(f"Current mode: {mode}")
                print(f"'{last_word}' removed.")
            else:
                print(f"Current mode: {mode}")
                print("No words to remove from list.")
            continue

        # find and print first matching word
        matching_word = find_matching_word(input_letters, words, used_words, mode)

        if matching_word:
            print(f"Current mode: {mode}")
            print(f"Matching word: {matching_word}")
            used_words.add(matching_word)
            used_words_list.append(matching_word)
        else:
            print(f"Current mode: {mode}")
            print("No matching unused words found.")

#################################################################################################

# set_console_size(81, 12) - broken??
if __name__ == "__main__":
    while True:
        print(art)
        print(" Choose mode (1 or 2):")
        print(" 1. Normal Mode")
        print(" 2. Compact Mode")
        print("\n Type 'exit' to quit the program.")

        set_window_topmost()
        
        print("\n Enter choice: ", end='', flush=True)
        choice = get_input().strip()
        
        if choice == '1':
            clear_console()
            main_normal_mode()
            break
        elif choice == '2':
            clear_console()
            main_compact_mode()
            break
        elif choice == 'exit':
            break
        else:
            clear_console()
            continue
