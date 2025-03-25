import os
import git
import sys
import requests
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.mongo_connect import connect_to_mongodb, search_field_in_collection, search_scenarios_by_state  # Import functions from mongo_connect.py

class BDDTestGeneratorService:
    def __init__(self, api_key):
        # Initialize the OpenAI API key
        self.api_key = api_key
        openai.api_key = self.api_key

    def format_git_diff(self, diff):
        """Format the git diff output for better readability."""
        formatted_diff = "Diff Summary between commits:\n\n"
        lines = diff.splitlines()

        for line in lines:
            if line.startswith('diff'):
                formatted_diff += f"{line}\n"
            elif line.startswith('index'):
                index_info = line.split()
                formatted_diff += f"Index Changes:\n- Old Version: {index_info[1]}\n- New Version: {index_info[2]}\n\n"
            elif line.startswith('---') or line.startswith('+++'):
                formatted_diff += f"File: {line[4:]}\n\n"
            elif line.startswith('@@'):
                formatted_diff += f"Changes:\n{line}\n"
            elif line.startswith('-'):
                formatted_diff += f"Removed: {line[1:]}\n"
            elif line.startswith('+'):
                formatted_diff += f"Added: {line[1:]}\n"

        return formatted_diff

    def generate_test_cases_openrouter(self, context):
        try:
            # Prepare the request to the OpenRouter API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek/deepseek-r1-zero:free",  # Correct model ID
                "prompt": f"Generate only Diff between commits:\n\n{context}",
                "temperature": 0.8,  
                "max_tokens": 100,    
                "top_p": 1.0,         
                "n": 1                
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                # Extract and return the generated test cases
                return response.json()["choices"][0]["text"].strip()
            else:
                raise ValueError(f"Failed to Summary: {response.text}")
        except Exception as e:
            # Handle errors appropriately
            raise ValueError(f"Failed to Summary: {str(e)}")


def main():
    # Git repository details
    repo_url = "https://github.com/msnish/catfe-test-turions.git"
    repo_dir = "my_local_repo"  # Change this to your desired local directory name

    # Clone the repository if it doesn't exist
    if not os.path.exists(repo_dir):
        print(f"Cloning repository from {repo_url} into {repo_dir}...")
        repo = git.Repo.clone_from(repo_url, repo_dir)
    else:
        print(f"Repository already exists at {repo_dir}.")
        repo = git.Repo(repo_dir)

    # Fetch the latest changes
    print("Fetching latest changes...")
    repo.git.fetch()

    # Get the latest commit and the previous commit
    commits = list(repo.iter_commits())
    if len(commits) < 2:
        print("Not enough commits to compare.")
        exit()

    latest_commit = commits[0]
    previous_commit = commits[1]

    # Identify changes
    diff = repo.git.diff(previous_commit.hexsha, latest_commit.hexsha)
    if diff:
        print("Raw Changes between the latest and previous commits:")
        #print(diff)
        
        script_names = []
        excluded_paths = ["tests/", "docs/"]  # Add paths or patterns to exclude
        for line in diff.splitlines():
            if line.startswith("--- ") or line.startswith("+++ "):
                # Extract the file name after "--- " or "+++ "
                file_path = line[4:]
                if file_path != "/dev/null":  # Ignore deleted files
                    # Exclude specific paths
                    if not any(excluded_path in file_path for excluded_path in excluded_paths):
                        script_names.append(file_path)

        print("\nExtracted Script Names (Excluding Specific Paths):")
        print(script_names)
        
        # Extract only the last script name (file name without path)
        if script_names:
            last_script_name = os.path.basename(script_names[-1])  # Extract only the file name
            print(f"\nLast Script modified: {last_script_name}")

            # Connect to MongoDB and call search_field_in_collection
            db = connect_to_mongodb()
            if db is not None:
                # Search for the field "main_2.py" in the "code_feature_mapping" collection
                documents = search_field_in_collection(db, "code_feature_mapping", last_script_name)
            else:
                print("\nNo script names found.")
        
        if documents:
            for doc in documents:
                primaryFeatureDependency = doc.get("primaryFeatureDependency")  # Replace "feature_id" with the actual field name
                if primaryFeatureDependency:
                    print(f"\nSearching for scenarios with primaryFeatureDependency: {primaryFeatureDependency}")
                    search_scenarios_by_state(db, "BDDTESTMAPPER", primaryFeatureDependency, "unstable")
        
        if documents:
            for doc in documents:
                secondaryFeatureDependency = doc.get("secondaryFeatureDependency")  # Replace "feature_id" with the actual field name
                if secondaryFeatureDependency:
                    print(f"\nSearching for scenarios with secondaryFeatureDependency: {secondaryFeatureDependency}")
                    search_scenarios_by_state(db, "BDDTESTMAPPER", secondaryFeatureDependency, "Partially unstable")

        # Initialize the BDD Test Generator with your OpenAI API key
        api_key = "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"  # Replace with your actual OpenAI API key
        bdd_test_generator = BDDTestGeneratorService(api_key)

        # Format the diff
        formatted_diff = bdd_test_generator.format_git_diff(diff)

        # Generate test cases
        test_cases = bdd_test_generator.generate_test_cases_openrouter(formatted_diff)
        #print("\nGenerated Summary:")
        #print(test_cases)
    else:
        print("No changes detected between the latest and previous commits.")

if __name__ == "__main__":
    main()