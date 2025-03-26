import subprocess
import re

def get_jira_from_commit():
    commit_message = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        capture_output=True, text=True
    ).stdout
    match = re.search(r"(JIRA-\d+)", commit_message)
    jira = match.group(0) if match else None
    return jira

print(get_jira_from_commit())  # JIRA-1234

