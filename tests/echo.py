#!/usr/bin/env python3
"""Simple game - echo input back"""
import sys

# Simple echo game: read char, print "YOU TYPED: X"
def p(s):
    for c in s:
        print('[-]+' + '+' * (ord(c) - 1) + '.')

p('TYPE:')
print(',')  # read to cell 0

# Now move to cell 1 for echo
print('>')
p('YOU:')
print('<')
print('.')  # print the char

# Exit
p('BYE')