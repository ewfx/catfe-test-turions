import subprocess
import re
import os
import json

def get_jira_from_commit():
    commit_message = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        capture_output=True, text=True
    ).stdout
    match = re.search(r"(JIRA-\d+)", commit_message)
    jira = match.group(0) if match else None
    #return jira
    
        # Get the root directory of the Git repository
    git_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True
    ).stdout.strip()
    
    print(git_root)
    
    jira_file_path = os.path.join(git_root, "code/src/app/service/mapTestToCodeToJira/Jira.json")
    print(jira_file_path)
    
    # Open and load the jira.json file
    with open(jira_file_path, "r") as jira_file:
        jira_data = json.load(jira_file)
        #print(jira_data)

    if jira in jira_data:
        story = jira_data[jira].get("story")
        return f"JIRA ID: {jira}, Story: {story}" if story else f"JIRA ID: {jira}, Story not found."
    else:
        return f"JIRA ID: {jira} not found in jira.json."   

print(get_jira_from_commit())  # JIRA-1234

