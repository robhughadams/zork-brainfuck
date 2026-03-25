#!/usr/bin/env python3
"""Tests for preprocessor: for loops to while loops"""
import pytest
import sys
import os
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'src'))
from preprocess import preprocess_source, verify_python


def test_simple_for_loop():
    """Test: for i in range(3): -> i = 3, while i > 0, i = i - 1"""
    source = """for i in range(3):
    print(chr(65))
"""
    result = preprocess_source(source)
    assert "i = 3" in result
    assert "while i > 0:" in result
    assert "i = i - 1" in result


def test_for_loop_preserves_body():
    """Test: body content is preserved"""
    source = """for i in range(3):
    print(chr(65))
    x = x + 1
"""
    result = preprocess_source(source)
    assert "print(chr(65))" in result
    assert "x = x + 1" in result


def test_nested_for_loops():
    """Test: nested for loops are converted"""
    source = """for i in range(2):
    for j in range(2):
        print(chr(65))
"""
    result = preprocess_source(source)
    # Outer loop
    assert "i = 2" in result
    assert "while i > 0:" in result
    # Inner loop
    assert "j = 2" in result
    assert "while j > 0:" in result


def test_for_with_other_code():
    """Test: for loop alongside other code"""
    source = """print("start")
for i in range(3):
    print(chr(65))
print("end")
"""
    result = preprocess_source(source)
    assert 'print("start")' in result
    assert 'print("end")' in result
    assert "i = 3" in result


def test_multiple_for_loops():
    """Test: multiple for loops"""
    source = """for i in range(2):
    print(chr(65))
for j in range(3):
    print(chr(66))
"""
    result = preprocess_source(source)
    assert "i = 2" in result
    assert "j = 3" in result


def test_verify_python_valid():
    """Test: verify_python returns True for valid Python"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("x = 1\nprint(x)\n")
        f.flush()
        temp_path = f.name
    
    try:
        result = verify_python(temp_path)
        assert result is True
    finally:
        os.unlink(temp_path)


def test_verify_python_invalid():
    """Test: verify_python returns False for invalid Python"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("x = 1\n    invalid syntax here\n")
        f.flush()
        temp_path = f.name
    
    try:
        result = verify_python(temp_path)
        assert result is False
    finally:
        os.unlink(temp_path)


def test_preprocess_valid_python():
    """Test: preprocessed output is valid Python (via py_compile)"""
    source = """for i in range(3):
    print(chr(65))
"""
    result = preprocess_source(source)
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(result)
        f.flush()
        temp_path = f.name
    
    try:
        assert verify_python(temp_path) is True
    finally:
        os.unlink(temp_path)


def test_end_to_end_preprocess_transpile():
    """Test: full pipeline preprocess -> verify -> transpile -> run"""
    import subprocess
    import tempfile
    
    source = """for i in range(3):
    print(chr(65))
"""
    # Pre-process
    preprocessed = preprocess_source(source)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pre.py', delete=False) as f:
        f.write(preprocessed)
        f.flush()
        pre_path = f.name
    
    try:
        # Verify
        assert verify_python(pre_path) is True
        
        # Transpile
        result = subprocess.run(
            [str(ROOT / 'venv/bin/python'), str(ROOT / 'src/transpile.py')],
            input=preprocessed,
            capture_output=True,
            text=True
        )
        bf_code = result.stdout
        
        # Run BF
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
            f.write(bf_code)
            f.flush()
            bf_path = f.name
        
        result = subprocess.run(
            [str(ROOT / 'venv/bin/python'), str(ROOT / 'src/bf.py'), bf_path],
            capture_output=True,
            text=True
        )
        
        # Should print 'A' three times
        assert result.stdout == "AAA", f"Expected 'AAA', got '{result.stdout}'"
    finally:
        os.unlink(pre_path)
        if 'bf_path' in locals():
            os.unlink(bf_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
