import os
import sys
import git
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from updateBDDTestSet import connect_to_mongodb, search_field_in_collection, search_and_update_scenarios_by_state  # Import functions from mongo_connect.py
from fetchJiraIdFromGit import get_jira_from_commit

def get_changed_files():
    try:
        # Initialize the repository
        repo = git.Repo(os.getcwd())
        print(f"Repository: {repo.working_dir}")

        print(f"Current branch: {repo.active_branch}")
        
        # Check if there are at least two commits
        commits = list(repo.iter_commits())
        if len(commits) < 2:
            print("Not enough commits to compare.")
            return []

        # Get the list of changed files between the latest commit and the previous commit
        changed_files = repo.git.diff('HEAD~1', name_only=True).split('\n')
        return [f.strip() for f in changed_files if f.strip()]
    except Exception as e:
        print(f"Error accessing git repository: {e}")
        return []

def main():
    # Print the list of changed files
    changed_files = get_changed_files()
    print("Changed files:", changed_files)

    # Extract only the last script name (file name without path)
    if changed_files:
        last_script_name = os.path.basename(changed_files[-1])  # Extract only the file name
        print(f"\nLast Script modified: {last_script_name}")
        
        jira=get_jira_from_commit()
        print(f"Jira ID: {jira}")

        # Connect to MongoDB and call search_field_in_collection
        db = connect_to_mongodb()
        documents = []  # Initialize documents to an empty list
        if db is not None:
            # Search for the code to module and feature mapping in the "code_feature_mapping" collection
            documents = search_field_in_collection(db, "code_feature_mapping", last_script_name)
        else:
            print("\nNo script names found.")
    else:
        documents = [] 
        
        
    if documents:
        for doc in documents:
            primaryFeatureDependency = doc.get("primaryFeatureDependency")  # Replace "feature_id" with the actual field name
            if primaryFeatureDependency:
                print(f"\nSearching for scenarios with primaryFeatureDependency: {primaryFeatureDependency}")
                search_and_update_scenarios_by_state(db, "BDDTESTMAPPER", primaryFeatureDependency, "Unstable",jira)
    
    if documents:
        for doc in documents:
            secondaryFeatureDependency = doc.get("secondaryFeatureDependency")  # Replace "feature_id" with the actual field name
            if secondaryFeatureDependency:
                print(f"\nSearching for scenarios with secondaryFeatureDependency: {secondaryFeatureDependency}")
                search_and_update_scenarios_by_state(db, "BDDTESTMAPPER", secondaryFeatureDependency, "Partially Unstable",jira)

if __name__ == "__main__":
    main()