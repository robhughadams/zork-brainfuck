#!/usr/bin/env python3
"""Debug: fixed loop"""
def p(s):
    for c in s:
        print('[-]')
        print('+' * ord(c))
        print('.')

# Init: run loop 3 times
print('+++')  # cell 0 = 3

print('[')    # while cell > 0
p('X')       # print X
print('-')    # decrement
print(']')    # end while

p('DONE')