import json
import os
import time
from bdd_generator import generate_bdd_scenario

TEST_DATA_FILE = r"D:\Softwares\catfe-test-turions\code\src\config\test_data.json"
BDD_OUTPUT_FILE = r"D:\Softwares\catfe-test-turions\code\src\tests\features\generated_bdd.feature"

def load_test_data():
    """Loads test data from JSON file."""
    try:
        with open(TEST_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_bdd_scenario(bdd_text):
    """Saves generated BDD scenario to a feature file."""
    with open(BDD_OUTPUT_FILE, "w") as f:
        f.write(bdd_text)

def monitor_test_data():
    """Monitors test data file and regenerates BDD when it changes."""
    last_data = load_test_data()

    while True:
        time.sleep(5)  # Check every 5 seconds
        current_data = load_test_data()

        if current_data != last_data:  # Detect change
            print("Test data changed. Regenerating BDD...")
            bdd_text = generate_bdd_scenario("Create a BDD for this test scenario: " + json.dumps(current_data))
            save_bdd_scenario(bdd_text)
            last_data = current_data

if __name__ == "__main__":
    monitor_test_data()
