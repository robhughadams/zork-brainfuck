#!/usr/bin/env python3
"""Test game functionality"""
import subprocess
from conftest import ROOT, PYTHON, TRANSPILE, run_bf

GAME = str(ROOT / 'game/game.py')

def transpile_file(filename):
    with open(filename) as f:
        source = f.read()
    result = subprocess.run([PYTHON, TRANSPILE], input=source,
                           capture_output=True, text=True)
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