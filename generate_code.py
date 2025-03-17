import pyperclip
import subprocess

def generate_code():
    # Get the problem statement from clipboard
    problem_statement = pyperclip.paste()
    
    if not problem_statement.strip():
        print("No text found in clipboard!")
        return ""

    # Call the AI model using Ollama
    command = f'ollama run codellama "Generate a solution for: {problem_statement}"'
    
    # Run the command and capture output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    return result.stdout.strip()

# Example usage
if __name__ == "__main__":
    code = generate_code()
    print("Generated Code:\n", code)
