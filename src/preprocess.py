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


def eval_expr(expr, vars_dict):
    """Evaluate a simple expression for string concatenation."""
    expr = expr.strip()
    
    # Handle string literal concatenation: "a" + "b"
    while '+' in expr:
        # Find the first + that's not inside quotes
        parts = []
        in_string = False
        current = ""
        depth = 0
        
        for ch in expr:
            if ch == '"' and (not current or current[-1] != '\\'):
                in_string = not in_string
            if ch == '+' and not in_string and depth == 0:
                parts.append(current.strip())
                parts.append('+')
                current = ""
            else:
                if ch in '([':
                    depth += 1
                elif ch in ')]':
                    depth -= 1
                current += ch
        parts.append(current.strip())
        
        # Now evaluate the concatenation
        result = ""
        new_parts = []
        i = 0
        while i < len(parts):
            if parts[i] == '+':
                # Concatenate previous and next
                if len(new_parts) >= 2:
                    left = new_parts.pop()
                    right = parts[i + 1]
                    new_parts.append(left + right)
                    i += 2
                else:
                    new_parts.append(parts[i])
                    i += 1
            else:
                new_parts.append(parts[i])
                i += 1
        
        if len(new_parts) == 1 and isinstance(new_parts[0], str):
            return new_parts[0]
        expr = '+'.join(new_parts)
    
    return expr


def preprocess_source(source, max_passes=10):
    """Convert for loops to while loops. Run multiple passes to handle nesting."""
    # Normalize tabs to spaces FIRST (before any processing)
    source = source.replace('\t', '    ')
    
    for pass_num in range(max_passes):
        lines = source.split('\n')
        result_lines = []
        modified = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Handle string concatenation: s = "a" + "b" or print("a" + "b")
            # Try to evaluate string concatenations at compile time
            concat_match = re.match(r'^(\s*)(\w+)\s*=\s*"([^"]*)"\s*\+\s*"([^"]*)"(.*)$', line)
            if concat_match:
                indent = concat_match.group(1)
                var_name = concat_match.group(2)
                left = concat_match.group(3)
                right = concat_match.group(4)
                rest = concat_match.group(5)
                combined = left + right
                result_lines.append(f'{indent}{var_name} = "{combined}"{rest}')
                modified = True
                i += 1
                continue
            
            # Handle string concatenation: s = "a" + "b" or s = "a" + "b" + "c"
            concat_any_match = re.match(r'^(\s*)(\w+)\s*=\s*(.+)$', line)
            if concat_any_match:
                indent = concat_any_match.group(1)
                var_name = concat_any_match.group(2)
                expr = concat_any_match.group(3)
                
                # Try to evaluate string concatenations
                if ' + ' in expr and '"' in expr:
                    try:
                        result = eval(expr)
                        if isinstance(result, str) and '"' in result:
                            result_lines.append(f'{indent}{var_name} = "{result}"')
                            modified = True
                            i += 1
                            continue
                    except:
                        pass
                
                # Try to evaluate arithmetic expressions: x = 1 + 2 -> x = 3
                # Only evaluate if it contains only numbers and operators (no variables)
                if '+' in expr or '-' in expr or '*' in expr or '/' in expr:
                    # Check if expr has any variable names (word characters)
                    import re as re2
                    if re2.search(r'[a-zA-Z_]', expr):
                        pass  # Has variables, don't evaluate
                    else:
                        try:
                            result = eval(expr)
                            # Handle both int and float (for division)
                            if isinstance(result, (int, float)) and result == int(result):
                                result_lines.append(f'{indent}{var_name} = {int(result)}')
                                modified = True
                                i += 1
                                continue
                        except:
                            pass
            
            # Handle print("a" + "b" + "c")
            print_concat_any_match = re.match(r'^(\s*)print\((.+)\)(.*)$', line)
            if print_concat_any_match:
                indent = print_concat_any_match.group(1)
                expr = print_concat_any_match.group(2)
                rest = print_concat_any_match.group(3)
                
                if ' + ' in expr and '"' in expr:
                    try:
                        result = eval(expr)
                        if isinstance(result, str):
                            result_lines.append(f'{indent}print("{result}"){rest}')
                            modified = True
                            i += 1
                            continue
                    except:
                        pass
                
                # Handle print("literal" + var) or print(var + "literal")
                # Convert to two prints: print("literal"); print(var)
                concat_match = re.match(r'^"([^"]+)"\s*\+\s*(\w+)$', expr)
                if concat_match:
                    literal_part = concat_match.group(1)
                    var_part = concat_match.group(2)
                    result_lines.append(f'{indent}print("{literal_part}"){rest}')
                    result_lines.append(f'{indent}print({var_part}){rest}')
                    modified = True
                    i += 1
                    continue
                
                concat_match = re.match(r'^(\w+)\s*\+\s*"([^"]+)"$', expr)
                if concat_match:
                    var_part = concat_match.group(1)
                    literal_part = concat_match.group(2)
                    result_lines.append(f'{indent}print({var_part}){rest}')
                    result_lines.append(f'{indent}print("{literal_part}"){rest}')
                    modified = True
                    i += 1
                    continue
            
            # Skip already processed conditional lines (markers from previous passes)
            if '# IF_COND_START:' in line or '# ELIF_COND_START:' in line or '# ELSE_START' in line:
                result_lines.append(line)
                i += 1
                # Skip until we hit the END marker
                while i < len(lines):
                    line = lines[i]
                    result_lines.append(line)
                    if '# IF_COND_END' in line or '# ELIF_COND_END' in line or '# ELSE_END' in line:
                        break
                    i += 1
                i += 1
                continue
            
            # Skip lines that look like lowered conditionals (contain _cond_ and if)
            if '_cond_' in line and 'if' in line:
                result_lines.append(line)
                i += 1
                continue
            
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
            
            # Match: while True: -> while running:
            match = re.match(r'(\s*)while\s+True\s*:', line)
            if match:
                modified = True
                indent = match.group(1)
                # Detect indent character (space or tab)
                indent_str = indent if indent else ''
                body_indent_str = indent_str + '    '  # 4 spaces for detection
                
                result_lines.append(f'{indent}running = 1')
                result_lines.append(f'{indent}while running > 0:')
                
                # Collect body - handle both tabs and spaces
                i += 1
                body_lines = []
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        body_lines.append(body_line)
                        i += 1
                        continue
                    # Check if we've dedented past the while body
                    line_indent = len(body_line) - len(body_line.lstrip())
                    indent_len = len(indent)  # body should be more indented than while line
                    if line_indent <= indent_len:
                        break
                    body_lines.append(body_line)
                    i += 1
                
                for body_line in body_lines:
                    result_lines.append(body_line)
                
                # Add: running = 0 at end to exit loop
                if body_lines:
                    body_indent = len(body_lines[0]) - len(body_lines[0].lstrip())
                    result_lines.append(' ' * body_indent + 'running = 0')
                continue
            
            # Match: if s == "literal": - compile-time string equality
            match = re.match(r'(\s*)if\s+(\w+)\s*==\s*"([^"]+)":', line)
            if match:
                modified = True
                indent = match.group(1)
                indent_len = len(indent)
                var_name = match.group(2)
                literal = match.group(3)
                
                # Look up the variable's value in previous source lines
                var_value = None
                for j in range(i):
                    prev_line = lines[j].strip()
                    assign_match = re.match(r'(\w+)\s*=\s*"([^"]*)"', prev_line)
                    if assign_match and assign_match.group(1) == var_name:
                        var_value = assign_match.group(2)
                        break
                
                if var_value == literal:
                    # Exact match - keep body
                    result_lines.append(f'{indent}# if s == "literal": (match)')
                    i += 1
                    while i < len(lines):
                        body_line = lines[i]
                        if not body_line.strip():
                            result_lines.append(body_line)
                            i += 1
                            continue
                        line_indent = len(body_line) - len(body_line.lstrip())
                        if line_indent <= indent_len:
                            i -= 1
                            break
                        result_lines.append(body_line)
                        i += 1
                else:
                    # No match - skip body
                    result_lines.append(f'{indent}# if s == "literal": (no match)')
                    i += 1
                    while i < len(lines):
                        body_line = lines[i]
                        if not body_line.strip():
                            i += 1
                            continue
                        line_indent = len(body_line) - len(body_line.lstrip())
                        if line_indent <= indent_len:
                            break
                        i += 1
                    # Don't decrement i - we've consumed the body lines
                continue
            
            # Match: if x == n: -> simple: preserve body but use simple condition
            # For now, just add a comment and preserve body (dedented to match if level)
            match = re.match(r'(\s*)if\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                modified = True
                indent = match.group(1)
                if_indent = len(indent)
                
                # Add comment about the condition
                result_lines.append(f'{indent}# if x == n: (simplified)')
                
                # Add body directly - dedent to match if level
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        result_lines.append(body_line)
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if line_indent <= if_indent:
                        i -= 1
                        break
                    # Dedent body to match the if statement's level
                    excess_indent = line_indent - if_indent
                    dedented = ' ' * if_indent + body_line[line_indent:]
                    result_lines.append(dedented)
                    i += 1
                continue
            
            # Match: elif x == n: - check _cond from previous
            match = re.match(r'(\s*)elif\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                modified = True
                indent = match.group(1)
                var_name = match.group(2)
                val = match.group(3)
                
                temp_name = f'_c_{var_name}'
                
                # Check if previous conditions failed (_c_prev == 0 means failed)
                # For now, just add this condition similarly to if
                result_lines.append(f'{indent}{temp_name} = {val}')
                result_lines.append(f'{indent}{temp_name} = {temp_name} - {var_name}')
                result_lines.append(f'{indent}while {temp_name} > 0:')
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        result_lines.append(body_line)
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if line_indent <= len(indent):
                        i -= 1
                        break
                    result_lines.append(body_line)
                    i += 1
                
                result_lines.append(indent + '    ' + f'{temp_name} = {temp_name} - 1')
                i += 1
                continue

            # Match: elif with method call like s.lower() == "literal":
            # Skip these - can't implement string comparison in BF
            match = re.match(r'(\s*)elif\s+(\w+)\.(\w+)\(\)\s*==\s*\(?["\']([^"\']+)["\']\)?:', line)
            if match:
                modified = True
                # Skip until we hit a line that's NOT indented more than the elif
                base_indent = len(match.group(1))
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    curr_indent = len(body_line) - len(body_line.lstrip())
                    if curr_indent <= base_indent:
                        i -= 1
                        break
                    i += 1
                # IMPORTANT: Skip the current body line by incrementing i
                # We don't want to fall through and add this line to result
                i += 1
                continue
            
            # Match: if with method call like s.lower() == "literal":
            # Skip the entire if/elif/else chain - can't do string comparison in BF
            match = re.match(r'(\s*)if\s+(\w+)\.(\w+)\(\)\s*==\s*\(?["\']([^"\']+)["\']\)?:', line)
            if match:
                modified = True
                # Skip until we hit a line that's NOT indented more than the if
                base_indent = len(match.group(1))
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    curr_indent = len(body_line) - len(body_line.lstrip())
                    if curr_indent <= base_indent:
                        i -= 1
                        break
                    i += 1
                # IMPORTANT: Skip the current body line by incrementing i
                # We don't want to fall through and add this line to result
                i += 1
                continue
            
            # Match: else: - add else body (original behavior)
            match = re.match(r'(\s*)else:', line)
            if match:
                modified = True
                indent = match.group(1)
                # Add else body
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        result_lines.append(body_line)
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if line_indent <= len(indent):
                        i -= 1
                        break
                    result_lines.append(body_line)
                    i += 1
                continue
            
            # Match: while x == n: -> convert to while with flag
            match = re.match(r'(\s*)while\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                modified = True
                indent = match.group(1)
                var_name = match.group(2)
                val = match.group(3)
                
                temp_name = f'_c_{var_name}'
                
                result_lines.append(f'{indent}_run = 1')
                result_lines.append(f'{indent}while _run > 0:')
                result_lines.append(f'{indent}    {temp_name} = {val}')
                result_lines.append(f'{indent}    {temp_name} = {temp_name} - {var_name}')
                result_lines.append(f'{indent}    if {temp_name} > 0:')
                result_lines.append(f'{indent}        _run = 0')
                
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        result_lines.append(body_line)
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if line_indent <= len(indent):
                        i -= 1
                        break
                    result_lines.append(body_line)
                    i += 1
                continue
            
            # Handle exit() -> running = 0
            if 'exit()' in line:
                modified = True
                result_lines.append(line.replace('exit()', 'running = 0'))
                i += 1
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
        print("Usage: preprocess.py <input.py> [--verify] [-o <output.py>]")
        print("  --verify: Also run py_compile to verify valid Python")
        print("  -o: Specify output file (default: input.pre.py)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    verify = '--verify' in sys.argv
    
    # Check for -o option
    output_path = None
    if '-o' in sys.argv:
        idx = sys.argv.index('-o')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Pre-process
    output_file = preprocess_file(input_file, output_path)
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
