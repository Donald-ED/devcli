"""
Git Integration for DevCLI

Tracks file changes, diffs, and provides context like Claude Code does.
"""
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import subprocess
from dataclasses import dataclass


@dataclass
class FileChange:
    """Represents a changed file"""
    path: str
    status: str  # 'M' (modified), 'A' (added), 'D' (deleted), etc.
    diff: Optional[str] = None
    

class GitTracker:
    """
    Track git changes and provide context about modifications.
    
    This helps the AI understand:
    - What files have changed
    - What the actual changes are
    - Recent commit history
    """
    
    def __init__(self, repo_path: Path):
        """
        Initialize git tracker.
        
        Args:
            repo_path: Root of git repository
        """
        self.repo_path = Path(repo_path)
        self._is_git_repo = self._check_git_repo()
    
    def _check_git_repo(self) -> bool:
        """Check if directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def is_git_repo(self) -> bool:
        """Check if this is a git repository"""
        return self._is_git_repo
    
    def get_uncommitted_changes(self) -> List[FileChange]:
        """
        Get all uncommitted changes (staged and unstaged).
        
        Returns:
            List of FileChange objects
        """
        if not self._is_git_repo:
            return []
        
        try:
            # Get status
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            changes = []
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                
                # Parse git status format: "?? file.py" or " M file.py"
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    status, file_path = parts
                    status = status.strip()
                    changes.append(FileChange(
                        path=file_path,
                        status=status
                    ))
            
            return changes
            
        except Exception as e:
            print(f"Error getting git changes: {e}")
            return []
    
    def get_diff(self, file_path: str, cached: bool = False) -> str:
        """
        Get diff for a specific file.
        
        Args:
            file_path: Path to file
            cached: If True, get staged diff; if False, get unstaged diff
            
        Returns:
            Diff string
        """
        if not self._is_git_repo:
            return ""
        
        try:
            cmd = ["git", "diff"]
            if cached:
                cmd.append("--cached")
            cmd.append(file_path)
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.stdout
            
        except Exception:
            return ""
    
    def get_all_diffs(self) -> Dict[str, str]:
        """
        Get diffs for all changed files.
        
        Returns:
            Dict mapping file paths to their diffs
        """
        changes = self.get_uncommitted_changes()
        diffs = {}
        
        for change in changes:
            # Try unstaged first
            diff = self.get_diff(change.path, cached=False)
            if not diff:
                # Try staged
                diff = self.get_diff(change.path, cached=True)
            
            if diff:
                diffs[change.path] = diff
        
        return diffs
    
    def get_recent_commits(self, count: int = 5) -> List[Dict[str, str]]:
        """
        Get recent commit history.
        
        Args:
            count: Number of commits to retrieve
            
        Returns:
            List of commit info dicts
        """
        if not self._is_git_repo:
            return []
        
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--pretty=format:%H|%an|%ae|%ad|%s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split('|', maxsplit=4)
                if len(parts) == 5:
                    commits.append({
                        'hash': parts[0][:7],  # Short hash
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    })
            
            return commits
            
        except Exception:
            return []
    
    def get_changed_files_since(self, since: str = "HEAD~5") -> List[str]:
        """
        Get files changed since a specific commit.
        
        Args:
            since: Git reference (e.g., "HEAD~5", "main", commit hash)
            
        Returns:
            List of file paths
        """
        if not self._is_git_repo:
            return []
        
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", since],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            return [f for f in result.stdout.strip().split('\n') if f]
            
        except Exception:
            return []
    
    def get_file_at_commit(self, file_path: str, commit: str = "HEAD") -> str:
        """
        Get file content at a specific commit.
        
        Args:
            file_path: Path to file
            commit: Git reference
            
        Returns:
            File content at that commit
        """
        if not self._is_git_repo:
            return ""
        
        try:
            result = subprocess.run(
                ["git", "show", f"{commit}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.stdout if result.returncode == 0 else ""
            
        except Exception:
            return ""
    
    def format_context_string(self) -> str:
        """
        Format git changes as context string for AI.
        
        This creates a summary like:
        "Recently modified: cli.py, config.py
         Latest commits: Added feature X, Fixed bug Y"
        
        Returns:
            Formatted context string
        """
        if not self._is_git_repo:
            return "# Not a git repository\n"
        
        lines = ["# Git Context\n"]
        
        # Uncommitted changes
        changes = self.get_uncommitted_changes()
        if changes:
            lines.append("## Uncommitted Changes:")
            for change in changes:
                status_map = {
                    'M': 'Modified',
                    'A': 'Added',
                    'D': 'Deleted',
                    '??': 'Untracked',
                    'MM': 'Modified (staged & unstaged)',
                    'AM': 'Added & modified'
                }
                status_desc = status_map.get(change.status, change.status)
                lines.append(f"  - {change.path} ({status_desc})")
            lines.append("")
        
        # Recent commits
        commits = self.get_recent_commits(3)
        if commits:
            lines.append("## Recent Commits:")
            for commit in commits:
                lines.append(f"  - {commit['hash']}: {commit['message']}")
            lines.append("")
        
        return "\n".join(lines)


# Test if run directly
if __name__ == "__main__":
    """Test git tracker"""
    import sys
    
    test_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print(f"Testing GitTracker with: {test_path}\n")
    
    tracker = GitTracker(test_path)
    
    if not tracker.is_git_repo():
        print("❌ Not a git repository!")
        sys.exit(1)
    
    print("✅ Git repository detected\n")
    
    # Test 1: Uncommitted changes
    print("=== Uncommitted Changes ===")
    changes = tracker.get_uncommitted_changes()
    for change in changes:
        print(f"  {change.status} {change.path}")
    print()
    
    # Test 2: Recent commits
    print("=== Recent Commits ===")
    commits = tracker.get_recent_commits(5)
    for commit in commits:
        print(f"  {commit['hash']} - {commit['message']}")
    print()
    
    # Test 3: Format context
    print("=== Formatted Context ===")
    context = tracker.format_context_string()
    print(context)
