"""
Context Builder

Reads project files and builds context for the AI to understand your code.
Manages token limits and prioritizes important files.
"""
from pathlib import Path
from typing import List, Dict, Optional
import json
from dataclasses import dataclass, asdict

from devcli.core.scanner import FileScanner


@dataclass
class FileContext:
    """Represents context about a single file."""
    path: str
    relative_path: str
    extension: str
    size: int
    content: str
    lines: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ProjectContext:
    """Represents the overall project context."""
    root_path: str
    name: str
    total_files: int
    total_lines: int
    files: List[FileContext]
    file_tree: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'root_path': self.root_path,
            'name': self.name,
            'total_files': self.total_files,
            'total_lines': self.total_lines,
            'files': [f.to_dict() for f in self.files],
            'file_tree': self.file_tree
        }
    
    def to_prompt(self, max_tokens: int = 4000) -> str:
        """
        Generate a prompt-friendly representation of the project.
        
        Args:
            max_tokens: Rough token limit (1 token ≈ 4 chars)
            
        Returns:
            String representation for AI prompt
        """
        # Start with overview
        prompt = f"""# Project: {self.name}

## Overview
- Total files: {self.total_files}
- Total lines of code: {self.total_lines}

## File Structure
{self.file_tree}

## File Contents
"""
        
        # Add file contents, respecting token limit
        max_chars = max_tokens * 4  # Rough estimate
        current_chars = len(prompt)
        
        files_added = 0
        for file_ctx in self.files:
            # Skip if we're near the limit
            if current_chars > max_chars * 0.9:
                remaining = self.total_files - files_added
                if remaining > 0:
                    prompt += f"\n... and {remaining} more files (truncated to fit token limit)\n"
                break
            
            file_section = f"""
### {file_ctx.relative_path}
```{file_ctx.extension.lstrip('.')}
{file_ctx.content}
```
"""
            current_chars += len(file_section)
            prompt += file_section
            files_added += 1
        
        return prompt


class ContextBuilder:
    """
    Builds project context for AI understanding.
    
    This scans your project, reads files, and creates a summary
    that can be sent to the AI model.
    """
    
    def __init__(self, root_path: Path):
        """
        Initialize the context builder.
        
        Args:
            root_path: Root directory of the project
        """
        self.root_path = Path(root_path).resolve()
        self.scanner = FileScanner(self.root_path)
    
    def read_file_safe(self, file_path: Path) -> Optional[str]:
        """
        Safely read a file's contents.
        
        Args:
            file_path: Path to file
            
        Returns:
            File contents as string, or None if can't read
        """
        try:
            # Try UTF-8 first
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Try latin-1 as fallback
            try:
                return file_path.read_text(encoding='latin-1')
            except Exception:
                return None
        except Exception:
            return None
    
    def build_context(self, max_files: int = 50) -> ProjectContext:
        """
        Build project context by scanning and reading files.
        
        Args:
            max_files: Maximum number of files to include
            
        Returns:
            ProjectContext with all the information
        """
        # Scan for files
        all_files = self.scanner.scan()
        
        # Limit number of files
        files_to_process = all_files[:max_files]
        
        # Build file contexts
        file_contexts = []
        total_lines = 0
        
        for file_path in files_to_process:
            content = self.read_file_safe(file_path)
            if content is None:
                continue
            
            lines = content.count('\n') + 1
            total_lines += lines
            
            file_ctx = FileContext(
                path=str(file_path),
                relative_path=str(file_path.relative_to(self.root_path)),
                extension=file_path.suffix,
                size=file_path.stat().st_size,
                content=content,
                lines=lines
            )
            file_contexts.append(file_ctx)
        
        # Create project context
        return ProjectContext(
            root_path=str(self.root_path),
            name=self.root_path.name,
            total_files=len(file_contexts),
            total_lines=total_lines,
            files=file_contexts,
            file_tree=self.scanner.get_file_tree()
        )
    
    def save_context(self, context: ProjectContext, output_path: Path) -> None:
        """
        Save project context to a JSON file.
        
        Args:
            context: ProjectContext to save
            output_path: Where to save it
        """
        output_path.write_text(
            json.dumps(context.to_dict(), indent=2)
        )
    
    def load_context(self, input_path: Path) -> ProjectContext:
        """
        Load project context from a JSON file.
        
        Args:
            input_path: Path to load from
            
        Returns:
            ProjectContext
        """
        data = json.loads(input_path.read_text())
        
        files = [
            FileContext(**f)
            for f in data['files']
        ]
        
        return ProjectContext(
            root_path=data['root_path'],
            name=data['name'],
            total_files=data['total_files'],
            total_lines=data['total_lines'],
            files=files,
            file_tree=data['file_tree']
        )


# Test if run directly
if __name__ == "__main__":
    """
    Test the context builder.
    
    Run: python src/devcli/core/context.py
    """
    import sys
    
    # Build context for current directory or provided path
    scan_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print(f"Building context for: {scan_path}\n")
    
    builder = ContextBuilder(scan_path)
    context = builder.build_context(max_files=10)  # Limit for demo
    
    print(f"Project: {context.name}")
    print(f"Files: {context.total_files}")
    print(f"Lines: {context.total_lines}")
    print(f"\nFile tree:\n{context.file_tree}")
    
    # Show what the prompt would look like (truncated)
    prompt = context.to_prompt(max_tokens=1000)
    if len(prompt) > 500:
        print(f"\nPrompt preview (first 500 chars):\n{prompt[:500]}...")
    else:
        print(f"\nFull prompt:\n{prompt}")
