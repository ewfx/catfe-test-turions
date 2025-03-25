import subprocess

class ModelLoader:
    def __init__(self, model_path, llama_bin_path):
        self.model_path = model_path
        self.llama_bin_path = llama_bin_path

    def generate_text(self, prompt):
        # Run the llama.cpp binary to generate text
        command = [
            self.llama_bin_path,
            "-m", self.model_path,
            "-p", prompt,
            "--no-mmap"  # Disable mmap if PrefetchVirtualMemory is unavailable
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running llama-cli.exe: {e.stderr}")
            return None