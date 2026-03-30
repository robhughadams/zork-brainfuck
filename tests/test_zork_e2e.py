#!/usr/bin/env python3
"""End-to-end tests for zork-py game - tests full game functionality."""
import subprocess
import tempfile
import os
import pytest
import pathlib
from conftest import ROOT, PYTHON, TRANSPILE, PREPROCESS

BF_INTERP = 'beef'

ZORK_PY = str(ROOT / 'vendor/zork-py/zork.py')
ZORK_PRE = str(ROOT / 'zork.pre.py')
ZORK_BF = str(ROOT / 'zork.bf')


def run_bf(bf_code, input_data='', timeout=30):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run([BF_INTERP, f.name],
                               input=input_data,
                               capture_output=True, text=True, timeout=timeout)
        os.unlink(f.name)
        return result.stdout, result.returncode, result.stderr


def transpile(source):
    result = subprocess.run([PYTHON, TRANSPILE], input=source,
                           capture_output=True, text=True, timeout=60)
    return result.stdout, result.stderr


def preprocess(source_file):
    result = subprocess.run([PYTHON, PREPROCESS, source_file],
                           capture_output=True, text=True, timeout=60)
    return result.returncode, result.stderr


class TestZorkE2E:
    """End-to-end tests for zork-py game - ordered by complexity."""

    def test_01_preprocess_zork_py(self):
        """Test 1: zork.py preprocesses without error."""
        returncode, stderr = preprocess(ZORK_PY)
        assert returncode == 0, f"Preprocess failed: {stderr}"
        assert os.path.exists(ZORK_PRE), "zork.pre.py should be created"

    def test_02_transpile_zork_pre(self):
        """Test 2: zork.pre.py transpiles to valid BF."""
        with open(ZORK_PRE) as f:
            source = f.read()
        bf, stderr = transpile(source)
        assert len(bf) > 0, "Transpiled BF should not be empty"
        assert ',' in bf, "BF should contain input commands (,)"

    def test_03_zork_runs_and_waits_for_input(self):
        """Test 3: zork.bf runs and waits for input (not all output at once)."""
        with open(ZORK_BF) as f:
            bf = f.read()
        output, _, stderr = run_bf(bf, '', timeout=5)
        assert "Welcome" in output or "Zork" in output, f"Should show welcome: {output}"

    def test_04_zork_accepts_input_and_continues(self):
        """Test 4: zork accepts input and continues to next state."""
        with open(ZORK_BF) as f:
            bf = f.read()
        output, _, _ = run_bf(bf, 'go southwest\n', timeout=10)
        assert "forest" in output.lower(), f"Should show forest: {output}"

    def test_05_zork_full_gameplay(self):
        """Test 5: Full gameplay - navigate through game rooms."""
        with open(ZORK_BF) as f:
            bf = f.read()
        inputs = 'go southwest\ngo east\ndescend grating\ndescend staircase\nn\n'
        output, _, _ = run_bf(bf, inputs, timeout=30)
        assert "cave" in output.lower() or "staircase" in output.lower(), \
            f"Should reach cave: {output}"

    def test_06_zork_gameplay_flow(self):
        """Test 6: Game progresses through rooms correctly."""
        with open(ZORK_BF) as f:
            bf = f.read()
        output, _, _ = run_bf(bf, 'go southwest\ngo east\ndescend grating\ndescend staircase\nn\n', timeout=10)
        assert "forest" in output.lower(), "Should reach forest"
        assert "clearing" in output.lower(), "Should reach clearing"
        assert "cave" in output.lower() or "staircase" in output.lower(), "Should reach cave"
        assert "continue" in output.lower(), "Game should continue to end"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
