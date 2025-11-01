#!/usr/bin/env python3
"""
Finish Day Agent
Automatically commits and syncs the AIPA project to GitHub with intelligent commit messages
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FinishDayAgent:
    """
    Autonomous agent that handles end-of-day GitHub synchronization
    """

    def __init__(self, project_path: str = None):
        self.project_path = Path(project_path or os.getcwd())
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.git_initialized = False
        self.changes_detected = False
        self.commit_message = ""

    def run(self, auto_commit: bool = False):
        """
        Main execution flow
        """
        print("🤖 Finish Day Agent Starting...")
        print(f"📁 Project: {self.project_path}")
        print()

        # Step 1: Check Git initialization
        if not self._check_git_initialized():
            print("⚠️  Git not initialized. Initializing now...")
            self._initialize_git()

        # Step 2: Check for changes
        print("🔍 Checking for changes...")
        status = self._get_git_status()

        if not status['has_changes']:
            print("✅ No changes to commit. Project is up to date!")
            return

        # Step 3: Display changes
        print("\n📝 Changes detected:")
        self._display_changes(status)

        # Step 4: Generate intelligent commit message
        print("\n🧠 Generating intelligent commit message...")
        self.commit_message = self._generate_commit_message(status)

        print(f"\n💬 Proposed commit message:")
        print("─" * 60)
        print(self.commit_message)
        print("─" * 60)

        # Step 5: Confirm or auto-commit
        if not auto_commit:
            response = input("\n❓ Proceed with commit and push? (y/n/e to edit): ").lower()

            if response == 'e':
                print("\n✏️  Enter your commit message (press Enter twice to finish):")
                lines = []
                while True:
                    line = input()
                    if line == "" and len(lines) > 0:
                        break
                    lines.append(line)
                self.commit_message = "\n".join(lines)
            elif response != 'y':
                print("❌ Commit cancelled.")
                return

        # Step 6: Stage all changes
        print("\n📦 Staging changes...")
        self._stage_changes()

        # Step 7: Commit
        print("💾 Creating commit...")
        self._create_commit()

        # Step 8: Push to GitHub
        print("🚀 Pushing to GitHub...")
        push_result = self._push_to_github()

        # Step 9: Verify sync
        print("✓ Verifying synchronization...")
        if self._verify_sync():
            print("\n✅ SUCCESS! Project fully synchronized with GitHub")
            print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 Files changed: {status['stats']['files_changed']}")
            print(f"➕ Additions: {status['stats']['insertions']}")
            print(f"➖ Deletions: {status['stats']['deletions']}")

            # Send summary to Telegram (if configured)
            self._send_summary_to_telegram()
        else:
            print("\n⚠️  Warning: Sync verification failed. Check git status manually.")

    def _check_git_initialized(self) -> bool:
        """Check if git is initialized in the project"""
        git_dir = self.project_path / '.git'
        return git_dir.exists()

    def _initialize_git(self):
        """Initialize git repository"""
        try:
            # Initialize git
            subprocess.run(['git', 'init'], cwd=self.project_path, check=True)

            # Set default branch to main
            subprocess.run(['git', 'branch', '-M', 'main'], cwd=self.project_path, check=True)

            # Check if remote exists
            result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            if 'origin' not in result.stdout:
                print("\n⚙️  GitHub repository URL needed.")
                print("Create a repository on GitHub first, then enter the URL:")
                repo_url = input("Enter repository URL (e.g., https://github.com/username/AIPA.git): ")

                subprocess.run(
                    ['git', 'remote', 'add', 'origin', repo_url],
                    cwd=self.project_path,
                    check=True
                )

            print("✅ Git initialized successfully")
            self.git_initialized = True

        except subprocess.CalledProcessError as e:
            print(f"❌ Error initializing git: {e}")
            sys.exit(1)

    def _get_git_status(self) -> Dict:
        """Get detailed git status"""
        try:
            # Get status
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )

            # Get diff stats
            diff_result = subprocess.run(
                ['git', 'diff', '--stat', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            # Parse status
            status_lines = status_result.stdout.strip().split('\n')
            status_lines = [line for line in status_lines if line]  # Remove empty lines

            # Categorize changes
            new_files = []
            modified_files = []
            deleted_files = []

            for line in status_lines:
                status_code = line[:2]
                filename = line[3:]

                if status_code.strip() == 'A' or status_code.strip() == '??':
                    new_files.append(filename)
                elif status_code.strip() == 'M':
                    modified_files.append(filename)
                elif status_code.strip() == 'D':
                    deleted_files.append(filename)
                else:
                    modified_files.append(filename)  # Default to modified

            # Parse diff stats
            stats = {
                'files_changed': len(new_files) + len(modified_files) + len(deleted_files),
                'insertions': 0,
                'deletions': 0
            }

            if diff_result.stdout:
                stats_line = diff_result.stdout.strip().split('\n')[-1]
                if 'insertion' in stats_line:
                    parts = stats_line.split(',')
                    for part in parts:
                        if 'insertion' in part:
                            stats['insertions'] = int(part.strip().split()[0])
                        if 'deletion' in part:
                            stats['deletions'] = int(part.strip().split()[0])

            return {
                'has_changes': len(status_lines) > 0,
                'new_files': new_files,
                'modified_files': modified_files,
                'deleted_files': deleted_files,
                'stats': stats,
                'raw_output': status_result.stdout
            }

        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting git status: {e}")
            return {'has_changes': False}

    def _display_changes(self, status: Dict):
        """Display changes in a readable format"""
        if status['new_files']:
            print(f"\n  📄 New files ({len(status['new_files'])}):")
            for file in status['new_files'][:10]:  # Show first 10
                print(f"     + {file}")
            if len(status['new_files']) > 10:
                print(f"     ... and {len(status['new_files']) - 10} more")

        if status['modified_files']:
            print(f"\n  ✏️  Modified files ({len(status['modified_files'])}):")
            for file in status['modified_files'][:10]:
                print(f"     ~ {file}")
            if len(status['modified_files']) > 10:
                print(f"     ... and {len(status['modified_files']) - 10} more")

        if status['deleted_files']:
            print(f"\n  🗑️  Deleted files ({len(status['deleted_files'])}):")
            for file in status['deleted_files'][:10]:
                print(f"     - {file}")
            if len(status['deleted_files']) > 10:
                print(f"     ... and {len(status['deleted_files']) - 10} more")

    def _generate_commit_message(self, status: Dict) -> str:
        """
        Use Claude to generate an intelligent commit message based on changes
        """
        try:
            # Get detailed diff for significant files
            diff_output = subprocess.run(
                ['git', 'diff', '--stat', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            # Prepare context for Claude
            context = f"""
Analyze these Git changes and generate a professional commit message.

Changes Summary:
- New files: {len(status['new_files'])}
- Modified files: {len(status['modified_files'])}
- Deleted files: {len(status['deleted_files'])}

New files:
{chr(10).join(status['new_files'][:20])}

Modified files:
{chr(10).join(status['modified_files'][:20])}

Diff stats:
{diff_output.stdout}

Generate a commit message following conventional commits format:
- Start with type: feat, fix, docs, refactor, test, chore, etc.
- Include scope if relevant
- Write clear, concise description
- Add bullet points for major changes if needed

Format:
type(scope): brief description

- Detailed point 1
- Detailed point 2
"""

            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": context
                    }
                ]
            )

            commit_message = response.content[0].text.strip()

            # Add timestamp footer
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            commit_message += f"\n\nAuto-generated by Finish Day Agent\nTimestamp: {timestamp}"

            return commit_message

        except Exception as e:
            print(f"⚠️  Could not generate AI commit message: {e}")
            # Fallback to basic message
            return self._generate_basic_commit_message(status)

    def _generate_basic_commit_message(self, status: Dict) -> str:
        """Fallback commit message if AI generation fails"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        changes = []
        if status['new_files']:
            changes.append(f"add {len(status['new_files'])} new files")
        if status['modified_files']:
            changes.append(f"update {len(status['modified_files'])} files")
        if status['deleted_files']:
            changes.append(f"remove {len(status['deleted_files'])} files")

        change_summary = ", ".join(changes)

        return f"chore: end of day commit - {change_summary}\n\nTimestamp: {timestamp}"

    def _stage_changes(self):
        """Stage all changes"""
        try:
            subprocess.run(
                ['git', 'add', '.'],
                cwd=self.project_path,
                check=True
            )
            print("✅ Changes staged")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error staging changes: {e}")
            sys.exit(1)

    def _create_commit(self):
        """Create git commit"""
        try:
            subprocess.run(
                ['git', 'commit', '-m', self.commit_message],
                cwd=self.project_path,
                check=True
            )
            print("✅ Commit created")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating commit: {e}")
            sys.exit(1)

    def _push_to_github(self) -> bool:
        """Push commits to GitHub"""
        try:
            # First, try to pull in case there are remote changes
            print("   Pulling latest changes...")
            pull_result = subprocess.run(
                ['git', 'pull', 'origin', 'main', '--rebase'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            # Now push
            print("   Pushing to remote...")
            push_result = subprocess.run(
                ['git', 'push', '-u', 'origin', 'main'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )

            print("✅ Pushed to GitHub successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Error pushing to GitHub: {e}")
            print(f"   Error output: {e.stderr if hasattr(e, 'stderr') else 'N/A'}")

            # Try to give helpful advice
            if 'rejected' in str(e.stderr):
                print("\n💡 Tip: Remote has changes you don't have locally.")
                print("   Run: git pull origin main --rebase")
            elif 'authentication' in str(e.stderr).lower():
                print("\n💡 Tip: Authentication failed. Check your GitHub credentials.")

            return False

    def _verify_sync(self) -> bool:
        """Verify local and remote are in sync"""
        try:
            # Fetch remote
            subprocess.run(
                ['git', 'fetch', 'origin'],
                cwd=self.project_path,
                capture_output=True,
                check=True
            )

            # Check if local is behind or ahead
            status = subprocess.run(
                ['git', 'status', '-sb'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )

            output = status.stdout

            # Check for "ahead" or "behind"
            if 'behind' in output:
                print("⚠️  Local is behind remote")
                return False
            elif 'ahead' in output:
                print("⚠️  Local is ahead of remote (push may have failed)")
                return False
            else:
                return True

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Could not verify sync: {e}")
            return False

    def _send_summary_to_telegram(self):
        """Send summary to Telegram (if configured)"""
        try:
            import requests

            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            user_id = os.getenv('TELEGRAM_USER_ID')

            if not bot_token or not user_id:
                return  # Telegram not configured

            message = f"""
🎉 **End of Day - GitHub Sync Complete**

📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Commit Message:**
```
{self.commit_message}
```

✅ Project synchronized with GitHub
"""

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': user_id,
                'text': message,
                'parse_mode': 'Markdown'
            }

            requests.post(url, json=data, timeout=5)

        except Exception as e:
            # Silently fail if Telegram notification doesn't work
            pass

    def generate_daily_summary(self) -> str:
        """
        Generate a summary of what was accomplished today
        """
        try:
            # Get commits from today
            today = datetime.now().strftime('%Y-%m-%d')
            log_result = subprocess.run(
                ['git', 'log', '--since', today, '--oneline'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )

            commits_today = log_result.stdout.strip().split('\n')
            commits_today = [c for c in commits_today if c]  # Remove empty

            if not commits_today:
                return "No commits today yet."

            summary = f"📊 **Today's Activity Summary**\n\n"
            summary += f"Total commits: {len(commits_today)}\n\n"
            summary += "**Commits:**\n"
            for commit in commits_today[:5]:  # Show last 5
                summary += f"  • {commit}\n"

            return summary

        except Exception as e:
            return f"Could not generate summary: {e}"


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Finish Day Agent - Sync project to GitHub')
    parser.add_argument('--auto', action='store_true', help='Auto-commit without confirmation')
    parser.add_argument('--path', type=str, help='Project path (default: current directory)')
    parser.add_argument('--summary', action='store_true', help='Show daily summary only')

    args = parser.parse_args()

    agent = FinishDayAgent(project_path=args.path)

    if args.summary:
        print(agent.generate_daily_summary())
    else:
        agent.run(auto_commit=args.auto)


if __name__ == "__main__":
    main()
