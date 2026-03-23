#!/usr/bin/env python3
"""Simple game - only LOOK command"""
import sys

def p(s):
    for c in s:
        print('[-]+' + '+' * (ord(c) - 1) + '.')

# Print prompt
p('CMD?')

# Read command to cell 0
print(',')

# Check if input == 76 (L for LOOK)
# Subtract 76: if result is 0, it was 'L'
print('[------')  # -6
print('------')  # -6
print('------')  # -6  
print('------')  # -6
print('------')  # -6
print('------')  # -6
print('------')  # -6
print('------')  # -6
print('------')  # -6
print('------')  # -6
print('------')  # -6
print('------')  # -6 = -72
print('----')   # -4 = -76
print('>')      # move to cell 1 (temp)
print('[')      # if temp != 0 (wasn't L)
print('<<-')    # back to cell 0, clear
print(']')      # end temp check
print('<<')     # back to cell 0

# If L: print "ROOM1"
print('<')      # cell -1 = temp? No this is getting confusing

# Let me restart - use clearer cell layout
# Cell 0: input
# Cell 1: temp for comparison

print('>')      # cell 1 (temp)
print('[-]')    # clear
print('<')      # back to 0

print('[')      # if input != 0
print('--------')  # -8
print('--------')  # -8 = -16
print('--------')  # -8 = -24
print('--------')  # -8 = -32
print('--------')  # -8 = -40
print('--------')  # -8 = -48
print('--------')  # -8 = -56
print('--------')  # -8 = -64
print('--------')  # -8 = -72
print('----')   # -4 = -76 (L)
print('>')     # to cell 1
print('[')     # if not 0 (wasn't L)
print('<<-')   # clear and continue
print(']')
print('<<')    # back to cell 0

# If L (now 0): print room
print('<')
print('[')
p('ROOM1')
print(']')

# Exit
p('BYE')