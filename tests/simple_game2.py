#!/usr/bin/env python3
"""Generate working BF game - simpler version"""
import sys

def p(s):
    """Print string"""
    for c in s:
        print('[-]+' + '+' * (ord(c) - 1) + '.')

# Simple game: just print prompt and handle one command
p('HI')  # Print HI
print(',')  # Read input  
print('[<<<<<[.>]<-]')  # Echo input back and loop

# Actually this is getting complex. Let me try a simpler direct approach.