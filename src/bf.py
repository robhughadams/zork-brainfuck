#!/usr/bin/env python3
"""Simple Brainfuck interpreter"""
import sys

def run_bf(code, input_data=''):
    tape = [0] * 30000
    ptr = 0
    input_idx = 0
    output = []
    pc = 0
    
    # Find matching brackets
    brackets = {}
    stack = []
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if stack:
                open_pos = stack.pop()
                brackets[open_pos] = i
                brackets[i] = open_pos
    
    while pc < len(code):
        cmd = code[pc]
        
        if cmd == '>':
            ptr += 1
            if ptr >= len(tape):
                tape.append(0)
        elif cmd == '<':
            ptr = max(0, ptr - 1)
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[ptr]))
        elif cmd == ',':
            if input_idx < len(input_data):
                tape[ptr] = ord(input_data[input_idx])
                input_idx += 1
            else:
                tape[ptr] = 0
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = brackets.get(pc, pc)
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = brackets.get(pc, pc)
        
        pc += 1
    
    return ''.join(output)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: bf.py <file.bf> [input]")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    
    input_data = sys.argv[2] if len(sys.argv) > 2 else ''
    result = run_bf(code, input_data)
    sys.stdout.write(result)