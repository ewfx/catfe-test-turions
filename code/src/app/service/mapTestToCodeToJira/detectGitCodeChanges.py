import subprocess

def get_changed_files():
    changed_files = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1"],
        capture_output=True, text=True
    ).stdout.split("\n")
    return [f.strip() for f in changed_files if f.strip()]

print(get_changed_files())  # ['src/main/java/com/app/authService.java']
