import pyautogui
import keyboard
import time
import subprocess
import pyperclip
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
        prompt = f"Write only the sql code without any explanation for the following problem:\n{problem_statement}"
        result = subprocess.run(
            ["ollama", "run", "codellama", prompt],
            capture_output=True, text=True, encoding="utf-8"
        )
        
        generated_code = result.stdout.strip()
        print("Generated Code:\n", generated_code)
    except Exception as e:
        print("Error generating code:", str(e))

def type_code():
    """Simulate human-like typing of the generated code"""
    global generated_code
    if not generated_code:
        print("No code generated yet. Press F8 to generate code first.")
        return

    print("Typing Code in IDE...")

    def interval(char):
        """Return a random interval for realistic typing speed"""
        if char.isalpha():  # Letters
            return random.uniform(0.05, 0.15)
        elif char.isdigit():  # Numbers
            return random.uniform(0.05, 0.2)
        else:  # Symbols and spaces
            return random.uniform(0.1, 0.3)

    def human_typewrite(line):
        """Simulate human typing behavior"""
        for char in line:
            if char == '}':  
                continue  # Skip auto-closing brackets
            pyautogui.typewrite(char)
            time.sleep(interval(char))  # Random delay for human-like typing

        pyautogui.press("enter")  # Move to next line

    lines = generated_code.split("\n")

    for line in lines:
        human_typewrite(line.strip())  # Strip leading/trailing spaces before typing

    print("Code typing completed. Ready for next problem selection!")

# Hotkeys
keyboard.add_hotkey("F8", lambda: generate_code(read_selected_text()))  # Generate code from selected text
keyboard.add_hotkey("F9", type_code)  # Type the generated code

print("AI Code Typing is running... Select a problem, press F8 to generate code, F9 to type it.")
keyboard.wait()
