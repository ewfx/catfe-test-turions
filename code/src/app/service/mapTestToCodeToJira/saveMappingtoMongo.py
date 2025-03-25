from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["test_mapping_db"]
collection = db["code_test_mappings"]

def save_mapping(code_file, related_tests, related_jira):
    document = {
        "code_file": code_file,
        "related_tests": related_tests,
        "related_jira_tickets": related_jira,
        "last_updated": datetime.utcnow().isoformat()
    }
    collection.update_one({"code_file": code_file}, {"$set": document}, upsert=True)

# Example Usage
save_mapping(
    "src/main/java/com/app/authService.java",
    [{"test_file": "src/test/java/com/app/AuthServiceTest.java", "test_name": "AuthServiceTest"}],
    [{"jira_id": "JIRA-1234", "title": "Fix login issue"}]
)
