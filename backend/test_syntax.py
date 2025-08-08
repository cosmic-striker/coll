#!/usr/bin/env python3
"""
Syntax validation script for the backend application

This script checks for basic Python syntax errors without importing
external dependencies.
"""

import ast
import os
import sys

def check_python_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(source, filename=file_path)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def find_python_files(directory):
    """Find all Python files in a directory"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def main():
    """Main validation function"""
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    python_files = find_python_files(backend_dir)
    
    print("=== Python Syntax Validation ===")
    print(f"Checking {len(python_files)} Python files...\n")
    
    errors = []
    
    for file_path in python_files:
        rel_path = os.path.relpath(file_path, backend_dir)
        is_valid, error = check_python_syntax(file_path)
        
        if is_valid:
            print(f"✅ {rel_path}")
        else:
            print(f"❌ {rel_path}: {error}")
            errors.append((rel_path, error))
    
    print(f"\n=== Summary ===")
    print(f"Total files: {len(python_files)}")
    print(f"Valid files: {len(python_files) - len(errors)}")
    print(f"Files with errors: {len(errors)}")
    
    if errors:
        print("\n=== Errors ===")
        for file_path, error in errors:
            print(f"{file_path}: {error}")
        return 1
    else:
        print("\n🎉 All Python files have valid syntax!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
