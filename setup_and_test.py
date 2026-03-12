#!/usr/bin/env python3
"""
Helper script to ensure dependencies are installed and then run the page loading test.
This resolves environment and dependency issues automatically.
"""

import subprocess
import sys
import os

def main():
    project_path = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(project_path, 'requirements.txt')
    test_script = os.path.join(project_path, 'test_pages.py')
    
    print("=" * 80)
    print("MBA Application - Page Loading Test Suite")
    print("=" * 80)
    print()
    
    # Step 1: Install dependencies
    print("[1/2] Installing dependencies from requirements.txt...")
    print(f"      Using Python: {sys.executable}")
    print()
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-q', '-r', requirements_file
        ])
        print("✓ Dependencies installed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}\n")
        sys.exit(1)
    
    # Step 2: Run the test
    print("[2/2] Running page loading tests...\n")
    print()
    
    try:
        result = subprocess.call([sys.executable, test_script])
        sys.exit(result)
    except Exception as e:
        print(f"✗ Failed to run tests: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
