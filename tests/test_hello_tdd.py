#!/usr/bin/env python3
"""Test: Generate BF to print 'Hello'"""
import subprocess
import sys

# Run transpiler
result = subprocess.run([sys.executable, 'transpile.py', 'tests/hello_source.py'], 
                       capture_output=True, text=True, cwd='/home/userland/code/zork-bf')

# Check output
with open('/home/userland/code/zork-bf/tests/hello_source.bf', 'r') as f:
    bf_code = f.read()

# Run the BF
result = subprocess.run(['beef', '/home/userland/code/zork-bf/tests/hello_source.bf'], 
                       capture_output=True, text=True)

expected = "Hello"
actual = result.stdout.strip()

print(f"Expected: {expected}")
print(f"Actual: {actual}")

if expected == actual:
    print("PASS")
else:
    print("FAIL")
    sys.exit(1)