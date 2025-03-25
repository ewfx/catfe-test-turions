import os
import git
import sys
import requests
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from updateBDDTestSet import connect_to_mongodb, search_field_in_collection, search_and_update_scenarios_by_state  # Import functions from mongo_connect.py

def main():
    # Git repository details
    repo_url = "https://github.com/ewfx/catfe-test-turions.git"
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
        #print("Raw Changes between the latest and previous commits:")
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
                # Search for the code to module ans feature mapping in the "code_feature_mapping" collection
                documents = search_field_in_collection(db, "code_feature_mapping", last_script_name)
            else:
                print("\nNo script names found.")
        
        if documents:
            for doc in documents:
                primaryFeatureDependency = doc.get("primaryFeatureDependency")  # Replace "feature_id" with the actual field name
                if primaryFeatureDependency:
                    print(f"\nSearching for scenarios with primaryFeatureDependency: {primaryFeatureDependency}")
                    search_and_update_scenarios_by_state(db, "BDDTESTMAPPER", primaryFeatureDependency, "unstable")
        
        if documents:
            for doc in documents:
                secondaryFeatureDependency = doc.get("secondaryFeatureDependency")  # Replace "feature_id" with the actual field name
                if secondaryFeatureDependency:
                    print(f"\nSearching for scenarios with secondaryFeatureDependency: {secondaryFeatureDependency}")
                    search_and_update_scenarios_by_state(db, "BDDTESTMAPPER", secondaryFeatureDependency, "Partially unstable")

        # Initialize the BDD Test Generator with your OpenAI API key


if __name__ == "__main__":
    main()