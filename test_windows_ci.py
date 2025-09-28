#!/usr/bin/env python3
"""
Minimal Windows CI test for ABIDES Configuration Generator.
Tests core functionality without GUI components.
"""

import sys
import os
import subprocess

def test_basic_cli():
    """Test basic CLI functionality."""
    print("=== ABIDES Windows CI Test ===")
    
    # Test 1: Version check
    try:
        result = subprocess.run([sys.executable, 'configgen.py', '--version'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Version check: PASS")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print("❌ Version check: FAIL")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Version check: EXCEPTION {e}")
        return False
    
    # Test 2: Template generation
    try:
        result = subprocess.run([sys.executable, 'configgen.py', '--template', 'minimal', 
                               '-f', 'test_ci_windows'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            if os.path.exists('test_ci_windows.py'):
                print("✅ Template generation: PASS")
                # Clean up
                os.remove('test_ci_windows.py')
            else:
                print("❌ Template generation: No output file")
                return False
        else:
            print("❌ Template generation: FAIL")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Template generation: EXCEPTION {e}")
        return False
    
    print("✅ All Windows CI tests passed!")
    return True

if __name__ == "__main__":
    success = test_basic_cli()
    sys.exit(0 if success else 1)