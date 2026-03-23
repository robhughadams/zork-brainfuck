#!/usr/bin/env python3
"""pytest tests for BF transpiler - using Python BF interpreter"""
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
    return result.stdout

def test_print_hello():
    """Test: print('Hello') -> 'Hello'"""
    bf = transpile('print("Hello")')
    output = run_bf(bf)
    assert output == "Hello", f"Expected 'Hello', got '{output}'"

def test_print_world():
    """Test: print('World') -> 'World'"""
    bf = transpile('print("World")')
    output = run_bf(bf)
    assert output == "World", f"Expected 'World', got '{output}'"

def test_print_empty():
    """Test: print('') produces no output"""
    bf = transpile('print("")')
    output = run_bf(bf)
    assert output == "", f"Expected '', got '{output}'"

def test_print_a():
    """Test: print('A') -> 'A'"""
    bf = transpile('print("A")')
    output = run_bf(bf)
    assert output == "A", f"Expected 'A', got '{output}'"

def test_print_zork():
    """Test: print('Zork') -> 'Zork'"""
    bf = transpile('print("Zork")')
    output = run_bf(bf)
    assert output == "Zork", f"Expected 'Zork', got '{output}'"

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])