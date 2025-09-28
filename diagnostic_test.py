#!/usr/bin/env python3
"""
Diagnostic script for ABIDES Configuration Generator CI debugging.
Tests basic functionality and reports environment details.
"""

import sys
import os
import platform
import subprocess
import traceback

def diagnostic_test():
    """Run comprehensive diagnostic tests."""
    
    print("=" * 60)
    print("ABIDES Configuration Generator - Diagnostic Test")
    print("=" * 60)
    
    # Environment info
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Encoding: {sys.getdefaultencoding()}")
    print(f"Locale: {os.environ.get('LANG', 'Not set')}")
    print(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'Not set')}")
    print(f"Working Directory: {os.getcwd()}")
    print("")
    
    # File checks
    print("File System Checks:")
    files_to_check = ['configgen.py', 'verify_deps.py']
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename}: {size} bytes")
        else:
            print(f"❌ {filename}: NOT FOUND")
    print("")
    
    # Basic Python execution
    print("Python Execution Tests:")
    test_commands = [
        ['python', '--version'],
        ['python', '-c', 'print("Hello World")'],
        ['python', '-c', 'import sys; print(f"Python executable: {sys.executable}")'],
    ]
    
    for cmd in test_commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {' '.join(cmd)}: {result.stdout.strip()}")
            else:
                print(f"❌ {' '.join(cmd)}: ERROR {result.returncode}")
                print(f"   STDERR: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {' '.join(cmd)}: EXCEPTION {e}")
    print("")
    
    # configgen.py tests
    print("ABIDES Configuration Generator Tests:")
    configgen_tests = [
        ['python', 'configgen.py', '--version'],
        ['python', 'configgen.py', '--help'],
        ['python', 'configgen.py', '--list-templates'],
    ]
    
    for cmd in configgen_tests:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                output_preview = result.stdout.strip()[:100] + "..." if len(result.stdout.strip()) > 100 else result.stdout.strip()
                print(f"✅ {' '.join(cmd[1:])}: {output_preview}")
            else:
                print(f"❌ {' '.join(cmd[1:])}: ERROR {result.returncode}")
                print(f"   STDERR: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {' '.join(cmd[1:])}: EXCEPTION {e}")
            traceback.print_exc()
    print("")
    
    # Template generation test
    print("Template Generation Test:")
    try:
        cmd = ['python', 'configgen.py', '--template', 'minimal', '-f', 'diagnostic_test']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            if os.path.exists('diagnostic_test.py'):
                size = os.path.getsize('diagnostic_test.py')
                print(f"✅ Template generation: Created diagnostic_test.py ({size} bytes)")
                os.remove('diagnostic_test.py')  # Clean up
            else:
                print("❌ Template generation: No output file created")
        else:
            print(f"❌ Template generation: ERROR {result.returncode}")
            print(f"   STDERR: {result.stderr.strip()}")
    except Exception as e:
        print(f"❌ Template generation: EXCEPTION {e}")
        traceback.print_exc()
    
    print("")
    print("=" * 60)
    print("Diagnostic test completed")
    print("=" * 60)

if __name__ == "__main__":
    diagnostic_test()