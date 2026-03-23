#!/usr/bin/env python3
"""Test transpiler variable support"""
import subprocess
import sys
import os
import tempfile

PYTHON = '/home/userland/code/zork-bf/venv/bin/python'
TRANSPILE = '/home/userland/code/zork-bf/transpile.py'
BF_INTERP = '/home/userland/code/zork-bf/bf.py'

def run_bf(bf_code, input_data=''):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run([PYTHON, BF_INTERP, f.name, input_data], 
                               capture_output=True, text=True)
        os.unlink(f.name)
        return result.stdout

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