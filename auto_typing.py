import pyautogui
import keyboard
import pynput.mouse as mouse
import time
import subprocess
import pyperclip
from pynput import mouse
import random

# Global variable to store generated code
generated_code = ""

def read_selected_text():
    """Read the selected text (problem statement) from clipboard"""
    keyboard.press_and_release('ctrl+c')  # Copy selected text
    time.sleep(0.5)
    return pyperclip.paste()

def generate_code(problem_statement):
    """Generate Java code using Code Llama (Ollama) without explanation"""
    global generated_code
    try:
        prompt = f"Write only the java code without any explanation for the following problem:\n{problem_statement}"
        result = subprocess.run(
            ["ollama", "run", "codellama", prompt],
            capture_output=True, text=True, encoding="utf-8"
        )
        
        generated_code = result.stdout.strip()
        print("Generated Code:\n", generated_code)
    except Exception as e:
        print("Error generating code:", str(e))

# Human-like typing behavior
def interval(char):
    if char.isalpha():
        return random.uniform(0.05, 0.15)
    elif char.isdigit():
        return random.uniform(0.05, 0.2)
    else:
        return random.uniform(0.1, 0.3)

def typo():
    typo_count = random.randrange(1, 3)
    for _ in range(typo_count):
        typo = random.choice('abcdefghijklmnopqrstuvwxyz')
        pyautogui.write(typo)
        time.sleep(interval(typo))
    for _ in range(typo_count):
        pyautogui.press('backspace')

def human_typewrite(text):
    for char in text:
        if random.random() < 0.02:  # 2% chance of making a typo
            typo()
        pyautogui.write(char)
        time.sleep(interval(char))

def type_code():
    """Simulate human-like typing and skip auto-closing brackets."""
    global generated_code
    if not generated_code:
        print("No code generated yet. Press F8 to generate code first.")
        return
    
    print("Typing Code in IDE...")
    lines = generated_code.split("\n")
    
    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line == "}":  # Skip auto-closing brackets
            continue
        
        human_typewrite(line)
        pyautogui.press("enter")  # Move to next line
    
    print("Code typing completed. Ready for next problem selection!")

def stop_typing_listener(x, y):
    """Stop typing if the mouse moves to the corner of the screen"""
    screen_width, screen_height = pyautogui.size()
    if (x < 50 and y < 50) or (x > screen_width - 50 and y > screen_height - 50):
        global typing_active
        typing_active = False  # Stop typing
        print("Typing stopped due to mouse movement.")

# Mouse listener for stopping typing
mouse_listener = mouse.Listener(on_move=stop_typing_listener)
mouse_listener.start()

# Hotkeys
keyboard.add_hotkey("F8", lambda: generate_code(read_selected_text()))  # Generate code from selected text
keyboard.add_hotkey("F9", type_code)  # Type the generated code

print("AI Code Typing is running... Select a problem, press F8 to generate code, F9 to type it.")
keyboard.wait()
