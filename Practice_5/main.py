import os
import subprocess

def visualize_commit_graph(dir):
    git_dir = os.path.join(dir, ".git")

    if not os.path.exists(git_dir):
        print("Папка .git не найдена.")
        return

    cmd = ["git", "--git-dir=" + git_dir, "log", "--all", "--oneline", "--graph"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    commit_logs = result.stdout.strip().split("\n")

    for commit_log in commit_logs:
        print(commit_log)

# Direction for parse
dir = "C:\\Users\\shilo\\Документы\\GIT\\SIAOD"
visualize_commit_graph(dir)