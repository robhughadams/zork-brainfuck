#!/usr/bin/env python3
"""pytest tests for BF transpiler"""
import subprocess
import sys
import os
import tempfile
import pytest

# Use the venv python
PYTHON = '/home/userland/code/zork-bf/venv/bin/python'
TRANSPILE = '/home/userland/code/zork-bf/transpile.py'

def run_bf(bf_code):
    """Run BF code and return stdout"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run(['beef', f.name], capture_output=True, text=True)
        os.unlink(f.name)
        return result.stdout

def transpile(source):
    """Run transpiler and return BF code"""
    result = subprocess.run([PYTHON, TRANSPILE], input=source, 
                           capture_output=True, text=True)
    return result.stdout

def test_print_hello():
    """Test: print('Hello') -> 'Hello'"""
    bf = transpile('print("Hello")')
    output = run_bf(bf)
    assert output == "Hello"

def test_print_empty():
    """Test: print('') produces no output"""
    bf = transpile('print("")')
    output = run_bf(bf)
    assert output == ""

def test_print_single_char():
    """Test: print('A') -> 'A'"""
    bf = transpile('print("A")')
    output = run_bf(bf)
    assert output == "A"

def test_print_world():
    """Test: print('World') -> 'World'"""
    bf = transpile('print("World")')
    output = run_bf(bf)
    assert output == "World"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])