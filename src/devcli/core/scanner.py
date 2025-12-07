"""
File Scanner

Walks through a project directory and finds all relevant code files.
Respects .gitignore patterns and common ignore patterns.
"""
from pathlib import Path
from typing import List, Set
import fnmatch


class FileScanner:
    """
    Scans a directory for code files, respecting ignore patterns.
    
    This is like what .gitignore does - it finds files but skips
    things like node_modules, .git, __pycache__, etc.
    """
    
    # File extensions we care about
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx',
        '.java', '.c', '.cpp', '.h', '.hpp',
        '.go', '.rs', '.rb', '.php',
        '.html', '.css', '.scss', '.sass',
        '.json', '.yaml', '.yml', '.toml',
        '.md', '.txt', '.sh', '.bash'
    }
    
    # Directories to always ignore
    DEFAULT_IGNORE_DIRS = {
        'node_modules', 'venv', 'env', '.venv',
        '.git', '.svn', '.hg',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'dist', 'build', '.next', '.nuxt',
        'target', 'out', 'bin', 'obj',
        '.idea', '.vscode', '.DS_Store'
    }
    
    # File patterns to ignore
    DEFAULT_IGNORE_PATTERNS = {
        '*.pyc', '*.pyo', '*.pyd',
        '*.so', '*.dll', '*.dylib',
        '*.class', '*.jar', '*.war',
        '*.min.js', '*.min.css',
        '*.map', '*.lock',
        '.env', '.env.*',
        '*.log', '*.sqlite', '*.db'
    }
    
    def __init__(
        self, 
        root_path: Path,
        ignore_dirs: Set[str] = None,
        ignore_patterns: Set[str] = None,
        max_file_size: int = 100_000  # 100KB default
    ):
        """
        Initialize the file scanner.
        
        Args:
            root_path: Root directory to scan
            ignore_dirs: Additional directories to ignore
            ignore_patterns: Additional file patterns to ignore
            max_file_size: Max file size in bytes (skip larger files)
        """
        self.root_path = Path(root_path).resolve()
        self.max_file_size = max_file_size
        
        # Combine default ignores with custom ones
        self.ignore_dirs = self.DEFAULT_IGNORE_DIRS.copy()
        if ignore_dirs:
            self.ignore_dirs.update(ignore_dirs)
        
        self.ignore_patterns = self.DEFAULT_IGNORE_PATTERNS.copy()
        if ignore_patterns:
            self.ignore_patterns.update(ignore_patterns)
    
    def should_ignore_dir(self, dir_path: Path) -> bool:
        """
        Check if a directory should be ignored.
        
        Args:
            dir_path: Path to check
            
        Returns:
            True if should ignore, False otherwise
        """
        dir_name = dir_path.name
        
        # Check if it's in our ignore list
        if dir_name in self.ignore_dirs:
            return True
        
        # Check if it starts with . (hidden)
        if dir_name.startswith('.') and dir_name not in {'.github'}:
            return True
        
        return False
    
    def should_ignore_file(self, file_path: Path) -> bool:
        """
        Check if a file should be ignored.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if should ignore, False otherwise
        """
        file_name = file_path.name
        
        # Check ignore patterns (like *.pyc)
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return True
        
        # Check if it's too large
        try:
            if file_path.stat().st_size > self.max_file_size:
                return True
        except OSError:
            return True
        
        # Check if it has a code extension
        if file_path.suffix not in self.CODE_EXTENSIONS:
            return True
        
        return False
    
    def scan(self) -> List[Path]:
        """
        Scan the directory and return list of code files.
        
        Returns:
            List of Path objects for code files
        """
        code_files = []
        
        # Walk the directory tree
        for item in self.root_path.rglob('*'):
            # Skip if it's in an ignored directory
            # Check if any parent is ignored
            is_in_ignored_dir = False
            for parent in item.parents:
                if parent == self.root_path:
                    break
                if self.should_ignore_dir(parent):
                    is_in_ignored_dir = True
                    break
            
            if is_in_ignored_dir:
                continue
            
            # Only process files
            if not item.is_file():
                continue
            
            # Skip ignored files
            if self.should_ignore_file(item):
                continue
            
            code_files.append(item)
        
        return sorted(code_files)
    
    def get_file_tree(self) -> str:
        """
        Generate a tree view of the project structure.
        
        Returns:
            String representation of the file tree
        """
        files = self.scan()
        
        if not files:
            return "No files found."
        
        # Group files by directory
        tree_lines = [f"📁 {self.root_path.name}/"]
        
        prev_parts = []
        for file_path in files:
            # Get relative path
            rel_path = file_path.relative_to(self.root_path)
            parts = rel_path.parts
            
            # Find where it differs from previous path
            common_len = 0
            for i, (prev, curr) in enumerate(zip(prev_parts, parts[:-1])):
                if prev == curr:
                    common_len = i + 1
                else:
                    break
            
            # Add directory lines
            for i in range(common_len, len(parts) - 1):
                indent = "  " * (i + 1)
                tree_lines.append(f"{indent}📁 {parts[i]}/")
            
            # Add file line
            indent = "  " * len(parts)
            tree_lines.append(f"{indent}📄 {parts[-1]}")
            
            prev_parts = parts[:-1]
        
        return "\n".join(tree_lines)


# Test if run directly
if __name__ == "__main__":
    """
    Test the file scanner.
    
    Run: python src/devcli/core/scanner.py
    """
    import sys
    
    # Scan current directory or provided path
    scan_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print(f"Scanning: {scan_path}\n")
    
    scanner = FileScanner(scan_path)
    files = scanner.scan()
    
    print(f"Found {len(files)} code files:\n")
    print(scanner.get_file_tree())
    
    print(f"\n\nFiles by type:")
    by_ext = {}
    for f in files:
        ext = f.suffix or 'no extension'
        by_ext[ext] = by_ext.get(ext, 0) + 1
    
    for ext, count in sorted(by_ext.items(), key=lambda x: -x[1]):
        print(f"  {ext}: {count} files")
