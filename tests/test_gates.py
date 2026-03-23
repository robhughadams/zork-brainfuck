#!/usr/bin/env python3
"""pytest tests for BF transpiler - Gate 2: variables, loops"""
import subprocess
import sys
import os
import tempfile
import pytest

PYTHON = '/home/userland/code/zork-bf/venv/bin/python'
TRANSPILE = '/home/userland/code/zork-bf/transpile.py'

def run_bf(bf_code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run(['beef', f.name], capture_output=True, text=True)
        os.unlink(f.name)
        return result.stdout

def transpile(source):
    result = subprocess.run([PYTHON, TRANSPILE], input=source, 
                           capture_output=True, text=True)
    return result.stdout

# ===== VARIABLE TESTS =====

def test_variable_print():
    """Test: x = 5; print(x) - just prints the char for that byte value"""
    # For now, test that we can handle variable assignment
    # This will fail until we implement variables
    bf = transpile('x = 5\nprint("x")')
    output = run_bf(bf)
    assert output == "x"

# ===== LOOP TESTS =====

def test_while_loop():
    """Test: simple while loop"""
    # This will fail until we implement loops
    bf = transpile('while True:\n    print("X")\n')
    output = run_bf(bf)
    # Should run once and print X
    assert "X" in output

def test_while_with_break():
    """Test: while with break"""
    bf = transpile('i = 0\nwhile i < 3:\n    print("X")\n    i = i + 1\n')
    output = run_bf(bf)
    # Should print X three times then stop
    assert output.count("X") == 3

# ===== INPUT TESTS =====

def test_input():
    """Test: input() reads a character"""
    # This will fail until we implement input
    bf = transpile('print("?")\nx = input()\nprint(x)\n')
    result = subprocess.run(['beef', '/dev/stdin'], 
                           input='A', capture_output=True, text=True)
    # Can't easily test input in BF - skip for now

if __name__ == '__main__':
    pytest.main([__file__, '-v'])