#!/usr/bin/env python3
"""
Dependency Verification Script for ABIDES Configuration Generator v1.0.0
Verifies that the application uses only Python standard library modules.
"""

import ast
import sys
import os

def verify_dependencies():
    """Verify that configgen.py uses only standard library imports."""
    
    print("Verifying application uses only Python standard library...")
    
    # Ensure UTF-8 encoding
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    # Read the main file
    try:
        with open('configgen.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError as e:
        print(f"Unicode decoding failed: {e}")
        try:
            with open('configgen.py', 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e2:
            print(f"Failed to read file: {e2}")
            sys.exit(1)
    except FileNotFoundError:
        print("ERROR: configgen.py not found")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        sys.exit(1)
    
    print(f"Successfully read {len(content)} characters from configgen.py")
    
    # Parse AST to find imports
    try:
        tree = ast.parse(content)
    except Exception as e:
        print(f"ERROR: Failed to parse Python AST: {e}")
        sys.exit(1)
    
    imports = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name:
                    imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split('.')[0])
    
    # Expected standard library modules
    stdlib_modules = {
        'argparse', 'os', 'sys', 'datetime', 'random', 'logging', 
        'tempfile', 'json', 'time', 'subprocess', 'shutil', 'pathlib',
        're', 'typing', 'tkinter', 'traceback', 'ast'
    }
    
    # Check for external dependencies
    imports = {imp for imp in imports if imp}  # Remove None values
    external_imports = imports - stdlib_modules
    
    if external_imports:
        print(f"ERROR: External dependencies found: {sorted(external_imports)}")
        print("Expected only Python standard library modules.")
        return False
    else:
        print(f"SUCCESS: Zero external dependencies confirmed.")
        print(f"Standard library imports: {sorted(imports)}")
        return True

if __name__ == "__main__":
    if verify_dependencies():
        print("✅ Dependency verification passed")
        sys.exit(0)
    else:
        print("❌ Dependency verification failed")
        sys.exit(1)