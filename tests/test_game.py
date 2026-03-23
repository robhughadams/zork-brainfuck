#!/usr/bin/env python3
"""Test game functionality"""
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

def test_game_generates_valid_bf():
    """Test: game.py generates valid BF"""
    # This tests that our game generator creates working code
    # We'll test this via the generator directly for now
    pass

def test_print_multiline():
    """Test: multiple print statements"""
    pass

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])