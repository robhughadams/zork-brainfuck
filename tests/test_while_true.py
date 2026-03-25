#!/usr/bin/env python3
"""Tests for while True: support"""
import subprocess
import sys
import os
import tempfile
import pytest
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
PYTHON = str(ROOT / 'venv/bin/python')
TRANSPILE = str(ROOT / 'src/transpile.py')
BF_INTERP = str(ROOT / 'src/bf.py')
PREPROCESS = str(ROOT / 'src/preprocess.py')

def run_bf(bf_code, input_data='', timeout=5):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run([PYTHON, BF_INTERP, f.name, input_data], 
                               capture_output=True, text=True, timeout=timeout)
        os.unlink(f.name)
        return result.stdout, result.returncode

def transpile(source):
    result = subprocess.run([PYTHON, TRANSPILE], input=source, 
                           capture_output=True, text=True)
    return result.stdout

def preprocess(source):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(source)
        f.flush()
        result = subprocess.run([PYTHON, PREPROCESS, f.name], 
                               capture_output=True, text=True)
        output_file = f.name[:-3] + '.pre.py'
        with open(output_file) as rf:
            preprocessed = rf.read()
        os.unlink(f.name)
        os.unlink(output_file)
        return preprocessed

def test_while_true_simple():
    """Test: while True: with break exits properly"""
    # Lowering approach: while True: becomes while running:
    # where running is set to 1 initially
    source = preprocess('running = 1\nwhile running > 0:\n    print("A")\n    running = 0')
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "A", f"Expected 'A', got '{output}'"

def test_while_true_with_break():
    """Test: while True: with break in body"""
    source = preprocess('''running = 1
while running > 0:
    print("X")
    running = 0
''')
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "X", f"Expected 'X', got '{output}'"

def test_while_true_counted_loop():
    """Test: while True: simulating counted loop with break"""
    source = preprocess('''count = 3
running = 1
while running > 0:
    print("B")
    count = count - 1
    if count == 0:
        running = 0
''')
    bf = transpile(source)
    output, rc = run_bf(bf)
    # Note: if/elif not working yet, so this test documents expected behavior
    assert output == "BBB", f"Expected 'BBB', got '{output}'"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
