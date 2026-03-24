#!/usr/bin/env python3
"""
Pre-processor: Converts for loops to while loops.

Input:  for i in range(3):
            print("X")

Output: i = 3
        while i > 0:
            print("X")
            i = i - 1

Build pipeline:
    game.py → preprocess.py → game.pre.py → [py_compile] → transpile.py → game.bf
"""

import re
import sys
import os
import py_compile
import tempfile


def preprocess_source(source, max_passes=5):
    """Convert for loops to while loops. Run multiple passes to handle nesting."""
    for pass_num in range(max_passes):
        lines = source.split('\n')
        result_lines = []
        modified = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Match: for i in range(3):
            match = re.match(r'(\s*)for (\w+) in range\((\d+)\):', line)
            if match:
                modified = True
                indent = match.group(1)
                var_name = match.group(2)
                count = int(match.group(3))
                
                # Add: i = n
                result_lines.append(f'{indent}{var_name} = {count}')
                
                # Add: while i > 0:
                result_lines.append(f'{indent}while {var_name} > 0:')
                
                # Collect body lines
                i += 1
                body_lines = []
                while i < len(lines):
                    body_line = lines[i]
                    
                    # Check if we've exited the for loop (dedent or empty)
                    if body_line.strip() and not body_line.startswith(indent + '    '):
                        break
                    
                    if body_line.strip():
                        body_lines.append(body_line)
                    i += 1
                
                # Add body (already has proper indentation from source)
                for body_line in body_lines:
                    result_lines.append(body_line)
                
                # Add: i = i - 1 (aligned with body indentation)
                # Body is at indent + 4 spaces, so dedent by 4 for the decrement
                body_indent = len(body_lines[0]) - len(body_lines[0].lstrip()) if body_lines else len(indent) + 4
                result_lines.append(' ' * body_indent + f'{var_name} = {var_name} - 1')
                
                # Continue processing (don't increment i again - already at next line)
                continue
            
            result_lines.append(line)
            i += 1
        
        source = '\n'.join(result_lines)
        
        # If no modifications in this pass, we're done
        if not modified:
            break
    
    return source


def preprocess_file(input_path, output_path=None):
    """Pre-process a file and optionally write output."""
    if output_path is None:
        # Generate .pre.py filename
        if input_path.endswith('.py'):
            output_path = input_path[:-3] + '.pre.py'
        else:
            output_path = input_path + '.pre'
    
    with open(input_path, 'r') as f:
        source = f.read()
    
    preprocessed = preprocess_source(source)
    
    with open(output_path, 'w') as f:
        f.write(preprocessed)
    
    return output_path


def verify_python(filepath):
    """Verify the pre-processed file is valid Python."""
    try:
        py_compile.compile(filepath, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print(f"ERROR: Pre-processed file is not valid Python:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: preprocess.py <input.py> [--verify]")
        print("  --verify: Also run py_compile to verify valid Python")
        sys.exit(1)
    
    input_file = sys.argv[1]
    verify = '--verify' in sys.argv
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Pre-process
    output_file = preprocess_file(input_file)
    print(f"Pre-processed: {input_file} -> {output_file}")
    
    # Verify if requested
    if verify:
        if verify_python(output_file):
            print(f"Verified: {output_file} is valid Python")
        else:
            print(f"FAILED: {output_file} is not valid Python", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
