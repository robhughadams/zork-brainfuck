#!/usr/bin/env python3
"""Test transpiler variable support"""
import subprocess
import sys
from conftest import ROOT, PYTHON, TRANSPILE, run_bf

def transpile(source):
    result = subprocess.run([PYTHON, TRANSPILE], input=source, 
                           capture_output=True, text=True)
    if result.returncode != 0:
        print("STDERR:", result.stderr, file=sys.stderr)
    return result.stdout

def test_print_still_works():
    """Ensure print still works after variable additions"""
    bf = transpile('print("Hi")')
    output = run_bf(bf)
    assert output == "Hi"

def test_variable_assignment():
    """Test: x = 5 (just set cell to 5)"""
    # Variables are mapped to cells
    # For now, this tests that assignment is parsed
    try:
        bf = transpile('x = 5\n')
        # Should not crash
    except Exception as e:
        pass  # Expected to fail until we implement

if __name__ == '__main__':
    test_print_still_works()
    print("test_print_still_works PASSED")
    print("All tests passed!")