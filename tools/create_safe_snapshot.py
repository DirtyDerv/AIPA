#!/usr/bin/env python3
import os, shutil, pathlib, datetime, subprocess, sys

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

def should_exclude(path: pathlib.Path) -> bool:
    # Exclude by name or if any part matches .git or .venv
    for part in path.parts:
        if part in exclude_names:
            return True
    # Check against the full relative path (posix style) so patterns like
    # 'docs/WORKLOG_COMPLETE.md' match correctly, not just the final filename.
    rel_str = str(path.as_posix()).lower()
    for patt in exclude_patterns:
        if patt.lower() in rel_str:
            return True
    # Skip virtual env directories typical names
    if any(p.startswith('.venv') or p.startswith('venv') for p in path.parts):
        return True
    return False


def copy_tree(src: pathlib.Path, dst: pathlib.Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        rel = item.relative_to(root)
        if should_exclude(rel):
            # print('Excluding', rel)
            continue
        # Avoid copying the destination (or any ancestor of it) back into itself which
        # can cause infinite recursion and extremely long paths on Windows.
        try:
            # if dest is inside this item, skip it
            if dest.resolve().relative_to(item.resolve()):
                # print('Skipping ancestor of dest', item)
                continue
        except Exception:
            # normal case: dest is not inside item
            pass
        target = dst / item.name
        try:
            if item.is_dir():
                copy_tree(item, target)
            else:
                shutil.copy2(item, target)
        except Exception as e:
            print('Warning copying', item, e)


def run():
    print('Creating snapshot at', dest)
    copy_tree(root, dest)
    # Initialize git repo
    cur = os.getcwd()
    os.chdir(dest)
    try:
        subprocess.check_call(['git', 'init'])
        subprocess.check_call(['git', 'add', '--all'])
        subprocess.check_call(['git', 'commit', '-m', f'Safe snapshot {timestamp}'])
        # Try to set origin from parent repo if exists
        try:
            origin = subprocess.check_output(['git', '-C', str(root), 'remote', 'get-url', 'origin']).decode().strip()
            subprocess.check_call(['git', 'remote', 'add', 'origin', origin])
            branch = f'safe-snapshot-{timestamp}'
            subprocess.check_call(['git', 'branch', '-M', branch])
            print('Attempting to push snapshot branch to origin:', branch)
            subprocess.check_call(['git', 'push', '-u', 'origin', branch])
            print('Push completed')
        except subprocess.CalledProcessError as e:
            print('Push failed or no origin configured:', e)
            print('Snapshot created locally at', dest)
    finally:
        os.chdir(cur)


if __name__ == '__main__':
    run()
