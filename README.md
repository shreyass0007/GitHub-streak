
# 🔁 Auto Git Daily Commit Bot

Automate your daily GitHub contributions with scheduled, randomized commits — and keep your commit streak alive effortlessly.

## 📌 Features

* ✅ Automatically commits daily to a dummy repository
* 🔀 Random commit messages and content
* 🔁 Tracks daily commit streaks
* 📅 Detects and logs missed days
* 🛠 Logs everything in `git_commits.log`
* 📁 Fully customizable via `config.json`

---

## 📂 Project Structure

```
AutoGitBot/
│
├── main.py              # Main script with logging and error handling
├── config.json          # Configurable repo path, branch, commit limits
├── daily_streak.txt     # Updated with each commit (content added)
├── streak.txt           # Stores current streak count
├── last_commit.txt      # Stores date of last commit
├── git_commits.log      # Full activity and error log
└── README.md            # Documentation
```

---

## ⚙️ Configuration (`config.json`)

The first time the script runs, it generates a default `config.json` file.

```json
{
  "repo_path": "C:\\Users\\shrey\\Documents\\DummyRepo",
  "min_commits": 1,
  "max_commits": 10,
  "commit_delay": 2,
  "branch": "main"
}
```

### Options:

* **repo\_path**: Full path to your dummy Git repository
* **min\_commits / max\_commits**: Random number of commits daily
* **commit\_delay**: Delay (in seconds) between each commit
* **branch**: Branch name (default: `main`)

---

## 🚀 How It Works

1. Checks `last_commit.txt` to determine if previous days were missed.
2. Makes a random number of commits (`min_commits` to `max_commits`) to `daily_streak.txt`.
3. Uses randomized messages/content.
4. Updates `streak.txt` and `last_commit.txt` if successful.
5. Logs everything in `git_commits.log`.

---

## 🛠️ Setup Instructions

### 1. ✅ Prerequisites

* Python 3.x installed
* Git installed and configured
* A dummy GitHub repository (cloned locally)

### 2. 📁 Clone or Create a Dummy Repo

```bash
git clone https://github.com/your-username/dummy-repo.git
```

### 3. 📝 Update `config.json`

Set your local repo path and branch name.

### 4. ▶️ Run the Script

```bash
python main.py
```

### 5. ⏱ (Optional) Schedule It Daily

Use Task Scheduler (Windows) or `cron` (Linux/Mac) to run the script daily.

---

## 📄 Log Output Example (`git_commits.log`)

```
2025-06-17 10:00:00 - INFO - Starting scheduled commit task
2025-06-17 10:00:01 - INFO - Attempting to make 3 commits today
2025-06-17 10:00:05 - INFO - Made 3/3 commits successfully. Messages: Keeping the streak alive, Daily update, Level up: Daily commit
2025-06-17 10:00:05 - INFO - Current streak: 12 days
```

---

## 🔐 Error Handling

* Handles:

  * Missing/malformed config or tracking files
  * Git operation failures
  * Missed days in streak
* Logs every failure with traceback in `git_commits.log`

---

## 🌟 Motivation

GitHub contribution graphs can be a great motivator. This tool helps developers:

* Build consistency
* Maintain a green contribution graph
* Practice discipline through automation

---

## 🧠 Pro Tip

Use this only with a **dummy repo**. Avoid automating commits to real codebases to maintain meaningful commit history.

---

## 📌 License

MIT License – feel free to use and modify for personal projects.

---


