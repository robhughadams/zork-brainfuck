#!/usr/bin/env python3
"""Debug: simple loop without input"""
def p(s):
    for c in s:
        print('[-]')
        print('+' * ord(c))
        print('.')

# Init cell 0 = 1 (to enter loop)
print('+')

# Loop
print('[')
p('X')
print(']')

p('DONE')