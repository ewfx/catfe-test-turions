import subprocess
import os


# Paths
LLAMA_CPP_BIN = r"D:\Softwares\main\catfe-test-turions\code\src\app\ai_service\llama_bin\llama-cli.exe"
MODEL_PATH = r"D:\Softwares\main\catfe-test-turions\code\src\app\ai_service\models\mistral-7b-v0.1.Q4_K_M.gguf"

def generate_bdd_scenario(prompt: str):
    """Runs Llama.cpp to generate BDD scenarios."""
    command = [
        LLAMA_CPP_BIN,
        "-m", MODEL_PATH,
        "-p", prompt,
        "--no-mmap"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "Error: llama-cli.exe not found!"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

# Test function
if __name__ == "__main__":
    print(generate_bdd_scenario("Create a Gherkin format BDD for login scenario"))
