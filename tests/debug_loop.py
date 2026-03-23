#!/usr/bin/env python3
"""Debug: simple loop with input"""
def p(s):
    for c in s:
        print('[-]')
        print('+' * ord(c))
        print('.')

# Init
print('[-]')  # cell 0

# Loop once
print('[')
p('X')
print(',')  # read to consume input
print(']')

print(p('DONE'))