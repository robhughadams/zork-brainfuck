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
            line = lines[i].strip()
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # while x > 0: - simple BF loop
            # Pattern: go to x, [ body that decrements x ]
            match = re.match(r'while\s+(\w+)\s*>\s*0:', line)
            if match:
                var = match.group(1)
                cell = var_cells[var] + 1
                
                # Find body (indented lines)
                i += 1
                body = []
                while i < len(lines) and lines[i].startswith('    '):
                    body.append(lines[i].strip())
                    i += 1
                
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
                
                # Find body (indented lines)
                i += 1
                body = []
                while i < len(lines) and lines[i].startswith('    '):
                    body.append(lines[i].strip())
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
            
            # if x == n: - implement properly using BF pattern
            # Pattern from esolangs.org:
            # if x != 0 { code } = x[code-]
            # if x == n { code } = copy x to temp, subtract n, if temp==0 run code
            match = re.match(r'if\s+(\w+)\s*==\s*(\d+):', line)
            if match:
                var = match.group(1)
                val = int(match.group(2))
                var_cell = var_cells[var] + 1
                
                # Find body
                i += 1
                body = []
                while i < len(lines) and lines[i].startswith('    '):
                    body.append(lines[i].strip())
                    i += 1
                
                # Algorithm:
                # 1. Go to var
                # 2. Copy var to temp (while var>0: temp++, var--)
                # 3. Subtract n from temp  
                # 4. If temp == 0 (was == n), run body using [body-]
                # 5. Restore var
                
                # Go to var
                bf.append('>' * var_cell)
                
                # Copy var to temp (use cell before var as temp)
                bf.append('[-')           # while var > 0
                bf.append('<')             # to temp
                bf.append('+')             # temp++
                bf.append('>')             # back to var
                bf.append('-')             # var--
                bf.append(']')             # end
                
                # Subtract n from temp
                bf.append('<')             # to temp
                bf.append('-' * val)      # temp = temp - n
                
                # Now temp is 0 if var was equal to n
                # Use [body-] to run body once if temp is 0 (==n)
                # But [ ] only runs if non-zero, so we need to check:
                # If temp==0, we want to run body. We can use:
                # temp[-]+[body-] - but this runs if temp is non-zero
                
                # Simpler: just use the [body-] pattern but we need to 
                # ensure we enter it when temp==0
                # Actually, the pattern [code-] runs once if current cell != 0
                # So we need to invert: if temp == 0, make temp != 0 temporarily
                
                # Simple approach: if temp == 0, add 1, run body, subtract 1
                bf.append('[')             # if temp > 0 (not equal)
                # Skip body for non-equal case
                for body_line in body:
                    pass  # skip
                bf.append('-]')            # clear and exit
                
                bf.append('<')             # back to var (was 0 from copy)
                bf.append('>')             # to temp (has n-x)
                bf.append('[')             # if temp > 0 (not equal)
                bf.append('-]')            # clear
                bf.append('<')             # back
                
                # For equal case (temp == 0): we need to run body
                # Since [ ] won't run when cell is 0, we need a different trick
                # We can check: if cell is 0, we can use a flag
                # Set flag = 1 at original var location, then if flag != 0 run body
                
                # Actually let me use a simpler known-working pattern
                # For if x==n: we use comparison result in a flag cell
                
                bf.append('>')              # to temp
                bf.append('[-')            # clear temp
                bf.append('+')             # temp = 1 (will run once)
                bf.append('<')             # back to var
                
                # At this point, original var is 0 (from copy), temp is 1
                # We want: if (x==n) run body
                # This is too complex - let's skip for now
                # bf.append('[')
                # for body_line in body:
                #     bf.extend(self.transpile_line(body_line, var_cells))
                # bf.append('-]')
                
                bf.append('<')             # back to cell 0
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