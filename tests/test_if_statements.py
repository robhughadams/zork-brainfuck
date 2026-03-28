#!/usr/bin/env python3
"""Tests for if/elif/else statements - SKIPPED until if is implemented"""
import subprocess
import sys
import os
import tempfile
import pytest
import pathlib
from conftest import ROOT, PYTHON, TRANSPILE

BF_INTERP = 'beef'
PREPROCESS = str(ROOT / 'src/preprocess.py')

def run_bf(bf_code, input_data='', timeout=5):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run([BF_INTERP, f.name], 
                               input=input_data,
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

@pytest.mark.skip(reason="if statements not implemented in BF")
def test_if_true():
    """Test: if x == 1: runs body when condition is true"""
    source = 'x = 1\nif x == 1:\n    print("A")'
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "A", f"Expected 'A', got '{output}'"

@pytest.mark.skip(reason="if statements not implemented in BF")
def test_if_false():
    """Test: if x == 1: runs nothing when condition is false"""
    source = 'x = 2\nif x == 1:\n    print("A")'
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "", f"Expected '', got '{output}'"

@pytest.mark.skip(reason="if statements not implemented in BF") 
def test_if_else_true():
    """Test: if/else - true branch"""
    source = '''x = 1
if x == 1:
    print("T")
else:
    print("F")
'''
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "T", f"Expected 'T', got '{output}'"

@pytest.mark.skip(reason="if statements not implemented in BF")
def test_if_else_false():
    """Test: if/else - false branch"""
    source = '''x = 0
if x == 1:
    print("T")
else:
    print("F")
'''
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "F", f"Expected 'F', got '{output}'"

@pytest.mark.skip(reason="if statements not implemented in BF")
def test_if_elif_else():
    """Test: if/elif/else"""
    source = '''x = 2
if x == 1:
    print("A")
elif x == 2:
    print("B")
else:
    print("C")
'''
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "B", f"Expected 'B', got '{output}'"

@pytest.mark.skip(reason="if statements not implemented in BF")
def test_if_with_input():
    """Test: if with input variable"""
    source = '''x = input()
if x == 65:
    print("A")
'''
    bf = transpile(source)
    output, rc = run_bf(bf, "A")
    assert output == "A", f"Expected 'A', got '{output}'"

@pytest.mark.skip(reason="if statements not implemented in BF")
def test_nested_if():
    """Test: nested if statements"""
    source = '''x = 1
y = 2
if x == 1:
    if y == 2:
        print("OK")
'''
    bf = transpile(source)
    output, rc = run_bf(bf)
    assert output == "OK", f"Expected 'OK', got '{output}'"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
