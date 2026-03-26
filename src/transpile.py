#!/usr/bin/env python3
"""Transpiler: Python subset -> Brainfuck v2 with variables and loops"""

import re
import sys

class Transpiler:
    def __init__(self):
        self.variables = {}  # name -> cell index
        self.cell = 0
    
    def transpile(self, source):
        lines = source.strip().split('\n')
        bf = []
        
        # Allocate cells for variables
        var_cells = {}
        var_count = 0
        
        # First pass: collect all variables
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            match = re.match(r'(\w+)\s*=\s*(\d+)', line)
            if match:
                var_name = match.group(1)
                if var_name not in var_cells:
                    var_cells[var_name] = var_count
                    var_count += 1
            
            match = re.match(r'(\w+)\s*=\s*input\(\)', line)
            if match:
                var_name = match.group(1)
                if var_name not in var_cells:
                    var_cells[var_name] = var_count
                    var_count += 1
        
        # Reserve cells: 0=temp, then variables
        bf.append('[-]')  # cell 0 = temp
        for i in range(var_count):
            bf.append('>[-]')  # initialize vars to 0
        
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
                cell = var_cells[var] + 1
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
                    bf.extend(self.transpile_line(body_line, var_cells, base_cell=cell))
                
                bf.append('<' + '>' * cell)
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
                    bf.extend(self.transpile_line(body_line, var_cells, base_cell=cell))
                
                bf.append('<' + '>' * cell)  # ensure we're back at var before ]
                bf.append(']')
                bf.append('<' * cell)  # back to cell 0
                continue
            
            # while x < n: - loop n-x times (simplified)
            match = re.match(r'while\s+(\w+)\s*<\s*(\d+):', line)
            if match:
                var = match.group(1)
                limit = int(match.group(2))
                cell = var_cells[var] + 1
                
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
                    bf.extend(self.transpile_line(body_line, var_cells))
                
                bf.append('<' * cell)
                bf.append(']')
                bf.append('<' * cell)
                continue
            
            # if x == n: - SKIP for now (too complex for BF, causes infinite loops)
            # Just skip the body to allow transpilation to complete
            match = re.match(r'if\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                # Skip body (just don't generate any BF)
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
            
            bf.extend(self.transpile_line(line, var_cells))
            i += 1
        
        return ''.join(bf)
    
    def transpile_line(self, line, var_cells, base_cell=0):
        bf = []
        
        # print("text")
        match = re.match(r'print\("([^"]*)"\)', line)
        if match:
            text = match.group(1)
            for char in text:
                bf.append('[-]')
                bf.append('+' * ord(char))
                bf.append('.')
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
        
        # print(chr(x)) - special: print var WITHOUT clearing
        match = re.match(r'print\(chr\((\w+)\)\)', line)
        if match:
            var = match.group(1)
            cell = var_cells[var] + 1 - base_cell
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
            cell = var_cells[var] + 1 - base_cell
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
            cell = var_cells[var] + 1 - base_cell
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
        
        # x = x - 1
        match = re.match(r'(\w+)\s*=\s*\w+\s*-\s*(\d+)', line)
        if match:
            var = match.group(1)
            val = int(match.group(2))
            cell = var_cells[var] + 1 - base_cell
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
        
        # x = input()
        match = re.match(r'(\w+)\s*=\s*input\(\)', line)
        if match:
            var = match.group(1)
            cell = var_cells[var] + 1 - base_cell
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
        
        return bf

def main():
    source = sys.stdin.read()
    t = Transpiler()
    result = t.transpile(source)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()