#!/usr/bin/env python3
"""Test game functionality"""
import subprocess
import sys
import os
import tempfile
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
PYTHON = str(ROOT / 'venv/bin/python')
TRANSPILE = str(ROOT / 'src/transpile.py')
BF_INTERP = str(ROOT / 'src/bf.py')
GAME = str(ROOT / 'game/game.py')

def transpile_file(filename):
    with open(filename) as f:
        source = f.read()
    result = subprocess.run([PYTHON, TRANSPILE], input=source,
                           capture_output=True, text=True)
    return result.stdout

def run_bf(bf_code, input_data=''):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run([PYTHON, BF_INTERP, f.name, input_data], 
                               capture_output=True, text=True, timeout=60)
        os.unlink(f.name)
        return result.stdout

def test_game_generates_valid_bf():
    """Test: game.py generates valid BF that runs"""
    bf = transpile_file(GAME)
    output = run_bf(bf, '\n\n\n\n\n\n')
    assert "ZORK" in output, f"Expected ZORK in output"
    assert "YOU WIN" in output, f"Expected YOU WIN in output"

def test_game_has_welcome():
    """Test: game shows welcome message"""
    bf = transpile_file(GAME)
    output = run_bf(bf, '\n')
    assert "Welcome" in output or "ZORK" in output

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])