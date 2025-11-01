#!/usr/bin/env python3
"""
Universal Finish Day Agent
A Claude-powered end-of-day Git synchronization tool for ANY project

Usage:
    python finish-day.py                    # Interactive mode
    python finish-day.py --auto             # Auto-commit mode
    python finish-day.py --summary          # Show daily summary
    python finish-day.py --analyze          # Analyze changes only
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import json

try:
    import anthropic
except ImportError:
    print("❌ Error: anthropic package not installed")
    print("Run: pip install anthropic")
    sys.exit(1)


class UniversalFinishDayAgent:
    """
    Universal end-of-day agent that works in ANY Git repository
    """

    def __init__(self):
        self.project_path = Path.cwd()
        self.project_name = self.project_path.name

        # Get Claude API key
        self.api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            print("❌ Error: ANTHROPIC_API_KEY or CLAUDE_API_KEY not set")
            print("Set it with: export ANTHROPIC_API_KEY=your-key")
            sys.exit(1)

        self.claude = anthropic.Anthropic(api_key=self.api_key)

    def run(self, mode: str = "interactive"):
        """
        Main execution

        Modes:
        - interactive: Ask for confirmation
        - auto: Auto-commit without asking
        - analyze: Just show what would be committed
        - summary: Show daily summary
        """

        print("╔════════════════════════════════════════════════════════╗")
        print("║       🤖 FINISH DAY AGENT - Claude Powered           ║")
        print("╚════════════════════════════════════════════════════════╝")
        print()
        print(f"📁 Project: {self.project_name}")
        print(f"📂 Path: {self.project_path}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Check if Git repo
        if not self._is_git_repo():
            print("❌ Not a Git repository!")
            print("Initialize with: git init")
            sys.exit(1)

        if mode == "summary":
            self._show_daily_summary()
            return

        # Get Git status
        print("🔍 Analyzing repository...")
        status = self._get_status()

        if not status['has_changes']:
            print("✅ No changes detected. Repository is clean!")
            self._show_daily_summary()
            return

        # Show changes
        self._display_changes(status)

        if mode == "analyze":
            print("\n📊 Analysis complete. No commit made (--analyze mode)")
            return

        # Generate intelligent commit message with Claude
        print("\n🧠 Asking Claude to analyze changes...")
        commit_msg = self._generate_commit_message_with_claude(status)

        print("\n" + "═" * 60)
        print("💬 PROPOSED COMMIT MESSAGE:")
        print("═" * 60)
        print(commit_msg)
        print("═" * 60)

        # Confirm or proceed
        if mode == "interactive":
            choice = input("\n❓ (c)ommit / (e)dit / (s)kip: ").lower()

            if choice == 's':
                print("❌ Commit cancelled")
                return
            elif choice == 'e':
                commit_msg = self._edit_commit_message(commit_msg)

        # Execute Git workflow
        self._execute_git_workflow(commit_msg, status)

    def _is_git_repo(self) -> bool:
        """Check if current directory is a Git repository"""
        return (self.project_path / '.git').exists()

    def _get_status(self) -> dict:
        """Get comprehensive Git status"""
        try:
            # Porcelain status
            result = subprocess.run(
                ['git', 'status', '--porcelain', '-u'],
                capture_output=True,
                text=True,
                check=True
            )

            lines = [l for l in result.stdout.strip().split('\n') if l]

            # Categorize changes
            staged = []
            unstaged = []
            untracked = []

            for line in lines:
                status_code = line[:2]
                filename = line[3:]

                if status_code[0] != ' ' and status_code[0] != '?':
                    staged.append((status_code[0], filename))
                if status_code[1] != ' ':
                    unstaged.append((status_code[1], filename))
                if status_code == '??':
                    untracked.append(filename)

            # Get diff stats
            diff_stat = subprocess.run(
                ['git', 'diff', '--stat', '--cached'] if staged else ['git', 'diff', '--stat'],
                capture_output=True,
                text=True
            )

            # Get file diffs (limited)
            diff_output = subprocess.run(
                ['git', 'diff', '--cached'] if staged else ['git', 'diff'],
                capture_output=True,
                text=True
            )

            # Limit diff to reasonable size
            diff_text = diff_output.stdout[:10000]  # First 10K chars

            return {
                'has_changes': bool(lines),
                'staged': staged,
                'unstaged': unstaged,
                'untracked': untracked,
                'diff_stat': diff_stat.stdout,
                'diff_text': diff_text,
                'total_files': len(lines)
            }

        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            sys.exit(1)

    def _display_changes(self, status: dict):
        """Display changes in readable format"""
        total = status['total_files']
        print(f"\n📊 CHANGES DETECTED: {total} file(s)")

        if status['staged']:
            print(f"\n✅ Staged changes ({len(status['staged'])}):")
            for code, file in status['staged'][:15]:
                icon = {'M': '~', 'A': '+', 'D': '-', 'R': '→'}.get(code, '?')
                print(f"   {icon} {file}")
            if len(status['staged']) > 15:
                print(f"   ... and {len(status['staged']) - 15} more")

        if status['unstaged']:
            print(f"\n⚠️  Unstaged changes ({len(status['unstaged'])}):")
            for code, file in status['unstaged'][:15]:
                icon = {'M': '~', 'D': '-'}.get(code, '?')
                print(f"   {icon} {file}")
            if len(status['unstaged']) > 15:
                print(f"   ... and {len(status['unstaged']) - 15} more")

        if status['untracked']:
            print(f"\n📄 Untracked files ({len(status['untracked'])}):")
            for file in status['untracked'][:15]:
                print(f"   + {file}")
            if len(status['untracked']) > 15:
                print(f"   ... and {len(status['untracked']) - 15} more")

        if status['diff_stat']:
            print(f"\n📈 Statistics:")
            print(status['diff_stat'].strip())

    def _generate_commit_message_with_claude(self, status: dict) -> str:
        """
        Use Claude to generate intelligent commit message
        """

        # Build context for Claude
        context = self._build_context_for_claude(status)

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                temperature=0.3,
                system="""You are an expert software developer helping to create Git commit messages.

Analyze the provided code changes and generate a professional commit message following these guidelines:

1. **Format**: Use Conventional Commits format
   - Type: feat, fix, docs, style, refactor, test, chore, perf
   - Optional scope in parentheses
   - Brief description (50 chars max)
   - Blank line
   - Detailed body with bullet points for significant changes

2. **Style**:
   - Use imperative mood ("Add feature" not "Added feature")
   - Be specific but concise
   - Focus on WHY and WHAT, not HOW
   - Group related changes

3. **Examples**:
   - "feat(auth): add OAuth2 authentication"
   - "fix(api): resolve race condition in user endpoint"
   - "docs: update installation guide with Docker setup"
   - "refactor: simplify database query logic"

Generate ONLY the commit message, no explanations.""",
                messages=[
                    {
                        "role": "user",
                        "content": context
                    }
                ]
            )

            commit_msg = response.content[0].text.strip()

            # Add metadata footer
            commit_msg += f"\n\n🤖 Generated by Finish Day Agent"
            commit_msg += f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            return commit_msg

        except Exception as e:
            print(f"⚠️  Claude API error: {e}")
            print("Falling back to basic commit message...")
            return self._generate_basic_commit_message(status)

    def _build_context_for_claude(self, status: dict) -> str:
        """Build context string for Claude"""

        context = f"Project: {self.project_name}\n\n"
        context += f"Total files changed: {status['total_files']}\n\n"

        # File list
        context += "Changed files:\n"
        for code, file in status['staged'][:30]:
            context += f"  {code} {file}\n"
        for code, file in status['unstaged'][:30]:
            context += f"  {code} {file}\n"
        for file in status['untracked'][:30]:
            context += f"  ? {file}\n"

        # Diff stats
        if status['diff_stat']:
            context += f"\nDiff statistics:\n{status['diff_stat']}\n"

        # Actual diff (truncated)
        if status['diff_text']:
            context += f"\nCode changes (sample):\n```diff\n{status['diff_text'][:3000]}\n```\n"

        context += "\nGenerate a professional commit message for these changes."

        return context

    def _generate_basic_commit_message(self, status: dict) -> str:
        """Fallback commit message if Claude fails"""

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

        # Determine primary type
        has_new = any(c == 'A' or c == '?' for c, _ in status['staged']) or status['untracked']
        has_modified = any(c == 'M' for c, _ in status['staged'] + status['unstaged'])
        has_deleted = any(c == 'D' for c, _ in status['staged'] + status['unstaged'])

        if has_new and not has_modified and not has_deleted:
            type_msg = "feat: add new files"
        elif has_modified and not has_new and not has_deleted:
            type_msg = "chore: update files"
        elif has_deleted:
            type_msg = "chore: remove files and update"
        else:
            type_msg = "chore: update project"

        msg = f"{type_msg}\n\n"
        msg += f"- {status['total_files']} file(s) changed\n"
        msg += f"\n🤖 Auto-generated\n📅 {timestamp}"

        return msg

    def _edit_commit_message(self, original: str) -> str:
        """Allow user to edit commit message"""
        print("\n✏️  Edit commit message (Ctrl+D or Ctrl+Z to finish):")
        print("Current message:")
        print(original)
        print("\nYour message:")

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            pass

        new_msg = '\n'.join(lines).strip()
        return new_msg if new_msg else original

    def _execute_git_workflow(self, commit_msg: str, status: dict):
        """Execute the Git commit and push workflow"""

        print("\n" + "═" * 60)
        print("🚀 EXECUTING GIT WORKFLOW")
        print("═" * 60)

        try:
            # Stage all changes
            print("\n1️⃣  Staging all changes...")
            subprocess.run(['git', 'add', '-A'], check=True)
            print("   ✅ All changes staged")

            # Commit
            print("\n2️⃣  Creating commit...")
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("   ✅ Commit created")

            # Check if remote exists
            remote_result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True
            )

            if not remote_result.stdout:
                print("\n⚠️  No remote repository configured")
                print("   Commit created locally. Push manually when ready.")
                return

            # Get current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = branch_result.stdout.strip()

            # Pull first (rebase)
            print(f"\n3️⃣  Pulling latest changes from {current_branch}...")
            try:
                subprocess.run(
                    ['git', 'pull', 'origin', current_branch, '--rebase'],
                    check=True,
                    capture_output=True
                )
                print("   ✅ Pulled and rebased")
            except subprocess.CalledProcessError:
                print("   ⚠️  No remote tracking branch or conflicts")

            # Push
            print(f"\n4️⃣  Pushing to origin/{current_branch}...")
            push_result = subprocess.run(
                ['git', 'push', 'origin', current_branch],
                capture_output=True,
                text=True
            )

            if push_result.returncode == 0:
                print("   ✅ Pushed successfully!")
            else:
                print("   ⚠️  Push failed or no upstream set")
                print("   Try: git push -u origin " + current_branch)

            # Summary
            print("\n" + "═" * 60)
            print("✅ FINISH DAY COMPLETE!")
            print("═" * 60)
            print(f"📦 Committed: {status['total_files']} files")
            print(f"🌿 Branch: {current_branch}")
            print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")

            # Show recent commits
            self._show_recent_commits(3)

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error during Git workflow: {e}")
            print("Check the error and try manually.")
            sys.exit(1)

    def _show_daily_summary(self):
        """Show summary of today's commits"""
        print("\n📊 TODAY'S SUMMARY")
        print("═" * 60)

        try:
            today = datetime.now().strftime('%Y-%m-%d')
            log_result = subprocess.run(
                ['git', 'log', '--since', f'{today} 00:00', '--oneline', '--no-decorate'],
                capture_output=True,
                text=True
            )

            commits = [c for c in log_result.stdout.strip().split('\n') if c]

            if not commits:
                print("No commits today yet")
            else:
                print(f"Total commits today: {len(commits)}\n")
                for i, commit in enumerate(commits[:5], 1):
                    print(f"{i}. {commit}")
                if len(commits) > 5:
                    print(f"... and {len(commits) - 5} more")

        except subprocess.CalledProcessError:
            print("Could not retrieve commit history")

    def _show_recent_commits(self, count: int = 3):
        """Show recent commits"""
        print(f"\n📝 Recent commits:")
        try:
            log_result = subprocess.run(
                ['git', 'log', f'-{count}', '--oneline', '--no-decorate'],
                capture_output=True,
                text=True
            )
            for line in log_result.stdout.strip().split('\n'):
                if line:
                    print(f"   {line}")
        except subprocess.CalledProcessError:
            pass


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='🤖 Finish Day Agent - Claude-powered Git automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python finish-day.py                 # Interactive mode
  python finish-day.py --auto          # Auto-commit without asking
  python finish-day.py --analyze       # Just show what changed
  python finish-day.py --summary       # Show today's commits

Environment:
  Set ANTHROPIC_API_KEY or CLAUDE_API_KEY before running
        """
    )

    parser.add_argument('--auto', action='store_true',
                       help='Auto-commit without confirmation')
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze changes without committing')
    parser.add_argument('--summary', action='store_true',
                       help="Show today's commit summary")

    args = parser.parse_args()

    # Determine mode
    if args.summary:
        mode = 'summary'
    elif args.analyze:
        mode = 'analyze'
    elif args.auto:
        mode = 'auto'
    else:
        mode = 'interactive'

    # Run agent
    agent = UniversalFinishDayAgent()
    agent.run(mode=mode)


if __name__ == "__main__":
    main()
