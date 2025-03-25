import os
import sys
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from updateBDDTestSet import connect_to_mongodb, search_field_in_collection, search_and_update_scenarios_by_state  # Import functions from mongo_connect.py

def get_changed_files():
    try:
        # Check if we are in a Git repository
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True)
        
        # Check if there are at least two commits
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            capture_output=True, text=True, check=True
        )
        commit_count = int(result.stdout.strip())
        if commit_count < 2:
            print("Not enough commits to compare.")
            return []

        # Run the git command to get the list of changed files
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"],
            capture_output=True, text=True, check=True
        )
        # Print the raw output for debugging
        print("Raw output from git command:", result.stdout)
        
        # Split the output into lines and strip any whitespace
        changed_files = result.stdout.split("\n")
        return [f.strip() for f in changed_files if f.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def main():
    # Print the list of changed files
    changed_files = get_changed_files()
    print("Changed files:", changed_files)

    # Extract only the last script name (file name without path)
    if changed_files:
        last_script_name = os.path.basename(changed_files[-1])  # Extract only the file name
        print(f"\nLast Script modified: {last_script_name}")

        # Connect to MongoDB and call search_field_in_collection
        db = connect_to_mongodb()
        documents = []  # Initialize documents to an empty list
        if db is not None:
            # Search for the code to module and feature mapping in the "code_feature_mapping" collection
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

if __name__ == "__main__":
    main()