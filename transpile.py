#!/usr/bin/env python3
"""Transpiler: Python subset -> Brainfuck"""

import re
import sys

class Transpiler:
    def __init__(self):
        self.variables = {}
    
    def transpile(self, source):
        lines = source.strip().split('\n')
        bf = []
        
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
        
        return ''.join(bf)

def main():
    source = sys.stdin.read()
    t = Transpiler()
    result = t.transpile(source)
    sys.stdout.write(result)

if __name__ == '__main__':
    main()