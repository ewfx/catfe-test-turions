import sys
import os

# Add the `code` directory to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

# Import app
from src.app.controller.bddtestgeneratorcontroller import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
