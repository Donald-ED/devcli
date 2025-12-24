"""
Smart Context Manager

Loads only relevant files based on user questions.
This is inspired by Aider's approach but simplified for quick implementation.

Future: Add tree-sitter for proper AST-based repo maps.
"""
from pathlib import Path
from typing import List, Optional
import re


class SmartContext:
    """
    Smart context manager that loads files on-demand.
    
    Instead of loading all 20 files upfront, this loads only
    what the user is asking about.
    """
    
    def __init__(self, root_path: Path):
        """
        Initialize smart context.
        
        Args:
            root_path: Root of the project
        """
        self.root_path = Path(root_path)
        self._file_cache = {}
        self._repo_structure = None
    
    def get_repo_structure(self) -> str:
        """
        Get a simple map of the repository structure.
        
        This is like Aider's repo map but simpler (no tree-sitter yet).
        Shows all files and their basic structure.
        
        Returns:
            String representation of repo structure
        """
        if self._repo_structure:
            return self._repo_structure
        
        lines = ["# Repository Structure\n"]
        
        # Find all Python files
        py_files = sorted(self.root_path.rglob("*.py"))
        
        for py_file in py_files:
            # Skip common ignore patterns
            if any(skip in str(py_file) for skip in [
                '__pycache__', '.egg-info', 'venv', '.venv', 
                'node_modules', '.git'
            ]):
                continue
            
            rel_path = py_file.relative_to(self.root_path)
            
            # Extract functions and classes (simple regex for now)
            try:
                content = py_file.read_text(encoding='utf-8')
                classes = re.findall(r'^class (\w+)', content, re.MULTILINE)
                functions = re.findall(r'^def (\w+)', content, re.MULTILINE)
                
                lines.append(f"\n{rel_path}:")
                if classes:
                    for cls in classes:
                        lines.append(f"  class {cls}")
                if functions:
                    for func in functions[:10]:  # Limit to first 10
                        lines.append(f"  def {func}()")
                    if len(functions) > 10:
                        lines.append(f"  ... and {len(functions) - 10} more functions")
                
            except Exception:
                # Skip files we can't read
                continue
        
        self._repo_structure = "\n".join(lines)
        return self._repo_structure
    
    def detect_mentioned_files(self, question: str) -> List[Path]:
        """
        Detect which files the user is asking about.
        
        Args:
            question: User's question
            
        Returns:
            List of file paths that were mentioned
        """
        mentioned = []
        question_lower = question.lower()
        
        # Find all Python files
        all_py_files = list(self.root_path.rglob("*.py"))
        
        for py_file in all_py_files:
            # Skip ignored files
            if any(skip in str(py_file) for skip in [
                '__pycache__', '.egg-info', 'venv', '.venv'
            ]):
                continue
            
            # Check if file name is mentioned
            file_name = py_file.name
            rel_path = str(py_file.relative_to(self.root_path))
            
            # Check various ways file might be mentioned
            if (file_name.lower() in question_lower or 
                rel_path.lower() in question_lower or
                py_file.stem.lower() in question_lower):
                mentioned.append(py_file)
        
        return mentioned
    
    def load_file(self, file_path: Path) -> Optional[str]:
        """
        Load a file's content with caching.
        
        Args:
            file_path: Path to file
            
        Returns:
            File content or None if can't read
        """
        if file_path in self._file_cache:
            return self._file_cache[file_path]
        
        try:
            content = file_path.read_text(encoding='utf-8')
            self._file_cache[file_path] = content
            return content
        except Exception:
            return None
    
    def get_context_for_question(self, question: str) -> str:
        """
        Build context based on the user's question.
        
        This is the main method. It:
        1. Always includes repo structure (compact)
        2. Detects mentioned files
        3. Loads full content ONLY for mentioned files
        
        Args:
            question: User's question
            
        Returns:
            Context string to send to AI
        """
        context_parts = []
        
        # 1. Always include repo structure
        context_parts.append(self.get_repo_structure())
        context_parts.append("\n---\n")
        
        # 2. Detect and load mentioned files
        mentioned_files = self.detect_mentioned_files(question)
        
        if mentioned_files:
            context_parts.append("# Full File Contents\n")
            
            for file_path in mentioned_files:
                content = self.load_file(file_path)
                if content:
                    rel_path = file_path.relative_to(self.root_path)
                    # Add line numbers for easier reference
                    lines = content.split('\n')
                    numbered_lines = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
                    numbered_content = '\n'.join(numbered_lines)
                    
                    context_parts.append(f"\n## {rel_path}\n")
                    context_parts.append(f"```python\n{numbered_content}\n```\n")
        
        return "\n".join(context_parts)
    
    def get_file_with_line_numbers(self, file_path: Path) -> str:
        """
        Get file content with line numbers.
        
        Args:
            file_path: Path to file
            
        Returns:
            File content with line numbers
        """
        content = self.load_file(file_path)
        if not content:
            return ""
        
        lines = content.split('\n')
        numbered = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered)


# Test if run directly
if __name__ == "__main__":
    """Test the smart context manager"""
    import sys
    
    test_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print(f"Testing SmartContext with: {test_path}\n")
    
    ctx = SmartContext(test_path)
    
    # Test 1: Get repo structure
    print("=== Repo Structure ===")
    structure = ctx.get_repo_structure()
    print(structure[:500], "...\n")
    
    # Test 2: Detect files in question
    question = "what is on line 200 in cli.py?"
    print(f"=== Question: {question} ===")
    mentioned = ctx.detect_mentioned_files(question)
    print(f"Detected files: {[str(f.name) for f in mentioned]}\n")
    
    # Test 3: Get full context
    print("=== Full Context ===")
    context = ctx.get_context_for_question(question)
    print(f"Context length: {len(context)} chars")
    print(f"Estimated tokens: {len(context) // 4}")
