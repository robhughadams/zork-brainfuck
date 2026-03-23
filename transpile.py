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
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Check for variable assignment
            match = re.match(r'(\w+)\s*=\s*(\d+)', line)
            if match:
                var_name = match.group(1)
                if var_name not in var_cells:
                    var_cells[var_name] = var_count
                    var_count += 1
        
        # Reserve cells: 0=temp, then variables
        bf.append('[-]')  # cell 0 = temp
        for i in range(var_count):
            bf.append('>[-]')  # initialize vars to 0
        
        # Process statements
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # print("text")
            match = re.match(r'print\("([^"]*)"\)', line)
            if match:
                text = match.group(1)
                for char in text:
                    bf.append('[-]')
                    bf.append('+' * ord(char))
                    bf.append('.')
            
            # x = 5
            match = re.match(r'(\w+)\s*=\s*(\d+)', line)
            if match:
                var = match.group(1)
                val = int(match.group(2))
                cell = var_cells[var] + 1  # +1 because cell 0 is temp
                bf.append('>' * cell)
                bf.append('[-]')
                bf.append('+' * val)
                bf.append('<' * cell)
            
            # x = x + 1
            match = re.match(r'(\w+)\s*=\s*\w+\s*\+\s*(\d+)', line)
            if match:
                var = match.group(1)
                val = int(match.group(2))
                cell = var_cells[var] + 1
                bf.append('>' * cell)
                bf.append('+' * val)
                bf.append('<' * cell)
            
            # while x < n:
            match = re.match(r'while\s+(\w+)\s*<\s*(\d+):', line)
            if match:
                var = match.group(1)
                limit = int(match.group(2))
                cell = var_cells[var] + 1
                # Loop while cell < limit
                bf.append('>' * cell)
                bf.append('[')  # while cell > 0
                bf.append('-' * limit)  # subtract limit
                bf.append('>')  # temp cell
                bf.append('[')  # if not zero (was >= limit)
                bf.append('<<-')  # clear and exit
                bf.append(']')
                bf.append('<<' + '+' * limit)  # restore value
                bf.append('<' * cell)
                
                # Find body (next lines with more indent)
                # This is a simplified version - just look for print statements
        
        return ''.join(bf)

def main():
    source = sys.stdin.read()
    t = Transpiler()
    result = t.transpile(source)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()