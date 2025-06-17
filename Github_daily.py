import os
import subprocess
from datetime import datetime, timedelta
import random
import time
import json
import logging
from pathlib import Path
import sys
import traceback

# Get the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure logging with absolute paths
LOG_FILE = os.path.join(SCRIPT_DIR, 'git_commits.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Default configuration
DEFAULT_CONFIG = {
    "repo_path": r"C:\Users\shrey\Documents\DummyRepo",
    "min_commits": 1,
    "max_commits": 10,
    "commit_delay": 2,
    "branch": "main"
}

def load_config():
    """Load configuration from config.json or create default if not exists"""
    config_path = os.path.join(SCRIPT_DIR, 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except json.JSONDecodeError as e:
            logging.error(f"Error reading config file: {e}")
            return DEFAULT_CONFIG
    else:
        try:
            with open(config_path, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            return DEFAULT_CONFIG
        except Exception as e:
            logging.error(f"Error creating config file: {e}")
            return DEFAULT_CONFIG

def get_last_commit_date():
    """Get the last commit date from last_commit.txt"""
    try:
        last_commit_path = os.path.join(SCRIPT_DIR, 'last_commit.txt')
        with open(last_commit_path, 'r') as f:
            return datetime.strptime(f.read().strip(), '%Y-%m-%d').date()
    except (FileNotFoundError, ValueError) as e:
        logging.info(f"No last commit date found or invalid format: {e}")
        return None

def update_last_commit_date():
    """Update the last commit date in last_commit.txt"""
    try:
        last_commit_path = os.path.join(SCRIPT_DIR, 'last_commit.txt')
        with open(last_commit_path, 'w') as f:
            f.write(datetime.now().strftime('%Y-%m-%d'))
    except Exception as e:
        logging.error(f"Error updating last commit date: {e}")

def check_missed_days(last_commit_date):
    """Check if any days were missed since last commit"""
    if last_commit_date is None:
        return 0
    
    today = datetime.now().date()
    days_diff = (today - last_commit_date).days
    
    if days_diff > 1:
        logging.warning(f"Missed {days_diff - 1} days since last commit")
    return days_diff

# List of random commit messages
COMMIT_MESSAGES = [
    "Daily growth check-in",
    "Another day, another commit",
    "Keeping the streak alive",
    "Daily contribution",
    "Consistency is key",
    "Making progress",
    "Daily update",
    "Adding some color to the repo",
    "Level up: Daily commit",
    "Coding rhythm continues",
    "Building momentum",
    "Step by step progress",
    "Daily coding practice",
    "Commit streak continues",
    "Another milestone reached",
    "Learning and growing",
    "Daily development check-in",
    "Code consistency matters",
    "Progress over perfection",
    "Daily coding journey"
]

# List of random content to add
CONTENT_OPTIONS = [
    "Today's progress: {timestamp}",
    "Daily update at {timestamp}",
    "Commit streak: {timestamp}",
    "Another day of consistency: {timestamp}",
    "Daily check-in: {timestamp}",
    "Progress update: {timestamp}",
    "Streak continues: {timestamp}",
    "Daily contribution: {timestamp}",
    "Another milestone: {timestamp}",
    "Keeping the momentum: {timestamp}"
]

def get_streak_count():
    """Get the current streak count from streak.txt"""
    try:
        streak_path = os.path.join(SCRIPT_DIR, 'streak.txt')
        with open(streak_path, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError) as e:
        logging.info(f"No streak count found or invalid format: {e}")
        return 0

def update_streak_count(count):
    """Update the streak count in streak.txt"""
    try:
        streak_path = os.path.join(SCRIPT_DIR, 'streak.txt')
        with open(streak_path, 'w') as f:
            f.write(str(count))
    except Exception as e:
        logging.error(f"Error updating streak count: {e}")

def make_commit(config):
    """Make a single commit with error handling"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        random_content = random.choice(CONTENT_OPTIONS).format(timestamp=timestamp)
        random_commit_message = random.choice(COMMIT_MESSAGES)

        daily_streak_path = os.path.join(config["repo_path"], 'daily_streak.txt')
        with open(daily_streak_path, 'a') as f:
            f.write(f"{random_content}\n")

        CREATE_NO_WINDOW = 0x08000000

        # Git operations with error handling
        try:
            subprocess.run(["git", "add", "daily_streak.txt"], 
                         check=True, creationflags=CREATE_NO_WINDOW, cwd=config["repo_path"])
            subprocess.run(["git", "commit", "-m", random_commit_message], 
                         check=True, creationflags=CREATE_NO_WINDOW, cwd=config["repo_path"])
            subprocess.run(["git", "push", "origin", config["branch"]], 
                         check=True, creationflags=CREATE_NO_WINDOW, cwd=config["repo_path"])
            return True, random_commit_message
        except subprocess.CalledProcessError as e:
            logging.error(f"Git operation failed: {str(e)}")
            return False, str(e)

    except Exception as e:
        logging.error(f"Commit failed: {str(e)}")
        return False, str(e)

def initialize_files():
    """Initialize required files if they don't exist"""
    files_to_init = {
        'streak.txt': '0',
        'last_commit.txt': datetime.now().strftime('%Y-%m-%d')
    }
    
    for filename, initial_content in files_to_init.items():
        filepath = os.path.join(SCRIPT_DIR, filename)
        if not os.path.exists(filepath):
            try:
                with open(filepath, 'w') as f:
                    f.write(initial_content)
                logging.info(f"Created {filename} with initial content")
            except Exception as e:
                logging.error(f"Error creating {filename}: {e}")

def main():
    try:
        logging.info("Starting scheduled commit task")
        config = load_config()
        
        # Initialize required files
        initialize_files()
        
        # Verify repository path exists
        if not os.path.exists(config["repo_path"]):
            logging.error(f"Repository path does not exist: {config['repo_path']}")
            return

        # Check for missed days
        last_commit_date = get_last_commit_date()
        missed_days = check_missed_days(last_commit_date)
        
        # Determine number of commits for today
        num_commits = random.randint(config["min_commits"], config["max_commits"])
        logging.info(f"Attempting to make {num_commits} commits today")
        
        # Make multiple commits
        successful_commits = 0
        commit_messages = []
        
        for i in range(num_commits):
            success, message = make_commit(config)
            if success:
                successful_commits += 1
                commit_messages.append(message)
                if i < num_commits - 1:
                    time.sleep(config["commit_delay"])
            else:
                logging.error(f"Failed to make commit: {message}")
                break

        # Update streak and last commit date if all commits were successful
        if successful_commits == num_commits:
            current_streak = get_streak_count()
            if missed_days <= 1:  # Only update streak if no days were missed
                update_streak_count(current_streak + 1)
                logging.info(f"Current streak: {current_streak + 1} days")
            else:
                update_streak_count(1)  # Reset streak to 1
                logging.info("Streak reset to 1 due to missed days")
            update_last_commit_date()
        
        # Log results
        logging.info(f"Made {successful_commits}/{num_commits} commits successfully. "
                    f"Messages: {', '.join(commit_messages)}")

    except Exception as e:
        logging.error(f"Script failed with error: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
