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

    def test_03_zork_runs_and_shows_welcome(self):
        """Test 3: zork.bf runs and shows welcome message."""
        with open(ZORK_BF) as f:
            bf = f.read()
        output, _, stderr = run_bf(bf, '', timeout=10)
        assert "Welcome" in output, f"Should show welcome: {output}"
        assert "Zork" in output, f"Should mention Zork: {output}"

    def test_04_zork_shows_first_room(self):
        """Test 4: zork shows the first room description."""
        with open(ZORK_BF) as f:
            bf = f.read()
        output, _, _ = run_bf(bf, 'a\nb\nc\nd\ne\nf\n', timeout=10)
        assert "open field" in output.lower(), f"Should show open field: {output}"
        assert "mailbox" in output.lower(), f"Should show mailbox: {output}"

    def test_05_zork_full_gameplay(self):
        """Test 5: Full gameplay - all rooms appear in output."""
        with open(ZORK_BF) as f:
            bf = f.read()
        inputs = 'a\nb\nc\nd\ne\nf\n'
        output, _, _ = run_bf(bf, inputs, timeout=15)
        assert "forest" in output.lower(), f"Should reach forest: {output}"
        assert "cave" in output.lower() or "staircase" in output.lower(), \
            f"Should reach cave: {output}"

    def test_06_zork_gameplay_flow(self):
        """Test 6: Game progresses through all rooms in order."""
        with open(ZORK_BF) as f:
            bf = f.read()
        output, _, _ = run_bf(bf, 'a\nb\nc\nd\ne\nf\n', timeout=15)
        output_lower = output.lower()
        assert "open field" in output_lower, "Should show room 1: open field"
        assert "forest" in output_lower, "Should show room 2: forest"
        assert "clearing" in output_lower, "Should show room 3: clearing"
        assert "cave" in output_lower, "Should show room 4: cave"
        assert "mud" in output_lower, "Should show room 5: end room"
        assert "continue" in output_lower, "Should ask to continue"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
