#!/usr/bin/env python3
"""pytest tests for BF transpiler"""
import subprocess
import pytest
from conftest import ROOT, PYTHON, TRANSPILE, run_bf

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

def test_var_assign():
    """Test: x = 3 produces no output (just stores value)"""
    bf = transpile('x = 3')
    output = run_bf(bf)
    assert output == "", f"Expected '', got '{output}'"

def test_print_var():
    """Test: x = 65; print(chr(x)) -> 'A'"""
    bf = transpile('x = 65\nprint(chr(x))')
    output = run_bf(bf)
    assert output == "A", f"Expected 'A', got '{output}'"

def test_input():
    """Test: input() reads one character from stdin"""
    bf = transpile('x = input()')
    output = run_bf(bf, 'A')
    assert output == "", f"Expected '', got '{output}'"

def test_print_input():
    """Test: x = input(); print(chr(x)) -> echos input"""
    bf = transpile('x = input()\nprint(chr(x))')
    output = run_bf(bf, 'B')
    assert output == "B", f"Expected 'B', got '{output}'"

def test_while_loop():
    """Test: while x > 0: loop with decrement in body"""
    bf = transpile('x = 3\nwhile x > 0:\n    print(chr(65))\n    x = x - 1')
    output = run_bf(bf, timeout=5)
    assert output == "AAA", f"Expected 'AAA', got '{output}'"

def test_while_loop_no_body_decr():
    """TODO: while loop body must decrement var - this is BF limitation"""
    # BF [ ] loops only exit when cell is 0
    # If body doesn't decrement, loop runs forever
    pass

# TODO: Implement if statements properly in BF
# def test_if_statement():
#     """Test: if x == 1: runs body when true"""
# 
# TODO: Implement if statements properly in BF  
# def test_if_false():
#     """Test: if x == 1: runs nothing when false"""

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])