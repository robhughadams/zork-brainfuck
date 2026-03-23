#!/usr/bin/env python3
"""Debug: fixed loop - don't clear inside loop"""
def p(s, clear_first=False):
    for c in s:
        if clear_first:
            print('[-]')
        print('+' * ord(c))
        print('.')

# Init: run loop 3 times
print('+++')

print('[')
p('X', clear_first=False)  # Don't clear inside loop!
print('-')
print(']')

p('DONE', clear_first=True)