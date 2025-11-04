#!/usr/bin/env python3
import os, shutil, pathlib, datetime, subprocess, sys, fnmatch

root = pathlib.Path(__file__).resolve().parents[1]
timestamp = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
dest = root / 'backups' / f'safe_snapshot_{timestamp}'
exclude_names = {
    '.git', '.venv', 'backups', '.gitignore', 'scan_report.txt'
}

# Also ignore temporary snapshot dirs and tmp folders to avoid copying the dest into itself
exclude_names.add('tmp')

# Additional sensitive filenames to exclude
exclude_patterns = [
    'CREDENTIAL_BACKUP', 'CREDENTIALS.md', 'credential_ids.json', 'credential*',
    'discord', 'token', 'credentials', 'credential_ids',
    'CREDENTIAL_BACKUP_20251103_134353.md', 'bot/discord_bot_simple.py',
    'docs/WORKLOG_COMPLETE.md', 'tools/test_discord_connection.py'
]

# Files and directories to always exclude from the snapshot
EXCLUDED_FILES = {
    ".git", ".vscode", "__pycache__", ".idea", "node_modules", "venv", ".venv",
    "*.pyc", "*.pyo", "*.pyd", "*.so", "*.egg-info",
    "*.log", "*.tmp", "*.swp",
    ".DS_Store", "Thumbs.db",
    ".env"  # <-- Explicitly exclude the .env file
}
EXCLUDED_PATTERNS = {
    "backups/safe_snapshot_*", # Exclude previous snapshots
    "tmp_*" # Exclude temporary directories
}

def should_exclude(path: pathlib.Path, root_path: pathlib.Path) -> bool:
    """
    Determines if a file or directory should be excluded from the snapshot.
    """
    # Check against simple name matches (e.g., ".env", ".git")
    if path.name in EXCLUDED_FILES:
        return True

    # Check against patterns for the full relative path
    relative_path_str = str(path.relative_to(root_path).as_posix())
    for pattern in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(relative_path_str, pattern):
            return True
            
    # Legacy checks (can be removed if EXCLUDED_FILES/PATTERNS is comprehensive)
    for part in path.parts:
        if part in exclude_names:
            return True
    rel_str = str(path.as_posix()).lower()
    for patt in exclude_patterns:
        if patt.lower() in rel_str:
            return True

    return False


def copy_tree(src: pathlib.Path, dst: pathlib.Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if should_exclude(item, root):
            # print(f"Excluding: {item.relative_to(root)}")
            continue

        target = dst / item.relative_to(src)

        try:
            if item.is_dir():
                copy_tree(item, target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
        except Exception as e:
            print(f'Warning copying {item}: {e}', file=sys.stderr)


def run_command(command, cwd=None):
    """Runs a command and handles errors."""
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise


def get_git_origin(repo_path):
    """Gets the remote origin URL of a git repository."""
    try:
        origin = subprocess.check_output(
            ['git', '-C', str(repo_path), 'remote', 'get-url', 'origin'],
            stderr=subprocess.STDOUT
        ).decode().strip()
        return origin
    except subprocess.CalledProcessError:
        return None


def main():
    """Main function to create and optionally push the snapshot."""
    push_to_remote = '--push' in sys.argv
    
    print(f"Creating clean snapshot in: {dest}")
    
    try:
        # 1. Copy the project tree to the destination
        copy_tree(root, dest)
        print("Project files copied successfully.")

        # 2. Initialize Git and create the first commit
        print("Initializing Git repository...")
        run_command(['git', 'init'], cwd=dest)
        run_command(['git', 'add', '.'], cwd=dest)
        commit_message = f"Safe snapshot created at {timestamp}"
        run_command(['git', 'commit', '-m', commit_message], cwd=dest)
        print(f"Git commit created: '{commit_message}'")

        if push_to_remote:
            print("Pushing to remote repository...")
            origin_url = get_git_origin(root)
            if origin_url:
                branch_name = f'safe-snapshot/{timestamp}'
                run_command(['git', 'remote', 'add', 'origin', origin_url], cwd=dest)
                run_command(['git', 'branch', '-M', branch_name], cwd=dest)
                print(f"Attempting to push new branch '{branch_name}' to origin.")
                run_command(['git', 'push', '-u', 'origin', branch_name, '--force'], cwd=dest)
                print("="*50)
                print("✅ Snapshot successfully pushed to remote!")
                print(f"Branch: {branch_name}")
                print("="*50)
            else:
                print("Could not determine git origin URL. Skipping push.")
                print(f"Snapshot is available locally at: {dest}")
        else:
            print("Snapshot created locally. To push, run with --push argument.")
            print(f"Path: {dest}")

    except Exception as e:
        print(f"An error occurred during the snapshot process: {e}", file=sys.stderr)
        # Optionally, clean up the destination directory on failure
        # if dest.exists():
        #     print(f"Cleaning up failed snapshot directory: {dest}")
        #     shutil.rmtree(dest)
        sys.exit(1)

if __name__ == '__main__':
    main()
