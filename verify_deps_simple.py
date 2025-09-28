#!/usr/bin/env python3
"""
Simplified dependency verification script for Windows compatibility.
Verifies that configgen.py uses only Python standard library modules.
"""

import ast
import sys
import os

def verify_stdlib_imports():
    """Simple verification that only stdlib imports are used."""
    
    print("Verifying Python standard library imports...")
    
    # Read configgen.py
    try:
        with open('configgen.py', 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading configgen.py: {e}")
        return False
    
    # Parse imports
    try:
        tree = ast.parse(content)
    except Exception as e:
        print(f"Error parsing Python code: {e}")
        return False
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name:
                    imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split('.')[0])
    
    # Expected stdlib modules
    expected_stdlib = {
        'argparse', 'os', 'sys', 'datetime', 'random', 'logging', 
        'tempfile', 'json', 'time', 'subprocess', 'shutil', 'pathlib',
        're', 'typing', 'tkinter', 'traceback', 'ast'
    }
    
    # Check for unexpected imports
    actual_imports = {imp for imp in imports if imp}
    unexpected = actual_imports - expected_stdlib
    
    if unexpected:
        print(f"ERROR: Unexpected imports found: {sorted(unexpected)}")
        return False
    
    print(f"SUCCESS: All imports are standard library: {sorted(actual_imports)}")
    return True

if __name__ == "__main__":
    success = verify_stdlib_imports()
    print("✅ PASS" if success else "❌ FAIL")
    sys.exit(0 if success else 1)