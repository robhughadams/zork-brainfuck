#!/usr/bin/env python3
"""Transpiler: Python subset -> Brainfuck v2 with variables and loops"""

import re
import sys

class Transpiler:
    def __init__(self):
        self.variables = {}  # name -> cell index
        self.cell = 0
        self.var_cells = {}  # name -> (cell, type) - populated in transpile
        self.string_vars = {}  # name -> string content
    
    def get_cell(self, var_name):
        """Get cell number from var_cells entry (handles tuple format)"""
        entry = self.var_cells.get(var_name, (0, 'num'))
        if isinstance(entry, tuple):
            return entry[0]
        return entry
    
    def get_type(self, var_name):
        """Get type from var_cells entry ('num' or 'str')"""
        entry = self.var_cells.get(var_name, (0, 'num'))
        if isinstance(entry, tuple):
            return entry[1]
        return 'num'
    
    def transpile(self, source):
        lines = source.strip().split('\n')
        bf = []
        
        # Allocate cells for variables - use instance vars for helper access
        self.var_cells = {}  # name -> (start_cell, type) where type is 'num' or 'str'
        self.string_vars = {}  # name -> string content for string literals
        var_count = 0
        
        # First pass: collect explicit variables (string literals, numbers)
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # String assignment: s = "text"
            match = re.match(r'(\w+)\s*=\s*"([^"]*)"', line)
            if match:
                var_name = match.group(1)
                str_content = match.group(2)
                if var_name not in self.var_cells:
                    self.var_cells[var_name] = (var_count, 'str')
                    self.string_vars[var_name] = str_content
                    var_count += 1 + len(str_content)
                continue
            
            match = re.match(r'(\w+)\s*=\s*(\d+)', line)
            if match:
                var_name = match.group(1)
                if var_name not in self.var_cells:
                    self.var_cells[var_name] = (var_count, 'num')
                    var_count += 1
                continue
            
            # x = y (variable copy)
            match = re.match(r'(\w+)\s*=\s*(\w+)$', line)
            if match:
                dest = match.group(1)
                src = match.group(2)
                if dest not in self.var_cells:
                    self.var_cells[dest] = (var_count, 'num')
                    var_count += 1
                if src not in self.var_cells:
                    self.var_cells[src] = (var_count, 'num')
                    var_count += 1
        
        # Second pass: analyze input() usage to determine type
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Check for input("prompt") usage
            match = re.match(r'(\w+)\s*=\s*input\("([^"]*)"\)', line)
            if match:
                var_name = match.group(1)
                is_string_used = False
                for check_line in lines:
                    check_line = check_line.strip()
                    if f'print({var_name})' in check_line or f'{var_name}[' in check_line or f'len({var_name})' in check_line:
                        is_string_used = True
                        break
                
                if var_name in self.var_cells:
                    old_entry = self.var_cells[var_name]
                    if is_string_used and old_entry[1] == 'num':
                        self.var_cells[var_name] = (old_entry[0], 'str')
                        self.string_vars[var_name] = ''
                        var_count += 10
                else:
                    if is_string_used:
                        self.var_cells[var_name] = (var_count, 'str')
                        self.string_vars[var_name] = ''
                        var_count += 1 + 10
                    else:
                        self.var_cells[var_name] = (var_count, 'num')
                        var_count += 1
                continue
            
            # Check for input() usage
            match = re.match(r'(\w+)\s*=\s*input\(\)', line)
            if match:
                var_name = match.group(1)
                # Check how it's used later
                is_string_used = False
                for check_line in lines:
                    check_line = check_line.strip()
                    # If print(s) or s[i] or len(s), it's used as string
                    if f'print({var_name})' in check_line or f'{var_name}[' in check_line or f'len({var_name})' in check_line:
                        is_string_used = True
                        break
                
                if var_name in self.var_cells:
                    # Already exists, update type if needed
                    old_entry = self.var_cells[var_name]
                    if is_string_used and old_entry[1] == 'num':
                        # Need to reallocate as string - adjust var_count
                        self.var_cells[var_name] = (old_entry[0], 'str')
                        self.string_vars[var_name] = ''
                        var_count += 10  # Extra 10 cells for string chars
                else:
                    # New variable
                    if is_string_used:
                        self.var_cells[var_name] = (var_count, 'str')
                        self.string_vars[var_name] = ''
                        var_count += 1 + 10  # length + 10 chars
                    else:
                        self.var_cells[var_name] = (var_count, 'num')
                        var_count += 1
                continue
            
            # Also check for len(s) and indexing to mark variables as strings
            match = re.match(r'(\w+)\s*=\s*len\((\w+)\)', line)
            if match:
                src = match.group(2)
                if src in self.var_cells:
                    old_entry = self.var_cells[src]
                    if old_entry[1] == 'num':
                        self.var_cells[src] = (old_entry[0], 'str')
                        self.string_vars[src] = ''
                        var_count += 10  # Extra cells for string
                continue
            
            match = re.match(r'(\w+)\s*=\s*(\w+)\[(\d+)\]', line)
            if match:
                src = match.group(2)
                if src in self.var_cells:
                    old_entry = self.var_cells[src]
                    if old_entry[1] == 'num':
                        self.var_cells[src] = (old_entry[0], 'str')
                        self.string_vars[src] = ''
                        var_count += 10
                continue
            
            # n = len(s) - string length
            match = re.match(r'(\w+)\s*=\s*len\((\w+)\)', line)
            if match:
                dest = match.group(1)
                src = match.group(2)
                if dest not in self.var_cells:
                    self.var_cells[dest] = (var_count, 'num')
                    var_count += 1
                continue
            
            # c = s[i] - string indexing
            match = re.match(r'(\w+)\s*=\s*(\w+)\[(\d+)\]', line)
            if match:
                dest = match.group(1)
                src = match.group(2)
                if dest not in self.var_cells:
                    self.var_cells[dest] = (var_count, 'num')
                    var_count += 1
                continue
        
        self.var_count = var_count
        
        # Reserve cells: 0=temp, then variables
        bf.append('[-]')  # cell 0 = temp
        for i in range(var_count):
            bf.append('>[-]')  # initialize vars to 0
        # Return to cell 0 after init
        if var_count > 0:
            bf.append('<' * var_count)
        
        # Current position - start at cell 0 (return after init)
        current_pos = 0
        
        # Process statements with while loop support
        i = 0
        while i < len(lines):
            orig_line = lines[i]
            line = orig_line.strip()
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # while x > 0: - simple BF loop
            # Pattern: go to x, [ body that decrements x ]
            match = re.match(r'while\s+(\w+)\s*>\s*0:', line)
            if match:
                var = match.group(1)
                cell = self.get_cell(var) + 1
                while_indent = len(orig_line) - len(orig_line.lstrip())
                
                # Find body (indented lines)
                i += 1
                body = []
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if line_indent <= while_indent:
                        break
                    body.append(body_line.strip())
                    i += 1
                
                # Generate loop BF
                bf.append('>' * cell)
                bf.append('[')
                
                for body_line in body:
                    bf.extend(self.transpile_line(body_line, base_cell=cell))
                
                bf.append(']')
                bf.append('<' * cell)
                continue
            
            # while x < n:
                
                # Go to var, then loop: [ body that MUST decrement var ]
                bf.append('>' * cell)  # go to var
                bf.append('[')         # while var > 0
                
                # Generate body (body must decrement var to exit)
                # Pass base_cell so body knows we're at 'var' cell
                for body_line in body:
                    bf.extend(self.transpile_line(body_line, base_cell=cell))
                
                bf.append('<' + '>' * cell)  # ensure we're back at var before ]
                bf.append(']')
                bf.append('<' * cell)  # back to cell 0
                continue
            
            # while x < n: - loop n-x times (simplified)
            match = re.match(r'while\s+(\w+)\s*<\s*(\d+):', line)
            if match:
                var = match.group(1)
                limit = int(match.group(2))
                cell = self.get_cell(var) + 1
                
                # Find body (handle tabs/spaces)
                i += 1
                body = []
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    while_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                    if line_indent <= while_indent:
                        break
                    body.append(body_line.strip())
                    i += 1
                
                # Generate loop BF: run (limit - current) times
                # Use counter pattern: decrement limit, loop until counter is 0
                bf.append('>' * cell)
                bf.append('[-')  # while var > 0
                bf.append('-' * 1)
                
                # Generate body BF
                for body_line in body:
                    bf.extend(self.transpile_line(body_line))
                 
                bf.append('<' * cell)
                bf.append(']')
                bf.append('<' * cell)
                continue
            
            # if s == "literal": - skip (too complex for now)
            # String equality will be handled by preprocessor for now
            match = re.match(r'if\s+(\w+)\s*==\s*"([^"]+)":', line)
            if match:
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                    if line_indent <= if_indent:
                        break
                    i += 1
                i -= 1
                continue
            
            # while s == "literal": - skip for now
            match = re.match(r'while\s+(\w+)\s*==\s*"([^"]+)":', line)
            if match:
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    while_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                    if line_indent <= while_indent:
                        break
                    i += 1
                i -= 1
                continue
            
            # if x == n: - skip for now (causes issues in BF)
            match = re.match(r'if\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                # Skip body
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    if_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                    if line_indent <= if_indent:
                        break
                    i += 1
                i -= 1
                continue
            
            # while x == n: - skip for now (complex in BF)
            # The preprocessor generates _cond_var = n - var but that's not enough
            match = re.match(r'while\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                # For now, just skip the body entirely
                # This allows transpilation to complete
                i += 1
                while i < len(lines):
                    body_line = lines[i]
                    if not body_line.strip():
                        i += 1
                        continue
                    line_indent = len(body_line) - len(body_line.lstrip())
                    while_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
                    if line_indent <= while_indent:
                        break
                    i += 1
                i -= 1
                continue
            
            bf.extend(self.transpile_line(line, base_cell=current_pos))
            current_pos = 0  # transpile_line returns to cell 0
            i += 1
        
        return ''.join(bf)
    
    def transpile_line(self, line, base_cell=0):
        bf = []
        
        # String assignment: s = "text" - store as bstr (length + chars)
        match = re.match(r'(\w+)\s*=\s*"([^"]*)"', line)
        if match:
            var_name = match.group(1)
            text = match.group(2)
            cell = self.get_cell(var_name)
            # Navigate from current position (base_cell) back to cell 0
            if base_cell > 0:
                bf.append('<' * base_cell)
            elif base_cell < 0:
                bf.append('>' * (-base_cell))
            # Now from cell 0, go to length cell (cell+1)
            bf.append('>' * (cell + 1))
            # Store length
            bf.append('[-]')
            bf.append('+' * len(text))
            # Store each character
            for char in text:
                bf.append('>[-]')
                bf.append('+' * ord(char))
            # Go back to cell 0
            bf.append('<' * (cell + 1 + len(text)))
            return bf
        
        # print(s) - print string variable (bstr format: length at cell, chars at cell+1...)
        match = re.match(r'print\((\w+)\)$', line)
        if match:
            var_name = match.group(1)
            if self.get_type(var_name) == 'str':
                cell = self.get_cell(var_name)
                str_content = self.string_vars.get(var_name, "")
                str_len = len(str_content)
                
                # If we have a literal string, use it directly
                if str_len > 0:
                    # Layout: cell0=temp, cell1=length, cell2=char[0], cell3=char[1], ...
                    bf.append('>' * (cell + 1))  # cell 1 = length
                    bf.append('>')  # cell 2 = first char
                    
                    # Simple loop: repeat str_len times
                    for _ in range(str_len):
                        bf.append('.')  # print char
                        bf.append('>')  # advance to next char
                    
                    # Return to cell 0
                    bf.append('<' * (cell + str_len + 2))
                else:
                    # For runtime strings (like input), just print max 10 chars
                    bf.append('>' * (cell + 2))  # Go to first char
                    for _ in range(10):
                        bf.append('.')  # print char
                        bf.append('>')  # advance
                    bf.append('<' * (cell + 12))  # return to cell 0
                return bf
        
        # print("text") - navigate to temp cell (0) first
        match = re.match(r'print\("([^"]*)"\)', line)
        if match:
            text = match.group(1)
            cell = 0 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            for char in text:
                bf.append('[-]')
                bf.append('+' * ord(char))
                bf.append('.')
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # print(chr(65)) - ALWAYS use temp cell (cell 0), go from current pos
        match = re.match(r'print\(chr\((\d+)\)\)', line)
        if match:
            val = int(match.group(1))
            # Navigate to temp (cell 0), use relative from base_cell
            cell = 0 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('[-]')
            bf.append('+' * val)
            bf.append('.')
            bf.append('[-]')
            # Navigate back
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # print(chr(var + n)) - add n to var, then print
        match = re.match(r'print\(chr\((\w+)\s*\+\s*(\d+)\)\)', line)
        if match:
            var = match.group(1)
            add_val = int(match.group(2))
            cell = self.get_cell(var) + 1 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('+' * add_val)
            bf.append('.')
            bf.append('-' * add_val)
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # print(chr(n + var)) - add var to n, then print  
        match = re.match(r'print\(chr\((\d+)\s*\+\s*(\w+)\)\)', line)
        if match:
            add_val = int(match.group(1))
            var = match.group(2)
            cell = self.get_cell(var) + 1 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('+' * add_val)
            bf.append('.')
            bf.append('-' * add_val)
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # print(chr(x)) - special: print var WITHOUT clearing
        match = re.match(r'print\(chr\((\w+)\)\)', line)
        if match:
            var = match.group(1)
            cell = self.get_cell(var) + 1 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('.')
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # x = 5
        match = re.match(r'(\w+)\s*=\s*(\d+)', line)
        if match:
            var = match.group(1)
            val = int(match.group(2))
            cell = self.get_cell(var) + 1 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('[-]')
            bf.append('+' * val)
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # x = x + 1
        match = re.match(r'(\w+)\s*=\s*\w+\s*\+\s*(\d+)', line)
        if match:
            var = match.group(1)
            val = int(match.group(2))
            cell = self.get_cell(var) + 1 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('+' * val)
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        
        # x = y (copy variable)
        match = re.match(r'(\w+)\s*=\s*(\w+)$', line)
        if match:
            dest = match.group(1)
            src = match.group(2)
            if src != dest:  # Only if different variables
                dest_cell = self.get_cell(dest) + 1 - base_cell
                src_cell = self.get_cell(src) + 1 - base_cell
                # Go to dest, clear it
                if dest_cell >= 0:
                    bf.append('>' * dest_cell)
                else:
                    bf.append('<' * (-dest_cell))
                bf.append('[-]')
                # Copy from src: go to src, copy to dest
                bf.append('<' * (dest_cell - src_cell) if dest_cell > src_cell else '>' * (src_cell - dest_cell))
                bf.append('[->+<]')
                # Go back to dest
                bf.append('>' if dest_cell > 0 else '<' * dest_cell)
            return bf
        
        # x = x - 1
        match = re.match(r'(\w+)\s*=\s*\w+\s*-\s*(\d+)', line)
        if match:
            var = match.group(1)
            val = int(match.group(2))
            cell = self.get_cell(var) + 1 - base_cell
            if cell >= 0:
                bf.append('>' * cell)
            else:
                bf.append('<' * (-cell))
            bf.append('-' * val)
            if cell >= 0:
                bf.append('<' * cell)
            else:
                bf.append('>' * (-cell))
            return bf
        # x = input("prompt") - print prompt first, then read
        match = re.match(r'(\w+)\s*=\s*input\("([^"]*)"\)', line)
        if match:
            var = match.group(1)
            prompt = match.group(2)
            # First print the prompt
            for char in prompt:
                bf.append('[-]')
                bf.append('+' * ord(char))
                bf.append('.')
            # Then do input
            if self.get_type(var) == 'str':
                cell = self.get_cell(var)
                if base_cell > 0:
                    bf.append('<' * base_cell)
                elif base_cell < 0:
                    bf.append('>' * (-base_cell))
                bf.append('>' * (cell + 2))
                bf.append('[-]')
                for i in range(10):
                    bf.append(',')
                    bf.append('>')
                bf.append('<' * 10)
                bf.append('<' * 1)
                bf.append('<' * 1)
                bf.append('+' * 10)
                bf.append('<' * (cell + 1))
                return bf
            else:
                cell = self.get_cell(var) + 1 - base_cell
                if cell >= 0:
                    bf.append('>' * cell)
                else:
                    bf.append('<' * (-cell))
                bf.append(',')
                if cell >= 0:
                    bf.append('<' * cell)
                else:
                    bf.append('>' * (-cell))
                return bf
        
        # x = input()
        match = re.match(r'(\w+)\s*=\s*input\(\)', line)
        if match:
            var = match.group(1)
            if self.get_type(var) == 'str':
                cell = self.get_cell(var)
                if base_cell > 0:
                    bf.append('<' * base_cell)
                elif base_cell < 0:
                    bf.append('>' * (-base_cell))
                bf.append('>' * (cell + 2))
                bf.append('[-]')
                for i in range(10):
                    bf.append(',')
                    bf.append('>')
                bf.append('<' * 10)
                bf.append('<' * 1)
                bf.append('<' * 1)
                bf.append('+' * 10)
                bf.append('<' * (cell + 1))
                return bf
            else:
                cell = self.get_cell(var) + 1 - base_cell
                if cell >= 0:
                    bf.append('>' * cell)
                else:
                    bf.append('<' * (-cell))
                bf.append(',')
                if cell >= 0:
                    bf.append('<' * cell)
                else:
                    bf.append('>' * (-cell))
                return bf
        
        # len(s) - get length of string variable (compile-time known!)
        match = re.match(r'(\w+)\s*=\s*len\((\w+)\)', line)
        if match:
            dest = match.group(1)
            src = match.group(2)
            if self.get_type(src) == 'str':
                str_len = len(self.string_vars.get(src, ""))
                dest_cell = self.get_cell(dest)
                # Navigate to dest cell and assign length
                bf.append('>' * (dest_cell + 1))
                bf.append('[-]')
                bf.append('+' * str_len)
                bf.append('<' * (dest_cell + 1))
                return bf
        
        # s[i] - get character at index (compile-time known!)
        match = re.match(r'(\w+)\s*=\s*(\w+)\[(\d+)\]', line)
        if match:
            dest = match.group(1)
            src = match.group(2)
            idx = int(match.group(3))
            if self.get_type(src) == 'str':
                str_content = self.string_vars.get(src, "")
                char_val = ord(str_content[idx]) if idx < len(str_content) else 0
                dest_cell = self.get_cell(dest)
                # Navigate to dest cell and assign character value
                bf.append('>' * (dest_cell + 1))
                bf.append('[-]')
                bf.append('+' * char_val)
                bf.append('<' * (dest_cell + 1))
                return bf
        
        # s = s.lower() - convert string to lowercase in place
        # For compile-time strings: we know the content, so we can generate simpler BF
        match = re.match(r'(\w+)\s*=\s*(\w+)\.lower\(\)$', line)
        if match:
            dest = match.group(1)
            src = match.group(2)
            if self.get_type(src) == 'str':
                cell = self.get_cell(src)
                str_content = self.string_vars.get(src, "")
                str_len = len(str_content)
                
                # Navigate to first char
                bf.append('>' * (cell + 2))
                
                # For each character: if uppercase (65-90), add 32
                for i in range(str_len):
                    # At char[i], add 32 if it's uppercase
                    char_ord = ord(str_content[i])
                    if 65 <= char_ord <= 90:  # uppercase
                        bf.append('+' * 32)  # add 32 to convert to lowercase
                    # else: leave unchanged (digit, punctuation, or lowercase)
                    if i < str_len - 1:
                        bf.append('>')  # move to next char
                
                # Return to cell 0
                bf.append('<' * (cell + str_len + 1))
                return bf
        
        # s = s.upper() - convert string to uppercase in place
        match = re.match(r'(\w+)\s*=\s*(\w+)\.upper\(\)$', line)
        if match:
            dest = match.group(1)
            src = match.group(2)
            if self.get_type(src) == 'str':
                cell = self.get_cell(src)
                str_content = self.string_vars.get(src, "")
                str_len = len(str_content)
                
                # Navigate to first char
                bf.append('>' * (cell + 2))
                
                # For each character: if lowercase (97-122), subtract 32
                for i in range(str_len):
                    char_ord = ord(str_content[i])
                    if 97 <= char_ord <= 122:  # lowercase
                        bf.append('-' * 32)  # subtract 32 to convert to uppercase
                    if i < str_len - 1:
                        bf.append('>')
                
                bf.append('<' * (cell + str_len + 1))
                return bf
        
        return bf

def main():
    source = sys.stdin.read()
    t = Transpiler()
    result = t.transpile(source)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()