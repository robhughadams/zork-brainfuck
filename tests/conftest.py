#!/usr/bin/env python3
"""pytest configuration and shared test utilities"""
import subprocess
import sys
import os
import tempfile
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
PYTHON = str(ROOT / 'venv/bin/python')
TRANSPILE = str(ROOT / 'src/transpile.py')
BF_INTERP = 'beef'

def run_bf(bf_code, input_data='', timeout=120):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bf', delete=False) as f:
        f.write(bf_code)
        f.flush()
        result = subprocess.run([BF_INTERP, f.name], 
                               input=input_data,
                               capture_output=True, text=True, timeout=timeout)
        os.unlink(f.name)
        return result.stdout
