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
        self.runtime_string_capacity = 24
        self.scratch_used = 0
    
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

    def _emit_temp_text(self, text, base_cell):
        bf = []
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

    def _emit_print_newline(self, base_cell):
        return self._emit_temp_text('\n', base_cell)

    def _move_abs(self, from_cell, to_cell):
        delta = to_cell - from_cell
        if delta > 0:
            return '>' * delta
        if delta < 0:
            return '<' * (-delta)
        return ''

    def _reserve_scratch(self, count):
        start = self.var_count + self.scratch_used + 1
        self.scratch_used += count
        return start

    def _emit_string_input(self, var_name, prompt, base_cell):
        bf = []
        start = self.get_cell(var_name) + 1
        len_cell = start
        capacity = self.runtime_string_capacity
        chars_start = start + 1
        scratch = self._reserve_scratch(4)
        active = scratch
        exec_cell = scratch + 1
        tmp = scratch + 2
        restore = scratch + 3

        bf.extend(self._emit_temp_text(prompt, base_cell))

        current = base_cell
        for cell in [len_cell] + list(range(chars_start, chars_start + capacity + 1)) + [active, exec_cell, tmp, restore]:
            bf.append(self._move_abs(current, cell))
            bf.append('[-]')
            current = cell

        # active=1 means the next unrolled read slot should execute.
        bf.append(self._move_abs(current, active))
        bf.append('+')
        current = active

        for index in range(capacity):
            char_cell = chars_start + index

            # Move active -> exec_cell so this slot executes at most once.
            bf.append(self._move_abs(current, active))
            bf.append('[')
            bf.append('-')
            bf.append(self._move_abs(active, exec_cell))
            bf.append('+')
            bf.append(self._move_abs(exec_cell, active))
            bf.append(']')
            current = active

            bf.append(self._move_abs(current, exec_cell))
            bf.append('[')
            bf.append('-')

            # Read one character and copy it into tmp+restore, while also using
            # exec_cell as a non-EOF flag for this slot.
            bf.append(self._move_abs(exec_cell, char_cell))
            bf.append(',')
            current = char_cell
            bf.append('[')
            bf.append('-')
            bf.append(self._move_abs(char_cell, tmp))
            bf.append('+')
            bf.append(self._move_abs(tmp, restore))
            bf.append('+')
            bf.append(self._move_abs(restore, exec_cell))
            bf.append('+')
            bf.append(self._move_abs(exec_cell, char_cell))
            bf.append(']')
            current = char_cell

            # exec_cell > 0 means a non-EOF character was read. Compare tmp
            # against newline; only non-newline characters are stored.
            bf.append(self._move_abs(current, exec_cell))
            bf.append('[')
            bf.append('[-]')
            bf.append(self._move_abs(exec_cell, tmp))
            current = tmp
            bf.append('-' * 10)
            bf.append('[')
            bf.append('[-]')
            bf.append(self._move_abs(tmp, len_cell))
            bf.append('+')
            bf.append(self._move_abs(len_cell, active))
            bf.append('+')
            bf.append(self._move_abs(active, restore))
            current = restore
            bf.append('[')
            bf.append('-')
            bf.append(self._move_abs(restore, char_cell))
            bf.append('+')
            bf.append(self._move_abs(char_cell, restore))
            bf.append(']')
            bf.append(self._move_abs(restore, tmp))
            bf.append(']')
            current = tmp

            # Return to exec_cell before closing the non-EOF branch.
            bf.append(self._move_abs(current, exec_cell))
            current = exec_cell
            bf.append(']')

            # Discard newline/EOF scratch state.
            bf.append(self._move_abs(current, restore))
            bf.append('[-]')
            current = restore

            # Return to exec_cell and close the one-shot gate for this slot.
            bf.append(self._move_abs(current, exec_cell))
            bf.append(']')
            current = exec_cell

        bf.append(self._move_abs(current, base_cell))
        return bf

    def _emit_runtime_string_eq(self, var_name, literal, body_lines, base_cell):
        """Emit BF for `if s == "literal":` where s is a runtime string."""
        bf = []
        str_cell = self.get_cell(var_name) + 1
        scratch = self._reserve_scratch(3)
        match_cell = scratch
        tmp_cell = scratch + 1
        restore_cell = scratch + 2
        body_indent = None

        def emit_cell_eq_const(cell, value, current):
            seq = []

            # Clear temp cells.
            for scratch_cell in (tmp_cell, restore_cell):
                seq.append(self._move_abs(current, scratch_cell))
                seq.append('[-]')
                current = scratch_cell

            # Copy source -> tmp + restore.
            seq.append(self._move_abs(current, cell))
            current = cell
            seq.append('[')
            seq.append('-')
            seq.append(self._move_abs(current, tmp_cell))
            seq.append('+')
            current = tmp_cell
            seq.append(self._move_abs(current, restore_cell))
            seq.append('+')
            current = restore_cell
            seq.append(self._move_abs(current, cell))
            current = cell
            seq.append(']')

            # Restore original source cell.
            seq.append(self._move_abs(current, restore_cell))
            current = restore_cell
            seq.append('[')
            seq.append('-')
            seq.append(self._move_abs(current, cell))
            seq.append('+')
            current = cell
            seq.append(self._move_abs(current, restore_cell))
            current = restore_cell
            seq.append(']')

            # Compare tmp against constant. Any nonzero result clears match_cell.
            seq.append(self._move_abs(current, tmp_cell))
            current = tmp_cell
            if value > 0:
                seq.append('-' * value)
            seq.append('[')
            seq.append('-')
            seq.append(self._move_abs(current, match_cell))
            seq.append('[-]')
            current = match_cell
            seq.append(self._move_abs(current, tmp_cell))
            current = tmp_cell
            seq.append(']')
            return seq, current

        if body_lines:
            first_nonempty = next((line for line in body_lines if line.strip()), None)
            if first_nonempty is not None:
                body_indent = len(first_nonempty) - len(first_nonempty.lstrip())

        current = base_cell

        # match_cell = 1
        bf.append(self._move_abs(current, match_cell))
        current = match_cell
        bf.append('[-]+')

        # Exact match requires equal stored length.
        seq, current = emit_cell_eq_const(str_cell, len(literal), current)
        bf.extend(seq)

        for idx, char in enumerate(literal):
            char_cell = str_cell + idx + 1
            seq, current = emit_cell_eq_const(char_cell, ord(char), current)
            bf.extend(seq)

        # Execute body once if match_cell is still set.
        bf.append(self._move_abs(current, match_cell))
        bf.append('[')
        dedented_body = []
        for body_line in body_lines:
            if not body_line.strip() or body_indent is None:
                dedented_body.append(body_line)
            else:
                dedented_body.append(body_line[body_indent:])
        bf.extend(self._transpile_block(dedented_body, base_cell=match_cell))
        bf.append('[-]')
        bf.append(']')
        current = match_cell

        # Return to caller base cell.
        bf.append(self._move_abs(current, base_cell))
        return bf

    def _emit_runtime_string_case_transform(self, var_name, to_lower, base_cell):
        """Emit BF to lowercase/uppercase a runtime string in place."""
        bf = []
        str_cell = self.get_cell(var_name) + 1
        length = self.runtime_string_capacity

        scratch = self._reserve_scratch(3)
        tmp = scratch
        restore = scratch + 1
        flag = scratch + 2

        start_ord = ord('A') if to_lower else ord('a')
        end_ord = ord('Z') if to_lower else ord('z')
        shift = 32 if to_lower else -32

        for idx in range(length):
            char_cell = str_cell + idx + 1
            for target in range(start_ord, end_ord + 1):
                current = base_cell

                # Clear scratch cells.
                for cell in (tmp, restore, flag):
                    bf.append(self._move_abs(current, cell))
                    bf.append('[-]')
                    current = cell

                # Copy char -> tmp + restore.
                bf.append(self._move_abs(current, char_cell))
                current = char_cell
                bf.append('[')
                bf.append('-')
                bf.append(self._move_abs(current, tmp))
                bf.append('+')
                current = tmp
                bf.append(self._move_abs(current, restore))
                bf.append('+')
                current = restore
                bf.append(self._move_abs(current, char_cell))
                current = char_cell
                bf.append(']')

                # Restore original char from restore.
                bf.append(self._move_abs(current, restore))
                current = restore
                bf.append('[')
                bf.append('-')
                bf.append(self._move_abs(current, char_cell))
                bf.append('+')
                current = char_cell
                bf.append(self._move_abs(current, restore))
                current = restore
                bf.append(']')

                # tmp = char - target
                bf.append(self._move_abs(current, tmp))
                current = tmp
                bf.append('-' * target)

                # flag = 1 if tmp == 0 else 0
                bf.append(self._move_abs(current, flag))
                current = flag
                bf.append('+')
                bf.append(self._move_abs(current, tmp))
                current = tmp
                bf.append('[')
                bf.append('-')
                bf.append(self._move_abs(current, flag))
                current = flag
                bf.append('[-]')
                bf.append(self._move_abs(current, tmp))
                current = tmp
                bf.append(']')

                # Apply case shift on match.
                bf.append(self._move_abs(current, flag))
                current = flag
                bf.append('[')
                bf.append('-')
                bf.append(self._move_abs(current, char_cell))
                current = char_cell
                if shift > 0:
                    bf.append('+' * shift)
                else:
                    bf.append('-' * (-shift))
                bf.append(self._move_abs(current, flag))
                current = flag
                bf.append(']')

                bf.append(self._move_abs(current, base_cell))
        return bf
    
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
                    if f'print({var_name})' in check_line or f'{var_name}[' in check_line or f'len({var_name})' in check_line or f'if {var_name} ==' in check_line or f'{var_name} = {var_name}.lower()' in check_line or f'{var_name} = {var_name}.upper()' in check_line:
                        is_string_used = True
                        break
                
                if var_name in self.var_cells:
                    old_entry = self.var_cells[var_name]
                    if is_string_used and old_entry[1] == 'num':
                        self.var_cells[var_name] = (old_entry[0], 'str')
                        self.string_vars[var_name] = ''
                        var_count += self.runtime_string_capacity
                else:
                    if is_string_used:
                        self.var_cells[var_name] = (var_count, 'str')
                        self.string_vars[var_name] = ''
                        var_count += 1 + self.runtime_string_capacity
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
                    if f'print({var_name})' in check_line or f'{var_name}[' in check_line or f'len({var_name})' in check_line or f'if {var_name} ==' in check_line or f'{var_name} = {var_name}.lower()' in check_line or f'{var_name} = {var_name}.upper()' in check_line:
                        is_string_used = True
                        break
                
                if var_name in self.var_cells:
                    # Already exists, update type if needed
                    old_entry = self.var_cells[var_name]
                    if is_string_used and old_entry[1] == 'num':
                        # Need to reallocate as string - adjust var_count
                        self.var_cells[var_name] = (old_entry[0], 'str')
                        self.string_vars[var_name] = ''
                        var_count += self.runtime_string_capacity
                else:
                    # New variable
                    if is_string_used:
                        self.var_cells[var_name] = (var_count, 'str')
                        self.string_vars[var_name] = ''
                        var_count += 1 + self.runtime_string_capacity
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
                        var_count += self.runtime_string_capacity
                continue
            
            match = re.match(r'(\w+)\s*=\s*(\w+)\[(\d+)\]', line)
            if match:
                src = match.group(2)
                if src in self.var_cells:
                    old_entry = self.var_cells[src]
                    if old_entry[1] == 'num':
                        self.var_cells[src] = (old_entry[0], 'str')
                        self.string_vars[src] = ''
                        var_count += self.runtime_string_capacity
                continue

            # s = s.lower() / s = s.upper() imply string typing
            match = re.match(r'(\w+)\s*=\s*(\w+)\.(lower|upper)\(\)$', line)
            if match:
                dest = match.group(1)
                src = match.group(2)
                for name in (dest, src):
                    if name in self.var_cells:
                        old_entry = self.var_cells[name]
                        if old_entry[1] == 'num':
                            self.var_cells[name] = (old_entry[0], 'str')
                            self.string_vars[name] = ''
                            var_count += self.runtime_string_capacity
                    else:
                        self.var_cells[name] = (var_count, 'str')
                        self.string_vars[name] = ''
                        var_count += 1 + self.runtime_string_capacity
                continue

            # if s == "literal": implies string typing for runtime variables
            match = re.match(r'if\s+(\w+)\s*==\s*"[^"]*":', line)
            if match:
                var_name = match.group(1)
                if var_name in self.var_cells:
                    old_entry = self.var_cells[var_name]
                    if old_entry[1] == 'num':
                        self.var_cells[var_name] = (old_entry[0], 'str')
                        self.string_vars[var_name] = ''
                        var_count += self.runtime_string_capacity
                else:
                    self.var_cells[var_name] = (var_count, 'str')
                    self.string_vars[var_name] = ''
                    var_count += 1 + self.runtime_string_capacity
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
        self.scratch_used = 0
        
        # Reserve cells: 0=temp, then variables
        bf.append('[-]')  # cell 0 = temp
        for i in range(var_count):
            bf.append('>[-]')  # initialize vars to 0
        # Return to cell 0 after init
        if var_count > 0:
            bf.append('<' * var_count)
        
        # Process statements recursively (handles nested control flow)
        bf.extend(self._transpile_block(lines, base_cell=0))
        
        return ''.join(bf)
    
    def _transpile_block(self, lines, base_cell=0):
        """Transpile a block of lines with nested control flow support.
        Pointer starts and ends at base_cell position."""
        bf = []
        i = 0
        while i < len(lines):
            orig_line = lines[i]
            line = orig_line.strip()
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # while x > 0: - BF loop with recursive body
            match = re.match(r'while\s+(\w+)\s*>\s*0:', line)
            if match:
                var = match.group(1)
                cell = self.get_cell(var) + 1  # absolute cell position
                while_indent = len(orig_line) - len(orig_line.lstrip())
                
                # Collect body lines (preserve indentation for nesting)
                i += 1
                body_lines = []
                while i < len(lines):
                    bl = lines[i]
                    if not bl.strip():
                        body_lines.append(bl)
                        i += 1
                        continue
                    bi = len(bl) - len(bl.lstrip())
                    if bi <= while_indent:
                        break
                    body_lines.append(bl)
                    i += 1
                
                # Navigate from base_cell to var cell
                nav = cell - base_cell
                if nav > 0:
                    bf.append('>' * nav)
                elif nav < 0:
                    bf.append('<' * (-nav))
                bf.append('[')
                
                # Recursively process body at new base_cell
                bf.extend(self._transpile_block(body_lines, base_cell=cell))
                
                bf.append(']')
                # Navigate back to base_cell
                if nav > 0:
                    bf.append('<' * nav)
                elif nav < 0:
                    bf.append('>' * (-nav))
                continue
            
            # if x > 0: - execute body once if condition is true
            match = re.match(r'if\s+(\w+)\s*>\s*0:', line)
            if match:
                var = match.group(1)
                cell = self.get_cell(var) + 1  # absolute cell position
                scratch = self._reserve_scratch(2)
                temp_cell = scratch
                run_cell = scratch + 1
                if_indent = len(orig_line) - len(orig_line.lstrip())
                
                # Collect body lines (preserve indentation)
                i += 1
                body_lines = []
                while i < len(lines):
                    bl = lines[i]
                    if not bl.strip():
                        body_lines.append(bl)
                        i += 1
                        continue
                    bi = len(bl) - len(bl.lstrip())
                    if bi <= if_indent:
                        break
                    body_lines.append(bl)
                    i += 1
                
                current = base_cell

                # Clear scratch cells.
                for scratch_cell in (temp_cell, run_cell):
                    bf.append(self._move_abs(current, scratch_cell))
                    bf.append('[-]')
                    current = scratch_cell

                # Copy condition into temp and run cells, preserving the original value.
                bf.append(self._move_abs(current, cell))
                current = cell
                bf.append('[')
                bf.append('-')
                bf.append(self._move_abs(current, temp_cell))
                bf.append('+')
                current = temp_cell
                bf.append(self._move_abs(current, run_cell))
                bf.append('+')
                current = run_cell
                bf.append(self._move_abs(current, cell))
                current = cell
                bf.append(']')

                # Restore the original condition value.
                bf.append(self._move_abs(current, temp_cell))
                current = temp_cell
                bf.append('[')
                bf.append('-')
                bf.append(self._move_abs(current, cell))
                bf.append('+')
                current = cell
                bf.append(self._move_abs(current, temp_cell))
                current = temp_cell
                bf.append(']')

                # Execute body once when run_cell is non-zero.
                bf.append(self._move_abs(current, run_cell))
                current = run_cell
                bf.append('[')
                bf.extend(self._transpile_block(body_lines, base_cell=run_cell))
                bf.append('[-]')
                bf.append(']')

                bf.append(self._move_abs(run_cell, base_cell))
                continue
            
            # --- Skip unsupported patterns (consume body, emit nothing) ---
            
            # if s == "literal":
            match = re.match(r'if\s+(\w+)\s*==\s*"([^"]*)":', line)
            if match:
                var_name = match.group(1)
                literal = match.group(2)
                skip_indent = len(orig_line) - len(orig_line.lstrip())
                i += 1
                body_lines = []
                while i < len(lines):
                    bl = lines[i]
                    if not bl.strip():
                        body_lines.append(bl)
                        i += 1
                        continue
                    if len(bl) - len(bl.lstrip()) <= skip_indent:
                        break
                    body_lines.append(bl)
                    i += 1
                if self.get_type(var_name) == 'str':
                    bf.extend(self._emit_runtime_string_eq(var_name, literal, body_lines, base_cell))
                continue
            
            # while s == "literal":
            match = re.match(r'while\s+\w+\s*==\s*"[^"]*":', line)
            if match:
                skip_indent = len(orig_line) - len(orig_line.lstrip())
                i += 1
                while i < len(lines):
                    bl = lines[i]
                    if not bl.strip():
                        i += 1
                        continue
                    if len(bl) - len(bl.lstrip()) <= skip_indent:
                        break
                    i += 1
                continue
            
            # if x == n:
            match = re.match(r'if\s+\w+\s*==\s*\d+:', line)
            if match:
                skip_indent = len(orig_line) - len(orig_line.lstrip())
                i += 1
                while i < len(lines):
                    bl = lines[i]
                    if not bl.strip():
                        i += 1
                        continue
                    if len(bl) - len(bl.lstrip()) <= skip_indent:
                        break
                    i += 1
                continue
            
            # while x == n:
            match = re.match(r'while\s+\w+\s*==\s*\d+:', line)
            if match:
                skip_indent = len(orig_line) - len(orig_line.lstrip())
                i += 1
                while i < len(lines):
                    bl = lines[i]
                    if not bl.strip():
                        i += 1
                        continue
                    if len(bl) - len(bl.lstrip()) <= skip_indent:
                        break
                    i += 1
                continue
            
            # Simple statement - delegate to transpile_line
            bf.extend(self.transpile_line(line, base_cell=base_cell))
            i += 1
        
        return bf
    
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
                current = base_cell
                
                # If we have a literal string, use it directly
                if str_len > 0:
                    target = cell + 2
                    bf.append(self._move_abs(current, target))
                    current = target
                    
                    # Simple loop: repeat str_len times
                    for _ in range(str_len):
                        bf.append('.')  # print char
                        bf.append('>')
                        current += 1
                    
                    bf.append(self._move_abs(current, base_cell))
                else:
                    target = cell + 2
                    bf.append(self._move_abs(current, target))
                    current = target
                    for _ in range(10):
                        bf.append('.')
                        bf.append('>')
                        current += 1
                    bf.append(self._move_abs(current, base_cell))
                bf.extend(self._emit_print_newline(base_cell))
                return bf
        
        # print("text") - navigate to temp cell (0) first
        match = re.match(r'print\("([^"]*)"\)', line)
        if match:
            text = match.group(1) + '\n'
            return self._emit_temp_text(text, base_cell)
        
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
            bf.extend(self._emit_print_newline(base_cell))
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
            bf.extend(self._emit_print_newline(base_cell=base_cell))
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
            bf.extend(self._emit_print_newline(base_cell=base_cell))
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
            bf.extend(self._emit_print_newline(base_cell=base_cell))
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
                dest_abs = self.get_cell(dest) + 1
                src_abs = self.get_cell(src) + 1

                # Return to temp cell 0 for a stable copy routine.
                if base_cell > 0:
                    bf.append('<' * base_cell)
                elif base_cell < 0:
                    bf.append('>' * (-base_cell))

                bf.append('[-]')

                # Clear destination.
                bf.append('>' * dest_abs)
                bf.append('[-]')
                bf.append('<' * dest_abs)

                # Move src into temp while mirroring into dest.
                bf.append('>' * src_abs)
                bf.append('[')
                bf.append('-')
                bf.append('<' * src_abs)
                bf.append('+')
                bf.append('>' * dest_abs)
                bf.append('+')
                bf.append('<' * dest_abs)
                bf.append('>' * src_abs)
                bf.append(']')

                # Restore src from temp.
                bf.append('<' * src_abs)
                bf.append('[')
                bf.append('-')
                bf.append('>' * src_abs)
                bf.append('+')
                bf.append('<' * src_abs)
                bf.append(']')

                # Return to original base cell.
                if base_cell > 0:
                    bf.append('>' * base_cell)
                elif base_cell < 0:
                    bf.append('<' * (-base_cell))
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
        # x = x - y (variable subtraction, preserving y)
        match = re.match(r'(\w+)\s*=\s*(\w+)\s*-\s*([a-zA-Z_]\w*)$', line)
        if match:
            dest = match.group(1)
            left = match.group(2)
            right = match.group(3)
            if dest == left:
                x_cell = self.get_cell(dest) + 1  # absolute
                y_cell = self.get_cell(right) + 1  # absolute
                # Navigate from base_cell to cell 0 (temp)
                if base_cell > 0:
                    bf.append('<' * base_cell)
                elif base_cell < 0:
                    bf.append('>' * (-base_cell))
                # Clear temp
                bf.append('[-]')
                # Go to y
                bf.append('>' * y_cell)
                # Move y to temp: y[ <y_cell + >y_cell - ]
                bf.append('[')
                bf.append('<' * y_cell)
                bf.append('+')
                bf.append('>' * y_cell)
                bf.append('-')
                bf.append(']')
                # Go to temp (cell 0)
                bf.append('<' * y_cell)
                # For each in temp: decrement x, restore y
                # temp[ >x_cell - ... >y_cell + ... <y_cell - ]
                bf.append('[')
                bf.append('>' * x_cell)
                bf.append('-')
                # Navigate from x to y
                if y_cell > x_cell:
                    bf.append('>' * (y_cell - x_cell))
                elif y_cell < x_cell:
                    bf.append('<' * (x_cell - y_cell))
                bf.append('+')
                # Navigate from y to temp (cell 0)
                bf.append('<' * y_cell)
                bf.append('-')
                bf.append(']')
                # Navigate from cell 0 back to base_cell
                if base_cell > 0:
                    bf.append('>' * base_cell)
                elif base_cell < 0:
                    bf.append('<' * (-base_cell))
                return bf
        
        # x = input("prompt") - print prompt first, then read
        match = re.match(r'(\w+)\s*=\s*input\("([^"]*)"\)', line)
        if match:
            var = match.group(1)
            prompt = match.group(2)
            if self.get_type(var) == 'str':
                return self._emit_string_input(var, prompt, base_cell)
            else:
                # Print prompt using cell 0 (temp) to avoid clobbering base_cell
                if base_cell > 0:
                    bf.append('<' * base_cell)
                elif base_cell < 0:
                    bf.append('>' * (-base_cell))
                for char in prompt:
                    bf.append('[-]')
                    bf.append('+' * ord(char))
                    bf.append('.')
                if base_cell > 0:
                    bf.append('>' * base_cell)
                elif base_cell < 0:
                    bf.append('<' * (-base_cell))
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
                return self._emit_string_input(var, '', base_cell)
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
                if src in self.string_vars and self.string_vars.get(src, ''):
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

                return self._emit_runtime_string_case_transform(src, to_lower=True, base_cell=base_cell)
        
        # s = s.upper() - convert string to uppercase in place
        match = re.match(r'(\w+)\s*=\s*(\w+)\.upper\(\)$', line)
        if match:
            dest = match.group(1)
            src = match.group(2)
            if self.get_type(src) == 'str':
                if src in self.string_vars and self.string_vars.get(src, ''):
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

                return self._emit_runtime_string_case_transform(src, to_lower=False, base_cell=base_cell)
        
        return bf

def main():
    source = sys.stdin.read()
    t = Transpiler()
    result = t.transpile(source)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()
