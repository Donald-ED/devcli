"""
File Operations Manager

Handles reading, writing, and editing files with proper tracking.
Like Claude Code's file operations.
"""
from pathlib import Path
from typing import Optional, List, Tuple
import difflib
from dataclasses import dataclass


@dataclass
class FileEdit:
    """Represents an edit to be made"""
    file_path: Path
    old_content: str
    new_content: str
    description: str


class FileOpsManager:
    """
    Manage file operations (read, write, edit) with tracking.
    
    This allows the AI to:
    - Read files
    - Write new files
    - Edit existing files
    - See diffs before applying
    """
    
    def __init__(self, root_path: Path):
        """
        Initialize file operations manager.
        
        Args:
            root_path: Root directory for operations
        """
        self.root_path = Path(root_path)
        self.pending_edits: List[FileEdit] = []
    
    def read_file(self, file_path: Path, add_line_numbers: bool = False) -> Optional[str]:
        """
        Read a file's content.
        
        Args:
            file_path: Path to file (relative or absolute)
            add_line_numbers: If True, prefix each line with number
            
        Returns:
            File content or None if error
        """
        # Resolve path
        if not file_path.is_absolute():
            file_path = self.root_path / file_path
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            if add_line_numbers:
                lines = content.split('\n')
                numbered = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
                return '\n'.join(numbered)
            
            return content
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def write_file(self, file_path: Path, content: str, create_dirs: bool = True) -> bool:
        """
        Write content to a file.
        
        Args:
            file_path: Path to file
            content: Content to write
            create_dirs: If True, create parent directories
            
        Returns:
            True if successful
        """
        # Resolve path
        if not file_path.is_absolute():
            file_path = self.root_path / file_path
        
        try:
            # Create parent directories if needed
            if create_dirs:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_path.write_text(content, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    def edit_file(
        self, 
        file_path: Path, 
        search: str, 
        replace: str,
        description: str = "Edit file"
    ) -> Optional[FileEdit]:
        """
        Edit a file by searching and replacing.
        
        Args:
            file_path: Path to file
            search: Text to search for (must be unique!)
            replace: Text to replace with
            description: Description of the edit
            
        Returns:
            FileEdit object if successful, None otherwise
        """
        # Read current content
        old_content = self.read_file(file_path)
        if old_content is None:
            return None
        
        # Check if search text exists and is unique
        occurrences = old_content.count(search)
        if occurrences == 0:
            print(f"Search text not found in {file_path}")
            return None
        elif occurrences > 1:
            print(f"Search text appears {occurrences} times - must be unique!")
            return None
        
        # Perform replacement
        new_content = old_content.replace(search, replace)
        
        # Create edit object
        edit = FileEdit(
            file_path=file_path,
            old_content=old_content,
            new_content=new_content,
            description=description
        )
        
        return edit
    
    def edit_file_lines(
        self,
        file_path: Path,
        start_line: int,
        end_line: int,
        new_lines: List[str],
        description: str = "Edit lines"
    ) -> Optional[FileEdit]:
        """
        Edit specific lines in a file.
        
        Args:
            file_path: Path to file
            start_line: Starting line number (1-indexed)
            end_line: Ending line number (1-indexed, inclusive)
            new_lines: New lines to replace with
            description: Description of edit
            
        Returns:
            FileEdit object if successful
        """
        # Read current content
        old_content = self.read_file(file_path)
        if old_content is None:
            return None
        
        # Split into lines
        lines = old_content.split('\n')
        
        # Validate line numbers
        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            print(f"Invalid line range: {start_line}-{end_line}")
            return None
        
        # Replace lines (convert to 0-indexed)
        new_lines_list = lines[:start_line-1] + new_lines + lines[end_line:]
        new_content = '\n'.join(new_lines_list)
        
        # Create edit
        edit = FileEdit(
            file_path=file_path,
            old_content=old_content,
            new_content=new_content,
            description=description
        )
        
        return edit
    
    def show_diff(self, edit: FileEdit) -> str:
        """
        Generate a unified diff for an edit.
        
        Args:
            edit: FileEdit object
            
        Returns:
            Unified diff string
        """
        old_lines = edit.old_content.splitlines(keepends=True)
        new_lines = edit.new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{edit.file_path}",
            tofile=f"b/{edit.file_path}",
            lineterm=''
        )
        
        return ''.join(diff)
    
    def apply_edit(self, edit: FileEdit, show_diff: bool = True) -> bool:
        """
        Apply an edit to a file.
        
        Args:
            edit: FileEdit to apply
            show_diff: If True, print diff before applying
            
        Returns:
            True if successful
        """
        if show_diff:
            print(f"\n=== {edit.description} ===")
            print(self.show_diff(edit))
            print()
        
        return self.write_file(edit.file_path, edit.new_content)
    
    def add_to_pending(self, edit: FileEdit):
        """Add an edit to pending list (for batch operations)"""
        self.pending_edits.append(edit)
    
    def show_pending_edits(self) -> str:
        """Show all pending edits"""
        if not self.pending_edits:
            return "No pending edits"
        
        output = []
        for i, edit in enumerate(self.pending_edits, 1):
            output.append(f"\n{i}. {edit.description}")
            output.append(self.show_diff(edit))
        
        return '\n'.join(output)
    
    def apply_all_pending(self) -> Tuple[int, int]:
        """
        Apply all pending edits.
        
        Returns:
            (success_count, failure_count)
        """
        success = 0
        failed = 0
        
        for edit in self.pending_edits:
            if self.apply_edit(edit, show_diff=False):
                success += 1
            else:
                failed += 1
        
        self.pending_edits.clear()
        return success, failed
    
    def clear_pending(self):
        """Clear all pending edits"""
        self.pending_edits.clear()
    
    def create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Path to backup file
        """
        content = self.read_file(file_path)
        if content is None:
            return None
        
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        if self.write_file(backup_path, content):
            return backup_path
        return None


# Test if run directly
if __name__ == "__main__":
    """Test file operations"""
    import sys
    from pathlib import Path
    
    test_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print(f"Testing FileOpsManager with: {test_path}\n")
    
    ops = FileOpsManager(test_path)
    
    # Create a test file
    test_file = test_path / "test_edit.txt"
    
    print("=== Creating test file ===")
    ops.write_file(test_file, "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
    print(f"Created: {test_file}\n")
    
    # Read with line numbers
    print("=== Reading file ===")
    content = ops.read_file(test_file, add_line_numbers=True)
    print(content)
    print()
    
    # Edit via search/replace
    print("=== Testing search/replace ===")
    edit = ops.edit_file(
        test_file,
        search="Line 3",
        replace="Modified Line 3",
        description="Update line 3"
    )
    
    if edit:
        print("Diff:")
        print(ops.show_diff(edit))
        print()
        
        # Apply it
        ops.apply_edit(edit, show_diff=False)
        print("✅ Applied edit\n")
    
    # Edit via line numbers
    print("=== Testing line edit ===")
    edit2 = ops.edit_file_lines(
        test_file,
        start_line=1,
        end_line=2,
        new_lines=["New Line 1", "New Line 2"],
        description="Replace first two lines"
    )
    
    if edit2:
        print("Diff:")
        print(ops.show_diff(edit2))
        
        # Add to pending
        ops.add_to_pending(edit2)
        print("Added to pending\n")
    
    # Show pending
    print("=== Pending Edits ===")
    print(ops.show_pending_edits())
    print()
    
    # Apply pending
    print("=== Applying pending ===")
    success, failed = ops.apply_all_pending()
    print(f"✅ {success} successful, ❌ {failed} failed\n")
    
    # Show final result
    print("=== Final content ===")
    final = ops.read_file(test_file, add_line_numbers=True)
    print(final)
    
    # Clean up
    test_file.unlink()
    print(f"\n🗑️  Cleaned up test file")
